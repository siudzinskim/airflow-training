# Lab 1: Building a Basic Data Pipeline with Airflow

This lab provides a basic introduction to Airflow and guides participants through creating a simple data pipeline. The instructions are clear and concise, and the barebone code gives them a starting point to build upon. The bonus challenge encourages them to explore additional features and enhance the pipeline's functionality.

## Objective

This lab will introduce you to the core concepts of Apache Airflow, a powerful platform for creating, scheduling, and monitoring data pipelines. You'll learn how to:

- Define a DAG (Directed Acyclic Graph) to represent your data pipeline.
- Use operators to perform tasks within your DAG.
- Set up scheduling for your DAG.
- Monitor the execution of your DAG in the Airflow UI.

## Scenario

You're a data engineer tasked with building a simple data pipeline that processes customer data. The pipeline should perform the following steps:

1. **Read data from a CSV file.**
2. **Transform the data by filtering out inactive customers.**
3. **Write the processed data to a new CSV file.**

## Instructions

1. **Open the `lab1_dag.py` file.** This file contains the barebones structure of an Airflow DAG.

2. **Implement the tasks:**
   - **`read_data`:** Replace the placeholder command with the actual command to read data from your CSV file and print the file content in logs. You can use the `BashOperator` to execute a shell command.
   - **`transform_data`:** Replace the placeholder command with the logic to filter out inactive customers. You can use the `BashOperator` or the `PythonOperator` for this task.
   - **`write_data`:** Replace the placeholder command with the command to write the processed data to a new CSV file.
   - **`change_data_format`:** Replace the placeholder command with the command to write the processed data to a new JSON file.

3. **Set up scheduling:**
   - In the `DAG` constructor, set the `schedule` parameter to a cron expression that defines how often you want the DAG to run (e.g., `@daily` to run once a day).

4. **Run the DAG:**
   - Start the Airflow web server and scheduler.
   - Go to the Airflow UI and find your DAG.
   - Trigger the DAG manually or wait for it to run according to the schedule you set.

5. **Monitor the execution:**
   - Observe the DAG's progress in the Airflow UI.
   - View the logs for each task to check for errors or debug issues.

## Tips

- Use the Airflow documentation for reference: [https://airflow.apache.org/docs/](https://airflow.apache.org/docs/)
- Experiment with different operators to see how they work.
- Don't be afraid to ask for help if you get stuck!

## Bonus Challenge

- Implement error handling to gracefully handle any failures in the pipeline.