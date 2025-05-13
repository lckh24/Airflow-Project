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
    df['review_creation_date'] = pd.to_datetime(df['review_creation_date'])
    df_latest_reviews = df.sort_values('review_creation_date', ascending=False)\
                          .drop_duplicates(subset='order_id', keep='first')
    dim_review_key = df_latest_reviews.index + 1
    dim_review_columns = ['order_id', 'review_score']     
    
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_reviews_{execution_date}.parquet', index=False)
    print("Transformed and saved data to dim_order_reviews")
    