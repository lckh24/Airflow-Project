import os
import sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.postgresql_operator import PostgresOperators

def transform_dim_payments():
    staging_operator = PostgresOperators("postgres")
    warehouse_operator = PostgresOperators("postgres")
    
    query_to_get_payment_table = f"SELECT * FROM staging.stg_payments"
    df = staging_operator.get_data_to_pd(query_to_get_payment_table)
    df_orders = staging_operator.get_data_to_pd(f"SELECT * FROM staging.stg_orders")
    
    df['payment_type'] = df['payment_type'].str.lower()
    df['payment_installments'] = df['payment_installments'].fillna(1).astype(int)
    
    # warehouse_operator.save_data_to_postgres(
    #     df,
    #     "dim_payments",
    #     schema='warehouse',
    #     if_exists='replace'
    # )
    
    df = df.merge(df_orders, on='order_id', how='left')
    df.rename(columns={'id_x': 'id',
                       'id_y': 'fk_order_id',
                       'order_id_x': 'order_id'}, inplace=True)    
    
    columns_to_keep = ["id", "fk_order_id", "payment_installments", "payment_type"]
    df = df[columns_to_keep]
    print(df.columns)
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_payments_{execution_date}.parquet', index=False)
    print("Transformed and loaded data to dim_payments") 
    