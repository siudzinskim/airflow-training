from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.decorators import task
from datetime import datetime

with DAG(
    dag_id="demo_302_http_deferrable_sensor",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["api", "deferrable", "module 007"]
) as dag:

    # Traditional sensors eat a worker slot while waiting (polling).
    # Setting deferrable=True tells Airflow to use the Triggerer.
    wait_for_api = HttpSensor(
        task_id="wait_for_external_system",
        http_conn_id="my_api_connection",
        endpoint="status/check",
        response_check=lambda response: "SUCCESS" in response.text,
        poke_interval=30,
        deferrable=True  # <--- THIS IS THE KEY PARAMETER
    )

    @task
    def process_api_data():
        print("API is ready! Worker slot was re-acquired to run this task.")

    wait_for_api >> process_api_data()