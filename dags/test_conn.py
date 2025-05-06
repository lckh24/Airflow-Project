from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.hooks.base import BaseHook
from datetime import datetime

def test_mysql_conn():
    conn = BaseHook.get_connection("mysql")
    print("Host:", conn.host)
    print("Schema:", conn.schema)
    

def query_mysql_v1():
    # Tạo kết nối MySQL và thực thi câu truy vấn
    mysql_hook = MySqlHook(mysql_conn_id="mysql")
    query = f"""SELECT geolocation_zip_code_prefix, COUNT(*) AS so_lan_xuat_hien
                FROM geolocation g 
                GROUP BY geolocation_zip_code_prefix 
                HAVING COUNT(*) > 1
                LIMIT 10;"""
    result = mysql_hook.get_records(query)
    print(f"Query geolocation table: {result}")

def query_mysql_v2():
    mysql_hook = MySqlHook(mysql_conn_id="mysql")
    query = f"""
        SELECT 
            oi.order_id,
            o.customer_id,
            oi.product_id,
            o.order_status,
            oi.price
        FROM order_items oi
        LEFT JOIN orders o 
        ON oi.order_id = o.order_id
        """
    result = mysql_hook.get_records(query)
    print(f"Query order and order_item table: {result}")

    

with DAG("test_mysql_connection",
         start_date=datetime(2024, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:
    task1 = PythonOperator(
        task_id="query_mysql_v1",
        python_callable=query_mysql_v1
    )
    
    task2 = PythonOperator(
        task_id="query_mysql_v2",
        python_callable=query_mysql_v2
    )
    
    task1 >> task2
    
    
