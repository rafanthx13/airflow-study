
## alert por sms/email do airflow pra attlasian

https://medium.com/unruly-engineering/quick-easy-alerting-for-apache-airflow-53c3f1ba2ca

É possível usar APache Airflow junto de  Atalssian (opsgenie) para que, quando uma task der erro, mandar um email pra gente.

Usamos uma configuraçao da task/dag `on_failure_callback`

````python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from an_opsgenie_hook import opsgenie_hook

dag = DAG('eternal_failure')

task_that_always_fails = BashOperator(
    task_id='task_that_always_fails',
    bash_command='exit 1',
    on_failure_callback=opsgenie_hook,
    dag=dag,
)
````

e por `on_failure_callback` chaamaos o seguinte hook de outo arquivo

````python
from airflow.contrib.hooks.opsgenie_alert_hook import OpsgenieAlertHook

def opsgenie_hook(context):
    dag = context.get('task_instance').dag_id,
    task = context.get('task_instance').task_id,
    ts = context.get('ts'),
    log_url = context.get('task_instance').log_url

    date_time = dateutil.parser.parse(ts[0])

    message = "Airflow DAG {}, failed to run {}, scheduled at {}.".format(dag[0], task[0], date_time.strftime('%Y-%m-%d %H:%M'))

    json = {
        "message": message,
        "description": message,
        "responders": [
            {
                "id": "SOME-TEAM-ID-HERE",
                "type": "team"
            }
        ],
        "tags": [
            "Data Engineering",
            "Airflow"
        ],
        "details": {
            "Logs": log_url.replace("localhost", "YOUR-AIRFLOW-DNS")
        },
        "priority": "P3"
    }
    
    hook = OpsgenieAlertHook('opsgenie_default')
    hook.execute(json)
````

## test unitario

https://levelup.gitconnected.com/airflow-unit-testing-for-bug-free-data-pipeline-d96f87a3cc8f
