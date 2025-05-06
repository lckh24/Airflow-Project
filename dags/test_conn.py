from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime

def test_mysql_conn():
    conn = BaseHook.get_connection("mysql")
    print("Host:", conn.host)
    print("Schema:", conn.schema)

with DAG("test_mysql_connection",
         start_date=datetime(2024, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:
    task = PythonOperator(
        task_id="test_conn",
        python_callable=test_mysql_conn
    )
    task