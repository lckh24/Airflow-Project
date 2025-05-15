import pandas as pd 
import os 
import sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators

def transform_dim_order_items():
    staging_operator = PostgresOperators("postgres")
    warehouse_operator = PostgresOperators("postgres")
    
    df_order_items = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_order_items")
    df_products = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_products")
    df_categories = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_product_category_name_translation")
    df_orders = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_orders")[['id', 'order_id']] 
    df = df_order_items.merge(df_products,on='product_id',how='left')
    df.rename(columns={'id_x': 'id',
                   'id_y': 'fk_product_id'}, inplace=True)
    df = df.merge(df_categories, on='product_category_name', how='left')
    df.rename(columns={'id_y': 'fk_product_category_name_id',
                       'id_x': 'id'}, inplace=True)         
    df = df.merge(df_orders, on='order_id', how='left')
    df.rename(columns={'id_x': 'id',
                       'id_y': 'fk_order_id',
                       'order_id_x': 'order_id'}, inplace=True)          
    df['product_category_name_english'] = df['product_category_name_english'].fillna("Unknown")
    df_columns = ['id',
                  'fk_product_id',
                  'fk_order_id',
                  'product_category_name_english',
                  'order_item_id',
                  'order_status',
                  'price',
                  'freight_value'
                 ]
    df = df[df_columns]
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_order_items_{execution_date}.parquet', index=False)
    print("Transformed and loaded data to dim_order_items")