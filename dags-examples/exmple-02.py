# source: https://medium.com/@gsanjeewa1111/create-dag-for-data-engineering-project-b1027c85fd38

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import datetime as dt

def print_world():
    print('world')


default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 6, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('airflow_tutorial_v01',
         default_args=default_args,
         schedule_interval='0 * * * *',
         ) as dag:

	# task 1
    print_hello = BashOperator(task_id='print_hello',
                               bash_command='echo "hello"')
	# task 2
    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 5')
	# task 3
    print_world = PythonOperator(task_id='print_world',
                                 python_callable=print_world)

# Order to exec Dag
print_hello >> sleep >> print_world
