# AutoStore Bin Optimization Pipeline

An end-to-end data engineering project built around a synthetic AutoStore
warehouse setup. It generates a realistic parts catalog and order data,
with the eventual goal of analyzing and optimizing bin placement based on
how often parts actually get ordered.

Scaled roughly in line with real AutoStore deployments — around 60k bins,
40 robots, 10 ports.

## Status

Phase 1 (data generation) and Phase 2 (loading into PostgreSQL) and phase 3(transformation) are done.

- `generate_skus.py` builds a catalog of ~500 parts across three fictional
  brands, each with a realistic weight and set of dimensions based on
  actual AutoStore bin size/weight limits.
- `generate_orders.py` builds order and order-line data on top of that
  catalog — quantities are weighted by part category, and customer/address
  data uses UK formatting.
- `load_to_postgres.py` loads all three datasets into PostgreSQL, with primary keys,unique constraints, and foreign keys linking order lines back to both orders and parts.
  DB credentials are kept in `.env` file, not in the repo.
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

Combining pick frequency with bin capacity reveals something raw
popularity alone misses: Brake Discs dominate the restock-trip estimates,
not because they're picked most often overall, but because their weight
(4-15kg) caps them at just 2 units per bin under AutoStore's 30kg limit.
High-frequency + low-capacity means discs need restocking roughly 30x
more often than similarly-popular but lighter/smaller parts like filters.

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