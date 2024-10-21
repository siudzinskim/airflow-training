from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator

with DAG(
        dag_id='param_demo',
        start_date=datetime(2024, 10, 12),
        schedule=None,
        catchup=False,
        tags=['module 002', 'params'],
        params={
            "data_source": Param("table_a", enum=["table_a", "table_b"]),
            "output_format": Param("csv", enum=["csv", "json"])
        }
) as dag:
    extract_data = BashOperator(
        task_id='extract_data',
        bash_command=f'echo "Extracting data from {{ params.data_source }}"',
    )

    format_data = BashOperator(
        task_id='format_data',
        bash_command=f'echo "Formatting data as {{ params.output_format }}"',
    )

    extract_data >> format_data

with DAG(
        dag_id='param_validation_demo',
        start_date=datetime(2024, 10, 12),
        schedule=None,
        catchup=False,
        tags=['module 002', 'params'],
        params={
            "email_address": Param("test@example.com", type="string", format="idn-email", minLength=8),
            "enum": Param("foo", type="string", enum=["foo", "bar", 42]),
            "value": Param("2024", type="integer", minimum=1972, maximum=2100),
        }
) as dag:
    print_params = BashOperator(
        task_id='print_params',
        bash_command="""
            echo "Email: {{ params.email_address }}"
            echo "Enum: {{ params.enum }}"
            echo "Value: {{ params.value }}"
        """
    )
