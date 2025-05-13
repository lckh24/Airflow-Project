import pandas as pd 
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.postgresql_operator import PostgresOperators

def transform_dim_order_items():
    staging_operator = PostgresOperators('postgres')
    warehouse_operator = PostgresOperators('postgres')
    
    df_order_items = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_order_items")
    df_products = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_products")
    df_categories = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_product_category_name_translation")
    df_orders = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_orders")['order_id', 'order_key']
    
    df = df_order_items.merge(df_products,on='product_id',how='left')\
                       .merge(df_categories, on='product_category_name', how='left')\
                       .merge(df_orders, on='order_id', how='left')
    
                       
    df['product_category_name_english'] = df['product_category_name_english'].fillna("Unknown")
    df['order_items_key'] = df.index + 1
    current_date = datetime.now().date()
    df['creation_date'] = current_date
    
    df_columns = ['order_items_key',
                  'product_category_name_english',
                  'price',
                  'freight_value',
                  'fk_order_id',
                  'fk_product_id'
                 ]
    
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_order_items_{execution_date}.parquet', index=False)
    print("Transformed and loaded data to dim_order_items")
    