import json
import requests
import pandas as pd
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


default_args = {
    'start_date': datetime(year=2021, month=6, day=20)
}


def extract_data(url: str, headers: str, ti) -> None:
    res = requests.get(url, headers=headers)
    json_data = json.loads(res.content)['articles']
    ti.xcom_push(key='extracted_data', value=json_data)


def transform_data(ti) -> None:
    data = ti.xcom_pull(key='extracted_data', task_ids=['extract_data'])[0]
    transformed_data = []
    for item in data:
        transformed_data.append({
            'SKU': item.get("sku", ""),
            'Brand Name': item['brand_name'],
            'Title': item['name'],
            'Thumbnail': f"https://img01.ztat.net/article/{item['media'][0]['path']}",
            'Price': item['price'].get("original"),
            'Product URL': f"https://www.zalando.co.uk/{item['url_key']}.html"
        })
    ti.xcom_push(key='transformed_data', value=transformed_data)


def load_data(path: str, ti) -> None:
    data = ti.xcom_pull(key='transformed_data', task_ids=['transform_data'])
    data_df = pd.DataFrame(data[0])
    data_df.to_csv(path, index=None)


with DAG(
    dag_id='zalando_workflow',
    default_args=default_args,
    schedule_interval='@daily',  # you can define crontabs aswell
    description='ETL pipeline for Zalando-UK'
) as dag:

    # Task 1 - Extract data from the API
    headers = {
        'authority': 'www.zalando.co.uk',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zalando.co.uk/mens-shoes-trainers/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,kn;q=0.6',
        'Origin': 'https://www.zalando.co.uk'
    }
    task_extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={'url': 'https://www.zalando.co.uk/api/catalog/articles?categories=shoes&limit=84&offset=0&pinned=&sort=popularity', "headers": headers}
    )

    # Task 2 - Transform the fetched data
    task_transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    # Task 3 - Load the Transformed data to CSV
    task_load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={'path': '/home/rhavel/Documentos/STUDY-PROJECTS/airflow-study/projects/shritam-airflow/Data/zalando_data.csv'}
    )

    task_extract_data >> task_transform_data >> task_load_data
