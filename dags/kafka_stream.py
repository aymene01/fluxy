from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests


default_args = {"owner": "Lokyra", "start_date": datetime(2024, 11, 3)}


def stream_data():
    res = requests.get("https://randomuser.me/api/")
    data = res.json()
    data = data["results"][0]
    print(json.dumps(data, indent=3))


with DAG(
    "user_automation",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    streaming_task = PythonOperator(
        task_id="stream_data_from_api", python_callable=stream_data
    )


stream_data()
