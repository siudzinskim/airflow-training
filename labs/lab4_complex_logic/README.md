# Lab 4: Sensors, XComs, Branching, and Data Processing with Airflow

## Objective

This lab will teach you how to build a robust and idempotent data pipeline using Airflow, incorporating sensors, XComs for inter-task communication, branching, and a series of data processing steps.

## Scenario

You are tasked with building an ETL pipeline for an online retail store. The pipeline processes transaction data, enriches it with customer information, and stores the processed data for analysis.  The data pipeline should be idempotent and optimized using staging to allow reruns.

- **Data Sources:**
    - Transaction data is generated by a separate process (Lab 2's DAG) and stored as newline-delimited JSON files in the `data/transactions/` directory, named `transactions_*.json`.
    - Customer information is stored in a CSV file: `data/customers.csv`.
- **Pipeline Trigger:** The pipeline should run every minute.
- **File Sensor:** The pipeline starts with a file sensor that checks for the presence of new `transactions_*.json` files in the `data/transactions/` directory. If no new files are found in 30 seconds, the pipeline skips the subsequent processing steps.
- **Batch Processing and Idempotence:** The pipeline is designed for batch processing to optimize performance and handle multiple transaction files efficiently and in an idempotent manner.  A staging directory `data/staging/{{ts}}/` using an execution timestamp (`{{ts}}`) ensures data is only loaded once, even if tasks are rerun.
- **Processing Steps:**
    1. **List Files:** List all `transactions_*.json` files in the `data/transactions/` directory and push the list of filenames to XCom.
    2. **Multiple Files Check:** Check if there's more than one transaction file.  If so, send a Slack notification (requires a Slack webhook configuration).
    3. **Stage Files:** Move the listed files from `data/transactions/` to the `data/staging/{{ts}}/` directory.
    4. **Merge with Customer Data:**  Merge the staged transaction data with the `data/customers.csv` file.  Store the enriched data as newline-delimited JSON in `data/customer_transactions/customer_transactions_{{ts}}.json`.
    5. **Denormalize Data:** Denormalize the enriched JSON data into a CSV file named `data/customer_transactions_denormalized/customer_transactions_denormalized_{{ts}}.csv`.
    6. **Archive Processed Files:** Move the processed transaction files from `data/staging/{{ts}}/` to `data/processed/`. Add a timestamp suffix (`.{{ts}}`) to the original filenames to maintain a history of processed files.

## Instructions

1. **Configure Slack Webhook (Optional):** If you want to use the Slack notification feature, configure a Slack webhook and set the webhook URL as an Airflow variable or connection.

1. **Create the DAG (`lab4_dag.py`):**  Implement the DAG to perform the steps described above.  Use the following operators:
    - `FileSensor`: To check for new transaction files.
    - `PythonOperator`: For listing files, moving files, merging data, denormalizing data, sending Slack notifications.
    - `BashOperator`: Can also be used for file system operations if preferred.
    - `BranchPythonOperator`:  To conditionally send a Slack notification.
    - `EmptyOperator`: To mark the start and end of the DAG.

1. **Implement XComs:** Use `xcom_push` to send data between tasks and `xcom_pull` to retrieve XCom values.

1. **Implement Branching Logic:** Use the `BranchPythonOperator` to determine whether to send a Slack notification based on the number of transaction files.

1. **File System Operations**: Implement file listing, renaming, moving files for idempotent load process using temporary `data/staging` directory.

1. **Run the DAG:** Upload your DAG to Airflow and trigger a DAG run.

## Tips:

- Use clear and descriptive task IDs and XCom keys.
- Implement comprehensive error handling and logging.
- Slack webhook is a paid option, so we will use a simulated webhook receiver: https://webhook.site/


## Bonus Challenge

- clean up the staging directory after processing all the files