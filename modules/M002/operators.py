from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

# Define a DAG with the following parameters:
# - dag_id: The unique identifier for the DAG.
# - start_date: The date when the DAG should start running.
# - schedule: The schedule for the DAG. In this case, it's set to None, meaning the DAG will not run on a schedule.
# - catchup: Whether to catch up on past runs. In this case, it's set to False, meaning the DAG will not run for past dates.
with DAG(
        dag_id='operator_examples',
        start_date=datetime(2024, 10, 9),
        schedule=None,
        catchup=False
) as dag:
    # Define a dummy start task
    start = DummyOperator(task_id='start')

    # Define a BashOperator task that prints a message
    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo "Hello from Bash Operator!"'
    )


    # Define a PythonOperator task that executes a Python function
    def python_function():
        print("Hello from Python Operator!")


    python_task = PythonOperator(
        task_id='python_task',
        python_callable=python_function
    )

    # Define a SimpleHttpOperator task that makes an HTTP request
    http_task = SimpleHttpOperator(
        task_id='http_task',
        method='GET',
        http_conn_id='http_default',  # Make sure you have a connection named 'http_default'
        endpoint='/quotes',
        log_response=True
    )

    # Define a KubernetesPodOperator task that runs a container in Kubernetes
    kubernetes_task = KubernetesPodOperator(
        task_id='kubernetes_task',
        name="kubernetes_task_pod",
        namespace='default',
        image="alpine:latest",
        cmds=["echo"],
        arguments=["Hello from Kubernetes Operator!"],
    )

    # Define a dummy end task
    end = DummyOperator(task_id='end')

    # Define the task dependencies
    start >> bash_task >> python_task >> http_task >> kubernetes_task >> end
