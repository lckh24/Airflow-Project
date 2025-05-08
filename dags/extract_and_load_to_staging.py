from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators

def extract_and_load_to_staging(**kwargs):
    source_operator = MySQLOperators('mysql')
    staging_operator = PostgresOperators('postgres')
    
    tables = {
        "product_category_name_translation",
        "geolocation",
        "sellers",
        "customers",
        "products",
        "orders",
        "order_items",
        "payments",
        "order_reviews"
    }
    
    for table in tables:
        df = source_operator.get_data_to_pd(f"SELECT * FROM {table}")
        staging_operator.save_dataframe_to_postgres(df, f"stg_{table}", schema="staging", if_exists="replace")
        print(f"Extracted and saved {table} from MySQL to PostgreSQL staging")
        
        
print(os.path.dirname(__file__))