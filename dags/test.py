from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': "khanhle",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(name, age):
    print(f"Hello World! My name is {name}, and I am {age} years old!")

def get_name():
    return "Jerry"

with DAG(
    default_args=default_args,
    dag_id='first_dag',
    start_date=datetime(2025,5,5),
    schedule_interval='@daily'
) as dag:
    # task1 = PythonOperator(
    #     task_id='greet',
    #     python_callable=greet,
    #     op_kwargs={'name': 'Tom', 'age': 20}
    # )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task2
    