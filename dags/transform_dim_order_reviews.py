import pandas as pd 
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.postgresql_operator import PostgresOperators

def transform_dim_order_reviews():
    staging_operator = PostgresOperators('postgres')
    warehouse_operator = PostgresOperators('postgres')
    
    df = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_order_reviews")
    df_orders = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_orders")
    df['review_creation_date'] = pd.to_datetime(df['review_creation_date'])
    df_latest_reviews = df.sort_values('review_creation_date', ascending=False)\
                          .drop_duplicates(subset='order_id', keep='first')
    df = df.merge(df_orders, on='order_id', how='left')
    df.rename(columns={'id_x': 'id',
                       'id_y': 'fk_order_id',
                       'order_id_x': 'order_id'}, inplace=True) 
    dim_review_columns = ['id', 'fk_order_id', 'review_score']     
    df = df[dim_review_columns]
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_reviews_{execution_date}.parquet', index=False)
    print("Transformed and saved data to dim_order_reviews") 
    