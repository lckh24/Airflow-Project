from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': "khanhle",
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    print(f"Hello World! My name is {first_name} {last_name}, and I am {age} years old!")

def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridman')

with DAG(
    default_args=default_args,
    dag_id='first_dag',
    start_date=datetime(2025,5,5),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 20}
    )
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task2 >> task1
    