
import os 
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

parts_df = pd.read_csv("data/raw/parts.csv")
customers_df = pd.read_csv("data/raw/customers.csv")
orders_df = pd.read_csv("data/raw/orders.csv")
order_lines_df = pd.read_csv("data/raw/order_lines.csv")

parts_df.to_sql("parts", engine, if_exists="append", index=False)
customers_df.to_sql("customers", engine, if_exists="append", index=False)
orders_df.to_sql("orders", engine, if_exists="append", index=False)
order_lines_df.to_sql("order_lines", engine, if_exists="append", index=False)

print("Load complete")