import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.postgresql_operator import PostgresOperators
import pandas as pd 
from datetime import datetime

def transform_dim_sellers():
    staging_operator = PostgresOperators('postgres')
    warehouse_operator = PostgresOperators('postgres')
    
    # Đọc dữ liệu từ staging
    df = staging_operator.get_data_to_pd("SELECT * FROM staging.stg_sellers")
    
    df['seller_zip_code_prefix'] = df['seller_zip_code_prefix'].astype(str).str.zfill(5)
    df['seller_city'] = df['seller_city'].astype(str).str.title()
    df['seller_state'] = df['seller_state'].str.upper()
    df['seller_key'] = df.index + 1
    # SCD Type 1
    df['last_updated'] = pd.Timestamp.now().date()
    df.rename(columns={'seller_id': 'used_id'}, inplace=True)
    # warehouse_operator.save_dataframe_to_postgres(
    #     df,
    #     'dim_sellers',
    #     schema='warehouse',
    #     if_exists='replace'
    # )
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_sellers_{execution_date}.parquet', index=False)
    print("Transformed and saved data to dim_sellers")