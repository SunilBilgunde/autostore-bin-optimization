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

CREATE VIEW velocity_by_sku AS
SELECT
    p.brand,
    p.category,
    p.part_sku,
    COUNT(*) AS pick_events
FROM fact_order_lines f
JOIN dim_parts p ON f.part_sku = p.part_sku
GROUP BY p.brand, p.category, p.part_sku;

CREATE VIEW slotting_recommendation AS
WITH ranked AS (
    SELECT
        part_sku,
        brand,
        category,
        pick_events,
        NTILE(5) OVER (ORDER BY pick_events DESC) AS velocity_tier
    FROM velocity_by_sku
)
SELECT
    part_sku,
    brand,
    category,
    pick_events,
    velocity_tier,
    CASE
        WHEN velocity_tier = 1 THEN 'Fast-Access'
        WHEN velocity_tier IN (2, 3) THEN 'Standard'
        ELSE 'Deep-Storage'
    END AS slotting_zone
FROM ranked;