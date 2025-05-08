from datetime import datetime

string = 'dim_customer_20Nov2025.parquet'
string = string.split('_')
print(string[0] + "_" + string[1])