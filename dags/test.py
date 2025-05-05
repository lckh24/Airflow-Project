from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': "khanhle",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet():
    print("Hello World")

with DAG(
    default_args=default_args,
    dag_id='first_dag',
    start_date=datetime(2025,5,5),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )
    task1
    