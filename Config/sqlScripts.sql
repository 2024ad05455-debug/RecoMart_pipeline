--ALTER USER postgres WITH PASSWORD 'Dmml123';--

CREATE DATABASE "RecoMart_DB";

CREATE TABLE ecommerce_events (
    event_time TIMESTAMP,
    event_type VARCHAR(20),
    product_id BIGINT,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand VARCHAR(100),
    price NUMERIC(10,2),
    user_id BIGINT,
    user_session UUID
);



CREATE DATABASE "RecoMart_DB";

CREATE TABLE ecommerce_events (
    event_time TIMESTAMP,
    event_type VARCHAR(20),
    product_id BIGINT,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand VARCHAR(100),
    price NUMERIC(10,2),
    user_id BIGINT,
    user_session UUID
);

SELECT COUNT(*) FROM ecommerce_events;
SELECT * FROM ecommerce_events;


CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title TEXT,
    brand TEXT,
    category TEXT,
    price NUMERIC(10,2),
    rating NUMERIC(3,2),
    stock INTEGER
);

SELECT COUNT(*) FROM ecommerce_events;
SELECT * FROM products;



