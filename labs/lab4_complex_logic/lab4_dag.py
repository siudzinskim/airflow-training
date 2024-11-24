from __future__ import annotations

import os
import shutil
from glob import glob

import duckdb
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule


def list_files(**context):
    """Lists files in the transactions directory and pushes the list to XCom."""
    data_dir = context["params"]["data_dir"]
    files = glob(f"{data_dir}/transactions/transactions_*.json")
    context['ti'].xcom_push(key='files', value=files)
    return files


def check_multiple_files(**context):
    """Checks if multiple files were found and pushes a boolean to XCom."""
    files_string = context['ti'].xcom_pull(task_ids='files')
    files = files_string.split(",") if files_string else []  # Split the comma-separated string
    multiple_files = len(files) > 1
    context['ti'].xcom_push(key='multiple_files', value=multiple_files)
    if multiple_files:
        return "send_slack_notification"
    else:
        return "skip_notification"


def stage_files(**context):
    """Moves files to a staging directory."""
    print("moving files to staging area")
    files_string = context['ti'].xcom_pull(task_ids='list_files')
    files = files_string.split(",") if files_string else []
    timestamp = context['ts_nodash']  # Use ts_nodash for cleaner filenames
    staging_dir = f"data/staging/{timestamp}"
    os.makedirs(staging_dir, exist_ok=True)

    for file in files:
        shutil.move(file, staging_dir)


