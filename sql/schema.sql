CREATE TABLE parts (
    number INTEGER,
    category VARCHAR(50),
    brand VARCHAR(50),
    sku VARCHAR(20) UNIQUE,
    weight NUMERIC(6,2),
    length NUMERIC(6,2),
    width NUMERIC(6,2),
    height NUMERIC(6,2)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    address VARCHAR(150),
    city VARCHAR(50),
    postcode VARCHAR(10)
);

CREATE TABLE orders (
    order_number VARCHAR(15) PRIMARY KEY,
    order_date DATE,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_pool VARCHAR(30),
    delivery_code VARCHAR(10),
    delivery_type VARCHAR(50),
    work_id VARCHAR(15),
    products_summary TEXT
);

CREATE TABLE order_lines (
    order_number VARCHAR(15) REFERENCES orders(order_number),
    line_number INTEGER,
    sku VARCHAR(20) REFERENCES parts(sku),
    category VARCHAR(50),
    quantity INTEGER
);


CREATE TABLE dim_date (
    date DATE PRIMARY KEY,
    day_of_week VARCHAR(10),
    month INTEGER,
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);