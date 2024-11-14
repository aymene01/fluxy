from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests


default_args = {"owner": "Lokyra", "start_date": datetime(2024, 11, 3)}


def get_data():
    res = requests.get("https://randomuser.me/api/")
    data = res.json()
    data = data["results"][0]
    return data

def format_data(res):
    data = {}
    location = res["location"]
    data["first_name"] = res["name"]["first"]
    data["last_name"] = res["name"]["last"]
    data["gender"] = res["gender"]
    data["address"] = (
        f"{str(location['street']['number'])} {location['street']['name']}, "
        f"{location['city']}, {location['state']}, {location['country']}"
    )
    data["postcode"] = location["postcode"]
    data["email"] = res["email"]
    data["username"] = res["login"]["username"]
    data["dob"] = res["dob"]["date"]
    data["registered_date"] = res["registered"]["date"]
    data["phone"] = res["phone"]
    data["picture"] = res["picture"]["medium"]

    return data


def stream_data():
    res = get_data()
    data = format_data(res)
    print(json.dumps(data, indent=3))


dag = DAG(
    "user_automation",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

stream_data_task = PythonOperator(
    task_id="stream_data",
    python_callable=stream_data,
    dag=dag,
)
