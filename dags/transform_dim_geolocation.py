import pandas as pd 
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators

def transform_dim_geolocation():
    staging_operator = PostgresOperators('postgres')
    warehouse_operator = PostgresOperators('postgres')
    
    df = staging_operator.get_data_to_pd("SELECT * FROM staging.stg_geolocation")
    
    # transform and clean data
    df['geolocation_zip_code_prefix'] = df['geolocation_zip_code_prefix'].astype(str).str.zfill(5)
    df['geolocation_city'] = df['geolocation_city'].str.title()
    df['geolocation_state'] = df['geolocation_state'].str.upper()
    df = df.drop_duplicates(subset=['geolocation_zip_code_prefix'])
    
    # surrogate key
    df['geolocation_key'] = df.index + 1
    
    warehouse_operator = warehouse_operator.save_dataframe_to_postgres(
        df,
        "dim_geolocation",
        schema='warehouse',
        if_exists='replace'
    )
    
    print("Transformed and saved data to dim_geolocation")