from airflow.decorators import dag, task
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'retries': 1
}

@dag(
    dag_id="dag_with_taskflow_api",
    default_args=default_args,
    start_date=datetime(2025, 5, 5),
    schedule_interval='@daily',
    catchup=False
)
def hello_world_etl():
    
    @task(multiple_outputs=True)
    def query_mysql_v1():
        mysql_hook = MySqlHook(mysql_conn_id="mysql")
        query = """
            SELECT geolocation_zip_code_prefix, COUNT(*) AS so_lan_xuat_hien
            FROM geolocation g 
            GROUP BY geolocation_zip_code_prefix 
            HAVING COUNT(*) > 1
            LIMIT 10;
        """
        result = mysql_hook.get_records(query)
        print(f"Query geolocation table: {result}")
        return {"result": result}

    @task()
    def query_mysql_v2():
        mysql_hook = MySqlHook(mysql_conn_id="mysql")
        query = """
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
        return result

    # Gọi các task
    task1 = query_mysql_v1()
    task2 = query_mysql_v2()
    task3 = query_mysql_v2()
    task4 = query_mysql_v1()
    [task1. task2, task3] >> task4


# Khởi tạo DAG
greet_dag = hello_world_etl()
