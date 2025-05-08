from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.decorators import dag, task, task_group
from datetime import datetime, timedelta

import os 
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from transform_dim_customers import transform_dim_customers
from transform_dim_products import transform_dim_products
from transform_dim_sellers import transform_dim_sellers
from transform_dim_geolocation import transform_dim_geolocation
from transform_dim_dates import transform_dim_dates
from transform_dim_payments import transform_dim_payments
from transform_fact_orders import transform_fact_orders
from extract_and_load_to_staging import extract_and_load_to_staging
from load_to_warehouse import load_to_warehouse

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025,5,8),
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

@task_group(group_id="extract")
def extract_group():
    return PythonOperator(
        task_id="extract_and_load_to_staging",
        python_callable=extract_and_load_to_staging,
        provide_context=True,
    )

@task_group(group_id="transform")
def transform_group():
    PythonOperator(task_id="transform_dim_customers", python_callable=transform_dim_customers)
    PythonOperator(task_id="transform_dim_products", python_callable=transform_dim_products)
    PythonOperator(task_id="transform_dim_sellers", python_callable=transform_dim_sellers)
    PythonOperator(task_id="transform_dim_geolocation", python_callable=transform_dim_geolocation)
    PythonOperator(task_id="transform_dim_dates", python_callable=transform_dim_dates)
    PythonOperator(task_id="transform_dim_payments", python_callable=transform_dim_payments)
    PythonOperator(task_id="transform_fact_orders", python_callable=transform_fact_orders)

@task_group(group_id="load")
def load_group():
    PythonOperator(task_id="load_dim_customers", python_callable=load_to_warehouse)
    
    
@dag(
    dag_id="e_commerce_dw_etl_decorator",
    default_args=default_args,
    description="ETL process for E-commerce Data Warehouse using decorators",
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=["etl", "ecommerce"]
)
def etl_pipeline():
    extract = extract_group()
    transform = transform_group()
    load = load_group()
    extract >> transform >> load
    
dag = etl_pipeline()