def merge_data(**context):
    """Merges transaction data with customer data and saves the result."""

    timestamp = context['ts_nodash']
    data_dir = context['params']['data_dir']
    staging_dir = f"{data_dir}/staging/{timestamp}"
    output_dir = f"{data_dir}/customer_transactions"
    output_file = f"customer_transactions_{timestamp}.json"
    # os.makedirs(output_dir, exist_ok=True)
    # ## code to merge
    con = duckdb.connect()  # In-memory DuckDB connection
    con.execute(f"CREATE OR REPLACE TABLE transactions AS SELECT * FROM read_json_auto('{staging_dir}/*.json');")
    con.execute(
        f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv('{data_dir}/customers.csv', header = true);")
    con.execute(
        "CREATE OR REPLACE TABLE customer_transactions AS SELECT * FROM transactions t JOIN customers c ON t.customer_id = c.customer_id")
    con.execute(f"COPY customer_transactions TO '{os.path.join(output_dir, output_file)}'")
    con.execute(f"COPY (SELECT * FROM tbl) TO '{os.path.join(output_dir, output_file)}' (HEADER, DELIMITER ',');")


def denormalize_data(**context):
    """Denormalizes the merged data and saves it as a CSV file."""
    timestamp = context['ts_nodash']
    data_dir = context['params']['data_dir']
    input_file = f"{data_dir}/customer_transactions/customer_transactions_{timestamp}.json"
    output_dir = f"{data_dir}/customer_transactions_denormalized"
    output_file = f"customer_transactions_denormalized_{timestamp}.csv"
    # os.makedirs(output_dir, exist_ok=True)
    # ## write code to denormalize
    con = duckdb.connect()  # In-memory DuckDB connection
    con.execute(f"CREATE OR REPLACE TABLE customer_transactions AS SELECT * FROM read_json_auto('{input_file}');")
    con.execute(
        "CREATE OR REPLACE TABLE customer_transactions_denormalized AS SELECT customer_transactions.* EXCLUDE items, UNNEST(items, recursive := true ) FROM customer_transactions")
    print(con.execute(
        "SELECT customer_transactions.* EXCLUDE items, UNNEST(items, recursive := true ) FROM customer_transactions").fetch_df())
    con.execute(
        f"COPY (SELECT * FROM customer_transactions_denormalized) TO '{os.path.join(output_dir, output_file)}' (FORMAT CSV, HEADER, DELIMITER ',');")


def archive_files(**context):
    """Archives processed files."""
    timestamp = context['ts_nodash']
    data_dir = context['params']['data_dir']
    staging_dir = f"{data_dir}/staging/{timestamp}"
    processed_dir = f"{data_dir}/processed/"
    os.makedirs(processed_dir, exist_ok=True)

    for file in glob(f"{staging_dir}/*"):
        shutil.move(file, f"{processed_dir}/{os.path.basename(file)}.{timestamp}")


def print_merged(**context):
    timestamp = context['ts_nodash']
    data_dir = context['params']['data_dir']
    con = duckdb.connect()  # In-memory DuckDB connection
    con.execute(
        f"CREATE OR REPLACE TABLE customer_transactions AS SELECT * FROM read_json_auto('{data_dir}/customer_transactions/*.json');")

    print(con.execute("SELECT * FROM customer_transactions").fetch_df())


def print_denormalized(**context):
    timestamp = context['ts_nodash']
    data_dir = context['params']['data_dir']
    con = duckdb.connect()  # In-memory DuckDB connection
    con.execute(
        f"CREATE OR REPLACE TABLE customer_transactions AS SELECT * FROM read_csv('{data_dir}/customer_transactions_denormalized/*.csv', header = true);")

    print(con.execute("SELECT * FROM customer_transactions").fetch_df())


with DAG(
        dag_id='lab4_data_pipeline',
        start_date=pendulum.yesterday(),
        schedule='@once',
        catchup=False,
        params={"data_dir": "/opt/airflow/data"},
        tags=['lab4', 'xcoms', 'branching', 'data processing']
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ONE_SUCCESS)  # New end task

    check_files = FileSensor(
        task_id='check_for_files',
        filepath='/opt/airflow/data/transactions/*.json',  # Use params here if needed
        poke_interval=5,  # Check every 30 seconds
        timeout=30,  #
        retries=0,
    )

    files_does_not_exist = EmptyOperator(
        task_id='files_does_not_exist',
        trigger_rule=TriggerRule.ALL_FAILED,
    )

    list_files_task = BashOperator(
        task_id="list_files",
        bash_command=f"ls /opt/airflow/data/transactions/transactions_*.json | paste -sd, -",
        do_xcom_push=False,  # Push the output to XCom (key will be 'return_value')
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    files_check = BranchPythonOperator(
        task_id="multiple_files_check",
        python_callable=check_multiple_files,
        provide_context=True,
    )

    send_slack_notification = SlackWebhookOperator(
        task_id='send_slack_notification',
        slack_webhook_conn_id='slack_default',  # Replace with your Slack connection ID
        message="Multiple transaction files found!",
    )

    skip_notification = EmptyOperator(task_id="skip_notification")  # Task to skip notification

    stage_files_task = PythonOperator(
        task_id="stage_files",
        python_callable=stage_files,
        provide_context=True,
        # ## set the trigger rule to process data if one of upstream tasks success
        # trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    merge_data_task = PythonOperator(
        task_id="merge_data",
        python_callable=merge_data,
        provide_context=True,
    )

    denormalize_data_task = PythonOperator(
        task_id="denormalize_data",
        python_callable=denormalize_data,
        provide_context=True,
    )

    print_merged_task = PythonOperator(
        task_id="print_merged",
        python_callable=print_merged,
        provide_context=True
    )

    print_denormalized_task = PythonOperator(
        task_id="print_denormalized",
        python_callable=print_denormalized,
        provide_context=True
    )

    archive_files_task = PythonOperator(
        task_id="archive_files",
        python_callable=archive_files,
        provide_context=True,
    )

    start >> check_files >> [list_files_task, files_does_not_exist]
    list_files_task >> files_check >> [send_slack_notification, skip_notification] >> stage_files_task
    files_does_not_exist >> end
    stage_files_task >> merge_data_task >> denormalize_data_task >> [print_merged_task,
                                                                     print_denormalized_task] >> archive_files_task >> end
