https://medium.com/plumbersofdatascience/key-concepts-in-apache-airflow-ee04cbdf45cc
https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html#adding-dag-and-tasks-documentation

## Docuemntar

## ocuemntar DAG

````python
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
doc_md = """
### A title for your dag
#### Purpose
Some info for your dag with how to operate it or what it interacts with
#### Notes
- Supports markdown features
- [Supports linking to external content](https://example.com/)
"""
with DAG(
    dag_id="DAG_DOC_EXAMPLE",
    doc_md=doc_md,
    schedule_interval="@daily",
    start_date=days_ago(1),
) as dag:
task_1 = DummyOperator(task_id="Task_1")
````
### DOcumentar Task

````python
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
doc_md = """
### A title for the dag task
#### Purpose
Some info for your dag with how to operate it or what it interacts with
#### Notes
- Supports markdown features
- [Supports linking to external content](https://example.com/)
"""
with DAG(
    dag_id="TASK_DOC_EXAMPLE",
    schedule_interval="@daily",
    start_date=days_ago(1),
) as dag:
task_1 = DummyOperator(task_id="Task_1", doc_md=doc_md)
````
