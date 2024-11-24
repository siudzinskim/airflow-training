# Lab 6: Parallel Processing with Dynamic TaskGroups in Airflow (TaskFlow)

This lab elevates the data pipeline from Lab 4 by implementing parallel processing using dynamic TaskGroups and the TaskFlow API. You will dynamically create five TaskGroups, each dedicated to processing files within a specific subdirectory, maximizing processing efficiency.

## Objective

Refactor the Lab 4 DAG to utilize the TaskFlow API and process files concurrently across five dynamically generated TaskGroups, each operating on a distinct subdirectory within the staging area.

## Task

1.  **Dynamic Subdirectories (Staging):** The `stage_files` task will create five subdirectories (`1` to `5`) within the staging directory and distribute files evenly amongst them.
2.  **Dynamic TaskGroup Generation:**  Five TaskGroups will be created dynamically, corresponding to each subdirectory.
3.  **Parallel Processing:**  The processing tasks (`merge_data`, `denormalize_data`, and `archive_files`) will be executed within each TaskGroup, processing files in their respective subdirectories concurrently.


## Instructions

1.  **TaskFlow Decorators:** Use the `@dag` decorator to define the DAG and the `@task` decorator for all tasks including `stage_files`, `create_dynamic_taskgroups`, `merge_data`, `denormalize_data`, and `archive_files`.
2.  **Modify `stage_files`:** Adapt `stage_files` to create five subdirectories within the staging directory and distribute files evenly into them.  Use the `data_dir` parameter and the execution timestamp to construct paths.
3.  **Create Dynamic TaskGroups:** Create a task using `@task` which handles creating dynamic taskgroups. Within this task, use a loop to iterate five times (for each subdirectory).  Inside each iteration, create a TaskGroup using `with TaskGroup(...)`.
4.  **Implement Processing Tasks (within TaskGroups):** Within each TaskGroup, implement `merge_data`, `denormalize_data`, and `archive_files` as TaskFlow tasks using the `@task` decorator. These tasks should accept `subdir` and `data_dir` as parameters to operate on the correct files within each subdirectory.
5.  **Set Dependencies (within and between TaskGroups):** Establish correct task order between the staging task and the dynamic TaskGroup creation task.  Also, set dependencies between tasks within each TaskGroup.
6.  **Set Concurrency:** Configure the DAG's `concurrent_tasks` parameter to `5` to allow parallel execution of the TaskGroups.