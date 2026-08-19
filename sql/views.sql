CREATE VIEW dim_parts AS
SELECT
    sku AS part_sku,
    number AS part_number,
    category,
    brand,
    weight,
    length,
    width,
    height
FROM parts;

CREATE VIEW dim_customers AS
SELECT
    customer_id,
    customer_name,
    address,
    city,
    postcode
FROM customers;

CREATE VIEW dim_orders AS
SELECT
    order_number,
    order_date,
    customer_id,
    order_pool,
    delivery_code,
    delivery_type,
    work_id,
    products_summary
FROM orders;

CREATE VIEW fact_order_lines AS
SELECT
    order_number,
    line_number,
    sku AS part_sku,
    quantity
FROM order_lines;