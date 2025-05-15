import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.postgresql_operator import PostgresOperators

def transform_fact_orders():
    staging_operator = PostgresOperators('postgres')
    warehouse_operator = PostgresOperators('postgres')
    
    df = staging_operator.get_data_to_pd("SELECT * FROM staging.stg_orders")
    df_customer = staging_operator.get_data_to_pd("SELECT * FROM staging.stg_customers")
    df_order_items = staging_operator.get_data_to_pd("SELECT * FROM staging.stg_order_items")
    df_order_payments = staging_operator.get_data_to_pd("SELECT * FROM staging.stg_payments")
    
    df = df.merge(df_customer, on='customer_id', how='left')
    
    df.rename(columns={"id_x": "id", "id_y": "fk_customer_id"}, inplace=True)
    
    order_payments_agg = df_order_payments.groupby('order_id').agg({
        'payment_value': 'sum',
        'payment_installments': 'max',
    }).reset_index()
    
    df = df.merge(order_payments_agg, left_on='order_id', right_on='order_id', how='left')
    
    order_items_agg = df_order_items.groupby(['order_id']).agg({
        'price': 'sum',
        'freight_value': 'sum'
    }).reset_index().rename(columns={
        'price': 'total_price',
        'freight_value': 'total_freight'
    })
    order_items_agg['total_amount'] = order_items_agg['total_price'] + order_items_agg['total_freight']
    df = df.merge(order_items_agg, left_on='order_id', right_on='order_id', how='left')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    
    # Tính toán thời gian giao hàng (delivery_time) và thời gian theo ngày (order_date_key)
    df['delivery_time'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.total_seconds() / 86400
    df['order_date_key'] = df['order_purchase_timestamp'].dt.date
    
    fact_columns = ['id', 'order_id','order_status', 'payment_value', 'total_amount', 'delivery_time', 'order_date_key', 'fk_customer_id']
    df_fact = df[fact_columns]

    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    file_path = f'/tmp/fact_orders_{execution_date}.parquet'
    df_fact.to_parquet(file_path, index=False)
    
    print(f"Transformed and saved data to {file_path}")
    
transform_fact_orders()
