----------------#1 CREATE STAGING SCHEMA----------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS staging;


----------------#2 CREATE TABLE FOR STAGING SCHEMA----------------------------------------------------------------------------

-- Table product_category_name_translation
CREATE TABLE IF NOT EXISTS staging.product_category_name_translation (
    id SERIAL PRIMARY KEY,
    product_category_name varchar(64) UNIQUE,
    product_category_name_english varchar(64)
);

-- Table geolocation
CREATE TABLE IF NOT EXISTS staging.geolocation (
    id SERIAL PRIMARY KEY,
    geolocation_zip_code_prefix INT,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city NVARCHAR(64),
    geolocation_state VARCHAR(64)
);

-- Table sellers
CREATE TABLE IF NOT EXISTS staging.sellers (
    id SERIAL PRIMARY KEY,
    seller_id varchar(64) UNIQUE,
    seller_zip_code_prefix INT,
    seller_city varchar(64),
    seller_state varchar(64)
);

-- Table customers
CREATE TABLE IF NOT EXISTS staging.customers (
    id SERIAL PRIMARY KEY,
    customer_id varchar(64) UNIQUE,
    customer_unique_id varchar(32),
    customer_zip_code_prefix INT,
    customer_city varchar(64),
    customer_state varchar(64)
);

-- Table products
CREATE TABLE IF NOT EXISTS staging.products (
    id SERIAL PRIMARY KEY,
    product_id varchar(64) UNIQUE,
    product_category_name varchar(64),
    product_name_length int,
    product_description_length FLOAT,
    product_photos_qty int,
    product_weight_g int,
    product_length_cm float,
    product_height_cm float,
    product_width_cm float,
    FOREIGN KEY (product_category_name) REFERENCES staging.product_category_name_translation(product_category_name)
);

-- Table orders
CREATE TABLE IF NOT EXISTS staging.orders (
    id SERIAL PRIMARY KEY,
    order_id varchar(64) UNIQUE,
    customer_id varchar(64),
    order_status varchar(32),
    order_purchase_timestamp date,
    order_approved_at date,
    order_delivered_carrier_date date,
    order_delivered_customer_date date,
    order_estimated_delivery_date date,
    FOREIGN KEY (customer_id) REFERENCES staging.customers(customer_id)
);

-- Table order_items
CREATE TABLE IF NOT EXISTS staging.order_items (
    id SERIAL PRIMARY KEY,
    order_id varchar(64),
    order_item_id int,
    product_id varchar(64),
    seller_id varchar(64),
    shipping_limit_date date,
    price float,
    freight_value float,
    FOREIGN KEY (product_id) REFERENCES staging.products(product_id),
    FOREIGN KEY (order_id) REFERENCES staging.orders(order_id),
    FOREIGN KEY (seller_id) REFERENCES staging.sellers(seller_id)
);

-- Table payments
CREATE TABLE IF NOT EXISTS staging.payments (
    id SERIAL PRIMARY KEY,
    order_id varchar(64),
    payment_sequential int,
    payment_type varchar(32),
    payment_installments float,
    payment_value float,
    FOREIGN KEY (order_id) REFERENCES staging.orders(order_id)
);

-- Table order_reviews
CREATE TABLE IF NOT EXISTS staging.order_reviews (
    id SERIAL PRIMARY KEY,
    review_id varchar(64),
    order_id varchar(64),
    review_score int,
    review_comment_title text,
    review_comment_message text,
    review_creation_date date,
    review_answer_timestamp date,
    FOREIGN KEY (order_id) REFERENCES staging.orders(order_id)
);
