import csv
import json

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Define the DAG with the following parameters:
# - dag_id: The unique identifier for the DAG.
# - start_date: The date when the DAG should start running.
# - schedule: The schedule for the DAG. In this case, it's set to None, meaning the DAG will not run on a schedule.
# - catchup: Whether to catch up on past runs. In this case, it's set to False, meaning the DAG will not run for past dates.
with DAG(
        dag_id='lab1_basic_data_pipeline',
        start_date=pendulum.yesterday(),
        schedule=None,
        catchup=False,
        tags=['lab 1', 'basic data pipeline']
) as dag:
    # Task 1: Read data from a file (replace with your actual file path)
    read_data = BashOperator(
        task_id='read_data',
        bash_command='echo "Reading data from /path/to/your/data.csv"'
    )

    # Task 2: Transform the data (replace with your actual transformation logic)
    transform_data = BashOperator(
        task_id='transform_data',
        bash_command='echo "Transforming data..."'
    )

    # Task 3: Write the processed data to a new file (replace with your actual file path)
    write_data = BashOperator(
        task_id='write_data',
        bash_command='echo "Writing processed data to /path/to/your/processed_data.csv"'
    )


    # Task 4: Convert data format from CSV to JSON
    def csv_to_json(csv_filepath, json_filepath):
        """
        Converts a CSV file to a JSON file.

        Args:
            csv_filepath: Path to the CSV file.
            json_filepath: Path to the output JSON file.
        """

        data = []
        with open(csv_filepath, "r") as csvfile:
            reader = csv.DictReader(csvfile)  # Use DictReader for named fields
            for row in reader:
                data.append(row)

        with open(json_filepath, "w") as jsonfile:
            json.dump(data, jsonfile, indent=4)  # Use indent for pretty printing


    to_json = PythonOperator(
        task_id='to_json',
        python_callable=csv_to_json,
        op_kwargs={}
    )

    # Define the task dependencies
    read_data >> transform_data >> write_data
