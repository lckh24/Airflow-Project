import glob
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.postgresql_operator import PostgresOperators

def load_to_warehouse(table_name):
    
    file_pattern = f"/tmp/{table_name}_*.parquet"
    files = glob.glob(file_pattern)
    
    if not files:
        raise FileNotFoundError(f"Did not find latest {table_name}.")
    
    latest_file = max(files, key=os.path.getmtime)
    print(f"Loading latest file: {latest_file}")
    
    df = pd.read_parquet(latest_file)
    
    warehouse_operator = PostgresOperators("postgres")
    warehouse_operator.save_dataframe_to_postgres(
        df, table_name, schema='warehouse', if_exists='replace'
    )
    
    print(f"Loaded data to {table_name} successfully.") 