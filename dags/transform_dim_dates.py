import pandas as pd 
import os 
import sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators


def transform_dim_dates():
    staging_operator = PostgresOperators('postgres')
    df = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_orders")
    df['order_status'] = df['order_status'].str.lower()
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_estimated_delivery_date']
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    
    columns_to_keep = ['id', 'order_id', 'order_purchase_timestamp', 'order_estimated_delivery_date', 'order_delivered_customer_date', 'order_status']
    df = df[columns_to_keep]
    # warehouse_operator.save_dataframe_to_postgres(
    #     df,
    #     'dim_dates',
    #     schema='warehouse',
    #     if_exists='replace'
    # )
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_dates_{execution_date}.parquet', index=False)
    print("Created and saved data to dim_dates")
    
