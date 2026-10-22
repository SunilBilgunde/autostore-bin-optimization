# AutoStore Bin Optimization Pipeline

An end-to-end data engineering project built around a synthetic AutoStore
warehouse setup. It generates a realistic parts catalog and order data,
with the eventual goal of analyzing and optimizing bin placement based on
how often parts actually get ordered.

Scaled roughly in line with real AutoStore deployments — around 60k bins,
40 robots, 10 ports.

## Status

Phases 1-4 are done: data generation, loading into PostgreSQL,
transformation in SQL, and orchestration with Airflow.

- `generate_skus.py` builds a catalog of ~500 parts across three fictional
  brands, each with a realistic weight and set of dimensions based on
  actual AutoStore bin size/weight limits.
- `generate_orders.py` builds a pool of recurring customers plus order and
  order-line data on top of the catalog. Quantities are weighted by part
  category, orders only fall on weekdays, and customer/address data uses
  UK formatting.
- `build_dim_date.py` builds the date dimension (Jan-Jun 2026).
- `load_to_postgres.py` loads everything into PostgreSQL, with primary
  keys, unique constraints, and foreign keys linking order lines back to
  both orders and parts. It clears the tables first, so it can be re-run
  safely. DB credentials are kept in a `.env` file, not in the repo.
- `dags/autostore_pipeline.py` is the Airflow DAG that chains it all
  together: generate parts, then orders (with the date table built in
  parallel), then load. Airflow runs in Docker via `docker-compose.yaml`.
- `sql/schema.sql` has the full table structure.
- `sql/views.sql` builds a star schema on top of the raw tables
  (`fact_order_lines`, `dim_parts`, `dim_customers`, `dim_orders`,
  `dim_date`), plus the actual analysis: a velocity view counting how
  often each part gets picked, a slotting recommendation view that
  buckets every part into Fast-Access / Standard / Deep-Storage zones
  based on pick frequency, a bin capacity view (weight and volume
  constraints, with a 65% packing-efficiency assumption), and a
  `final_slotting_plan` view combining velocity and capacity into a
  single restock-priority ranking — the project's core output.

## Key Finding

Combining pick frequency with bin capacity reveals something that 
popularity alone misses: Brake Discs dominate the restock-estimates 
at aboout 17 estimated trips per SKU, against roughly 1-3 for the 
Control arms and steering kits (around 7-8 trips) follow for a similar reason: bulky parts that fit few to a bin.
The pattern is driven by bin capacity more than by pick  frequency alone.

This estimate assumes a bin depletes fully before refilling, which is a
simplification — real replenishment usually triggers at a threshold, not
at zero. Still, it's a useful directional signal for where bin capacity
planning matters most.

A second issue surfaced while validating `dim_date`: order dates were
originally generated uniformly across every calendar day, including
weekends — but the warehouse only operates Monday-Friday. Roughly 29% of
generated order lines had physically impossible weekend dates. Fixed by
sampling `order_date` only from a pre-built list of valid weekdays,
rather than generating and filtering after the fact.
  
## Coming next

- Power BI dashboard on top of `final_slotting_plan`
- Rebuild the transformation layer in PySpark on Databricks
- Port the pipeline to Azure

## Running it

You'll need Docker Desktop and a local PostgreSQL database. On a fresh
database, run `sql/schema.sql` and then `sql/views.sql` once by hand (the
DAG doesn't create tables or views yet).

Create a `.env` in the project root with your own database details:

    AUTOSTORE_DB_USER=...
    AUTOSTORE_DB_PASSWORD=...
    AUTOSTORE_DB_HOST=localhost
    AUTOSTORE_DB_PORT=5432
    AUTOSTORE_DB_NAME=autostore_db

Start Airflow:

    docker compose up airflow-init
    docker compose up -d

Open http://localhost:8080, log in with airflow / airflow, and trigger
the `autostore_pipeline` DAG.

To run the scripts without Airflow:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python src/generate_skus.py
    python src/build_dim_date.py
    python src/generate_orders.py
    python src/load_to_postgres.py