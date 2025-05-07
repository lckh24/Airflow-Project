from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

from plugins.mysql_operator import MySQLOperators
from plugins.postgresql_operator import PostgresOperators

def extract_and_load_to_staging(**kwargs):
    source_operator = MySQLOperators('mysql')
    staging_operator = PostgresOperators('postgres')
    