# AutoStore Bin Optimization Pipeline

An end-to-end data engineering project built around a synthetic AutoStore
warehouse setup. It generates a realistic parts catalog and order data,
with the eventual goal of analyzing and optimizing bin placement based on
how often parts actually get ordered.

Scaled roughly in line with real AutoStore deployments — around 60k bins,
40 robots, 10 ports.

## Status

Phase 1 (data generation) and Phase 2 (loading into PostgreSQL) are done.

- `generate_skus.py` builds a catalog of ~500 parts across three fictional
  brands, each with a realistic weight and set of dimensions based on
  actual AutoStore bin size/weight limits.
- `generate_orders.py` builds order and order-line data on top of that
  catalog — quantities are weighted by part category, and customer/address
  data uses UK formatting.
- `load_to_postgres.py` loads all three datasets into PostgreSQL, with primary keys,unique constraints, and foreign keys linking order lines back to both orders and parts.
  DB credentials are kept in `.env` file, not in the repo.
  
## Coming next

- Build out the SQL transformation layer / star schema
- Orchestrate with Airflow
- Dashboards in Metabase

## Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/generate_skus.py
python src/generate_orders.py
```

You'll also need a local PostgreSQL database and `.env` file with your own DB credentials to run 'load_to_postgres.py'.