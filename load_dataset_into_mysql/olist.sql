-- ------------- #1 CREATE DATABASE---------------------------------------------------------------------------- 

-- CREATE DATABASE olist;
-- USE olist;

-- -------------- #2 CREATE TABLE product_category_name_translation----------------------------------------------------
CREATE TABLE product_category_name_translation (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    product_category_name VARCHAR(64) UNIQUE, 
    product_category_name_english VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------#3 CREATE TABLE geolocation------------------------------------------------------------
CREATE TABLE geolocation (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    geolocation_zip_code_prefix INT,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city NVARCHAR(64),
    geolocation_state VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------#4 CREATE TABLE sellers-------------------------------------------------------------------
CREATE TABLE sellers (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    seller_id VARCHAR(64) UNIQUE,  
    seller_zip_code_prefix INT,
    seller_city VARCHAR(64),
    seller_state VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------#5 CREATE TABLE customers-------------------------------------------------------------
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    customer_id VARCHAR(64) UNIQUE, 
    customer_unique_id VARCHAR(32),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(64),
    customer_state VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------#6 CREATE TABLE products------------------------------------------------------------
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    product_id VARCHAR(64) UNIQUE,  
    product_category_name VARCHAR(64),
    product_name_length INT,
    product_description_length FLOAT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (product_category_name) REFERENCES product_category_name_translation(product_category_name)
);

-- --------------#7 CREATE TABLE orders-------------------------------------------------------------
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    order_id VARCHAR(64) UNIQUE, 
    customer_id VARCHAR(64),
    order_status VARCHAR(32),
    order_purchase_timestamp DATE,
    order_approved_at DATE,
    order_delivered_carrier_date DATE,
    order_delivered_customer_date DATE,
    order_estimated_delivery_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- --------------#8 CREATE TABLE order_items----------------------------------------------------------
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    order_id VARCHAR(64),
    order_item_id INT,
    product_id VARCHAR(64),
    seller_id VARCHAR(64),
    shipping_limit_date DATE,
    price FLOAT,
    freight_value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- --------------#9 CREATE TABLE payments------------------------------------------------------------
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    order_id VARCHAR(64),
    payment_sequential INT,
    payment_type VARCHAR(32),
    payment_installments FLOAT,
    payment_value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- --------------#10 CREATE TABLE order_reviews------------------------------------------------------
CREATE TABLE order_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    review_id VARCHAR(64),
    order_id VARCHAR(64),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATE,
    review_answer_timestamp DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
