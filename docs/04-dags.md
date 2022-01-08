# DAGS

## Links

https://medium.com/@gsanjeewa1111/create-dag-for-data-engineering-project-b1027c85fd38

## Executar uma Dag

First check that DAG file contains valid Python code by executing the file with Python:

````
$ python airflow_tutorial.py
````

You can manually test a single task for a given execution_date with airflow test:

````
$ airflow test airflow_tutorial_v01 print_world 2021-07-01
````

This runs the task locally as if it was for 2021–07–01, ignoring other tasks and without communicating to the database.

**Scheduler e webserver**

Somente com `airflow scheduler` é que o webserver é cpaz de executar as dasg internamente na hora
