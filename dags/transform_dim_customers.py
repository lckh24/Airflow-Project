import pandas as pd 
from datetime import datetime, timedelta
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators

def transform_dim_customers():
    staging_operator = PostgresOperators("postgres")
    warehouse_operator = PostgresOperators("postgres")
    
    query_to_get_customer_table = f"SELECT * FROM staging.stg_customers"
    df = staging_operator.get_data_to_pd(query_to_get_customer_table)
    
    df['customer_unique_id'] = df['customer_unique_id'].astype(str)
    df['customer_zip_code_prefix'] = df['customer_zip_code_prefix'].astype(str).str.zfill(5)
    df['customer_city'] = df['customer_city'].str.title()
    df['customer_state'] = df['customer_state'].str.upper()
    
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_customers_{execution_date}.parquet', index=False)

    print("Transformed and saved data to dim_customers") 