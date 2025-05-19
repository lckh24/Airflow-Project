# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from plugins.postgresql_operator import PostgresOperators
# import pandas as pd 
# from datetime import datetime

# def transform_dim_products():
#     staging_operator = PostgresOperators("postgres")
#     warehouse_operator = PostgresOperators("postgres")
    
#     query_to_get_products = f"SELECT * FROM staging.stg_products"
#     query_to_get_categories = f"SELECT * FROM staging.stg_product_category_name_translation"
    
#     df_products = staging_operator.get_data_to_pd(query_to_get_products)
#     df_categories = staging_operator.get_data_to_pd(query_to_get_categories) 
#     df = pd.merge(df_products, df_categories, on='product_category_name', how='left')
    
#     df['product_category_name_english'] = df['product_category_name_english'].fillna("Unknown")
#     df['product_weight_g'] = df['product_weight_g'].fillna(0)
#     df['products_length_cm'] = df['product_length_cm'].fillna(0)
#     df['product_height_cm'] = df['product_height_cm'].fillna(0)
#     df['product_width_cm'] = df['product_width_cm'].fillna(0)
#     df['product_key'] = df.index + 1

#     # Thêm cột để theo dõi thay đổi (SCD Type 1)
#     df['last_updated'] = pd.Timestamp.now().date()
    
#     # warehouse_operator.save_dataframe_to_postgres(
#     #     df,
#     #     "dim_products",
#     #     schema="warehouse",
#     #     if_exists="replace"
#     # )
#     date = datetime.now()
#     execution_date = date.strftime("%d%b%Y")
#     df.to_parquet(f'/tmp/dim_products_{execution_date}.parquet', index=False)
#     print("Transformed and Saved data to dim_products") 
    
    