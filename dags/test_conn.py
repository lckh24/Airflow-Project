from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.hooks.base import BaseHook
from datetime import datetime

def test_mysql_conn():
    conn = BaseHook.get_connection("mysql")
    print("Host:", conn.host)
    print("Schema:", conn.schema)
    

def query_mysql():
    # Tạo kết nối MySQL và thực thi câu truy vấn
    mysql_hook = MySqlHook(mysql_conn_id="mysql_db")
    query = f"""SELECT geolocation_zip_code_prefix, COUNT(*) AS so_lan_xuat_hien
                FROM geolocation g 
                GROUP BY geolocation_zip_code_prefix 
                HAVING COUNT(*) > 1
                LIMIT 10;"""
    result = mysql_hook.get_records(query)
    if result:
        print(result)
    else:
        print("No records found.")

    
    

with DAG("test_mysql_connection",
         start_date=datetime(2024, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:
    # task1 = PythonOperator(
    #     task_id="test_conn",
    #     python_callable=test_mysql_conn
    # )
    
    task2 = PythonOperator(
        task_id="query_mysql",
        python_callable=query_mysql
    )
    
    task2
    
    
