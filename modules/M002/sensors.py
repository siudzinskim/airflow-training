# /home/marcin/dev/airflow-training/airflow-training/modules/M002/sensors.py
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.filesystem import FileSensor

# DAG that waits for the file and triggers another DAG
with DAG(
        dag_id='file_sensor_dag',
        start_date=datetime(2024, 10, 9),
        schedule=None,  # No scheduled run, trigger manually or via API
        catchup=False
) as dag:
    # Define a dummy start task
    start = DummyOperator(task_id='start')

    # Define a FileSensor task that waits for a file to exist
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/tmp/myfile.txt'
    )

    # Define a TriggerDagRunOperator task that triggers another DAG
    trigger_file_creator_dag = TriggerDagRunOperator(
        task_id='trigger_file_creator_dag',
        trigger_dag_id='file_creator_dag',  # This is the ID of the second DAG
        wait_for_completion=False  # Don't wait for the second DAG to finish
    )

    # Define a BashOperator task that processes the file
    process_file = BashOperator(
        task_id='process_file',
        bash_command='echo "File arrived and processed!"'
    )

    # Define a BashOperator task that removes the file after processing
    remove_file = BashOperator(
        task_id='remove_file',
        bash_command='rm /tmp/myfile.txt'
    )

    # Define a dummy end task
    end = DummyOperator(task_id='end')

    # Define the task dependencies
    start >> [wait_for_file, trigger_file_creator_dag]
    wait_for_file >> process_file >> remove_file >> end

    ## Verify what will happen if you change the tasks dependencies to following:
    # start >> [wait_for_file, trigger_file_creator_dag] >> wait_for_file >> process_file >> remove_file >> end

# DAG that creates the file after a delay
with DAG(
        dag_id='file_creator_dag',
        start_date=datetime(2024, 10, 9),
        schedule=None,
        catchup=False
) as dag:
    # Define a BashOperator task that waits for 120 seconds
    wait = BashOperator(
        task_id='wait',
        bash_command='sleep 120'  # Wait for 120 seconds
    )

    # Define a BashOperator task that creates the file
    create_file = BashOperator(
        task_id='create_file',
        bash_command='touch /tmp/myfile.txt'  # Create the file
    )

    # Define the task dependencies
    wait >> create_file
