import pandas as pd 
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators


def transform_dim_dates():
    warehouse_operator = PostgresOperators('postgres')
    
    start_date = pd.Timestamp('2016-01-01')
    end_date = pd.Timestamp('2025-12-31')
    date_range = pd.date_range(start = start_date, end = end_date)
    
    df = pd.DataFrame({
        'date_key': date_range,
        'day': date_range.day,
        'month': date_range.month,
        'year': date_range.year,
        'quarter': date_range.quarter,
        'day_of_week': date_range.dayofweek,
        'day_name': date_range.strftime('%A'),
        'month_name': date_range.strftime('%B'),
        'is_weekend': date_range.day_of_week.isin([5,6])
    })
    
    warehouse_operator.save_dataframe_to_postgres(
        df,
        'dim_dates',
        schema='warehouse',
        if_exists='replace'
    )
    
    print("Created and saved data to dim_dates")
    
