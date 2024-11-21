from __future__ import annotations

import random
import time

import pendulum
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# Import from your local script
from random_transactions import generate_transactions


@dag(
    dag_id="lab2_scheduling_and_dependencies",
    schedule="@once",  # Run every minute
    start_date=pendulum.yesterday(),
    catchup=False,
    tags=["lab2", "scheduling", "dependencies"],
)
def generate_transaction_data():
    create_folder = BashOperator(
        task_id="create_folder",
        bash_command="mkdir -p /opt/airflow/data/transactions",
    )

    generate_transactions_task = PythonOperator(
        task_id="generate_transactions",
        python_callable=generate_transactions,
        op_kwargs={'num_transactions': random.randint(9, 99), 'dest_file_prefix': '/opt/airflow/data'}

    )

    def wait_random_time():
        sleep_time = random.randint(60, 540)  # Random sleep between 1 and 9 minutes (in seconds)
        time.sleep(sleep_time)

    wait = PythonOperator(
        task_id="sleep",
        python_callable=wait_random_time
    )

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> create_folder >> generate_transactions_task >> wait >> end

generate_transaction_data()