from __future__ import annotations

import duckdb
import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


@dag(
    dag_id="lab3_data_loading_and_transformation",
    schedule="*/15 * * * *",
    start_date=pendulum.yesterday(),
    catchup=False,
    tags=["lab3", "data loading", "transformation", "duckdb"],
)
def load_and_transform_data():
    def load_and_join_data(**kwargs):
        data_dir = kwargs["data_dir"]

        con = duckdb.connect()  # In-memory DuckDB connection

        con.execute(
            f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv('{data_dir}/customers.csv', header = true)")
        print(f"Loaded {con.execute('SELECT COUNT(*) FROM customers;').fetchone()[0]} customer records.")

        con.execute(
            f"CREATE OR REPLACE TABLE transactions AS SELECT * FROM read_json_auto('{data_dir}/transactions/*.json');")

        con.execute(
            "CREATE OR REPLACE TABLE customer_transactions AS SELECT * FROM transactions t JOIN customers c ON t.customer_id = c.customer_id")

        con.execute("COPY customer_transactions TO 'data/customer_transactions.json'")

    load_data = PythonOperator(
        task_id="load_and_join_data",
        python_callable=load_and_join_data,
        op_kwargs={"data_dir": "/opt/airflow/data/"},
        provide_context=True  # this is needed to provide kwargs
    )

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> load_data >> end  # task dependency


# Call the DAG to create it
load_and_transform_data()
