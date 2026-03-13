from __future__ import annotations

import duckdb
import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def load_customers(**kwargs):
    data_dir = kwargs["data_dir"]
    con = duckdb.connect()
    con.execute(
        f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv('{data_dir}/customers.csv', header = true)")
    print(f"Loaded {con.execute('SELECT COUNT(*) FROM customers;').fetchone()[0]} customer records.")
    con.close()


def load_transactions(**kwargs):
    data_dir = kwargs["data_dir"]
    con = duckdb.connect()
    con.execute(
        f"CREATE OR REPLACE TABLE transactions AS SELECT * FROM read_json_auto('{data_dir}/transactions/*.json');")
    print(f"Loaded {con.execute('SELECT COUNT(*) FROM transactions;').fetchone()[0]} transactions records.")
    con.close()


def join_and_save_data(**kwargs):
    con = duckdb.connect()
    con.execute(
        "CREATE OR REPLACE TABLE customer_transactions AS SELECT * FROM transactions t JOIN customers c ON t.customer_id = c.customer_id")
    print(
        f"Loaded {con.execute('SELECT COUNT(*) FROM customer_transactions;').fetchone()[0]} transactions with customers records.")
    con.execute("COPY customer_transactions TO 'data/customer_transactions.json'")
    con.close()


@dag(
    dag_id="lab3_data_loading_and_transformation",
    schedule="*/15 * * * *",
    start_date=pendulum.yesterday(),
    catchup=False,
    tags=["lab3", "data loading", "transformation", "duckdb"],
)
def load_and_transform_data():
    start = EmptyOperator(task_id="start")

    load_customers_task = PythonOperator(
        task_id="load_customers",
        python_callable=load_customers,
        op_kwargs={"data_dir": "/opt/airflow/data/"},
    )

    load_transactions_task = PythonOperator(
        task_id="load_transactions",
        python_callable=load_transactions,
        op_kwargs={"data_dir": "/opt/airflow/data/"},
    )

    join_and_save_data_task = PythonOperator(
        task_id="join_and_save_data",
        python_callable=join_and_save_data,
    )

    end = EmptyOperator(task_id="end")

    start >> [load_customers_task, load_transactions_task] >> join_and_save_data_task >> end


load_and_transform_data()
