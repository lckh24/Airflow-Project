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
    
    df['payment_type'] = df['payment_type'].str.lower()
    df['payment_installments'] = df['payment_installments'].fillna(1).astype(int)
    df['payment_key'] = df.index + 1
    
    # warehouse_operator.save_data_to_postgres(
    #     df,
    #     "dim_payments",
    #     schema='warehouse',
    #     if_exists='replace'
    # )
    date = datetime.now()
    execution_date = date.strftime("%d%b%Y")
    df.to_parquet(f'/tmp/dim_payments_{execution_date}.parquet', index=False)
    print("Transformed and loaded data to dim_payments")
    