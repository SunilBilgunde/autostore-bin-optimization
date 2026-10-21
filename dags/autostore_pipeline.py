import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = "/opt/airflow/project"

with DAG(
    dag_id="autostore_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,      # manual trigger; synthetic data has no real schedule
    catchup=False,
    tags=["autostore"],
) as dag:
    generate_skus = BashOperator(
        task_id="generate_skus",
        bash_command=f"cd {PROJECT} && python src/generate_skus.py",
    )
    build_dim_date = BashOperator(
        task_id="build_dim_date",
        bash_command=f"cd {PROJECT} && python src/build_dim_date.py",
    )
    generate_orders = BashOperator(
        task_id="generate_orders",
        bash_command=f"cd {PROJECT} && python src/generate_orders.py",
    )
    load_to_postgres = BashOperator(
        task_id="load_to_postgres",
        bash_command=f"cd {PROJECT} && python src/load_to_postgres.py",
    )

    generate_skus >> generate_orders
    [generate_orders, build_dim_date] >> load_to_postgres