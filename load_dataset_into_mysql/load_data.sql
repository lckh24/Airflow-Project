-- 1. product_category_name_translation.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/product_category_name_translation.csv'
INTO TABLE product_category_name_translation
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_category_name, product_category_name_english);

-- 2. olist_geolocation_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_geolocation_dataset.csv'
INTO TABLE geolocation
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state);

-- 3. olist_sellers_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_sellers_dataset.csv'
INTO TABLE sellers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(seller_id, seller_zip_code_prefix, seller_city, seller_state);

-- 4. olist_customers_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_customers_dataset.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state);

-- 5. olist_products_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_products_dataset.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm);

-- 6. olist_orders_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_orders_dataset.csv'
INTO TABLE orders
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date);

-- 7. olist_order_items_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_order_items_dataset.csv'
INTO TABLE order_items
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value);

-- 8. olist_order_payments_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_order_payments_dataset.csv'
INTO TABLE payments
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, payment_sequential, payment_type, payment_installments, payment_value);

-- 9. olist_order_reviews_dataset.csv
LOAD DATA LOCAL INFILE '/tmp/dataset/olist_order_reviews_dataset.csv'
INTO TABLE order_reviews
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp);