from __future__ import annotations

import os
import random
import shutil
import time
from glob import glob

import pendulum
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import get_current_context
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule


# Modified functions accepting subdir and data_dir
def stage_files(data_dir: str, **context):
    context = get_current_context()
    files = glob(f"{data_dir}/transactions/transactions_*.json")
    timestamp = context['ts_nodash']
    staging_base_dir = f"{data_dir}/staging/{timestamp}"
    for i in range(1, 6):
        subdir = os.path.join(staging_base_dir, str(i))
        os.makedirs(subdir, exist_ok=True)
    for i, file in enumerate(files):
        subdir = os.path.join(staging_base_dir, str((i % 5) + 1))
        shutil.move(file, subdir)


def merge_data(subdir_id: str, data_dir: str, **context):
    print(f"Merging data in subdir: {subdir_id}")
    time.sleep(random.randint(60, 120))
    # ... (Your merge logic for files in subdir) ...


def denormalize_data(subdir_id: str, data_dir: str, **context):
    print(f"Denormalizing data in subdir: {subdir_id}")
    time.sleep(random.randint(60, 120))
    # ... (Your denormalize logic for files in subdir) ...


def archive_files(subdir_id: str, data_dir: str, **context):
    print(f"Archiving files from subdir: {subdir_id}")
    context = get_current_context()
    timestamp = context['ts_nodash']
    staging_base_dir = f"{data_dir}/staging/{timestamp}"
    subdir_path = os.path.join(staging_base_dir, str(subdir_id))
    processed_dir = f"{data_dir}/processed/{timestamp}"
    os.makedirs(processed_dir, exist_ok=True)
    print(f'files to be archived:{glob(f"{subdir_path}/*")}')

    for file in glob(f"{subdir_path}/*"):
        print(f"Moving: {file} to {processed_dir}")
        shutil.move(file, processed_dir)


@dag(
    dag_id='lab6_parallel_processing_taskflow',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    params={"data_dir": "/opt/airflow/data"},
    tags=['lab6', 'parallel_processing', 'dynamic_taskgroups', 'taskflow'],
)
def lab6_parallel_processing_taskflow():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ALL_DONE)

    check_for_files = FileSensor(
        task_id='check_for_files',
        filepath='{{ params.data_dir }}/transactions/*.json',
        poke_interval=5
    )

    files_does_not_exist = EmptyOperator(
        task_id="files_does_not_exist",
        trigger_rule=TriggerRule.ALL_FAILED
    )

    files_exist = EmptyOperator(
        task_id="files_exist",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    @task(task_id="stage_files")
    def stage_files_taskflow(**context):
        stage_files(data_dir=context["params"]["data_dir"])

    merged = {}
    denormalized = {}
    archived = {}
    for i in range(1, 6):
        with TaskGroup(group_id=f"processing_group_{i}") as processing_group:
            @task(task_id=f"merge_{i}")
            def merge_data_taskflow(subdir):
                context = get_current_context()
                data_dir = context["params"]["data_dir"]
                timestamp = context['ts_nodash']
                staging_base_dir = f"{data_dir}/staging/{timestamp}"
                subdir = os.path.join(staging_base_dir, str(i))
                merge_data(subdir_id=subdir, data_dir=data_dir)
                return subdir

            @task(task_id=f"denormalize_{i}")
            def denormalize_data_taskflow(subdir):
                context = get_current_context()
                data_dir = context["params"]["data_dir"]
                timestamp = context['ts_nodash']
                staging_base_dir = f"{data_dir}/staging/{timestamp}"
                subdir = os.path.join(staging_base_dir, str(i))
                denormalize_data(subdir_id=subdir, data_dir=data_dir)
                return subdir

            @task(task_id=f"archive_{i}")
            def archive_files_taskflow(subdir):
                context = get_current_context()
                data_dir = context["params"]["data_dir"]
                timestamp = context['ts_nodash']
                staging_base_dir = f"{data_dir}/staging/{timestamp}"
                subdir = os.path.join(staging_base_dir, str(i))
                archive_files(subdir_id=subdir, data_dir=data_dir)

            merged[i] = merge_data_taskflow(i)
            denormalized[i] = denormalize_data_taskflow(i)
            archived[i] = archive_files_taskflow(i)

    start >> check_for_files >> [files_exist, files_does_not_exist]
    files_exist >> stage_files_taskflow() >> end
    files_does_not_exist >> end


lab6_parallel_processing_taskflow()
