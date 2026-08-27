import random
import pandas as pd
from faker import Faker
from datetime import date
fake = Faker("en_GB")

ORDER_POOLS = ["RAPID", "IFA", "GENERAL TRAFFIC", "PALLET", "DPD", "Scotland", "Priority", "Box"]

QUANTITY_RANGES = {
    "Brake Disc": (1, 50),
    "Brake Pad": (1, 90),
    "Brake Shoe": (1, 90),
    "Engine Oil Filter": (1, 100),
    "Engine Air Filter": (1, 100),
    "Engine Fuel Filter": (1, 100),
    "Engine Kabin Filter": (1, 100),
    "Control Arm": (1, 8),
    "Stabilizer Link": (1, 10),
    "Tie Rod": (1, 10),
    "Steering Kit": (1, 6),
}

DELIVERY_OPTIONS = {
    "DPD": ["Next Day by 10:30am", "Next Day by 12:30pm", "Next Day"],
    "DHL": ["Express", "Economy Select", "Next Day by 10:30am", "Next Day by 12noon"],
}

parts_df = pd.read_csv("data/raw/parts.csv")

def generate_order_number(sequence_num):
    return f"CSO{sequence_num:06d}"

def generate_work_id():
    number = random.randint(100000000, 999999999)
    return f"WID{number}"

def generate_order_line(parts_df):
    random_part = parts_df.sample(n=1)
    category = random_part['category'].iloc[0]
    sku = random_part["sku"].iloc[0]

    min_qty, max_qty = QUANTITY_RANGES[category]
    quantity = random.randint(min_qty,max_qty)

    return sku, category, quantity

def generate_order_lines(parts_df, order_number, num_lines):
    lines = []
    for i in range(num_lines):
        sku, category, quantity, = generate_order_line(parts_df)
        line_number = i + 1
        lines.append((order_number, line_number, sku, category, quantity))
    return lines


def summarize_order(order_number, order_lines_df):
    order_rows = order_lines_df[order_lines_df["order_number"] == order_number]
    category_totals = order_rows.groupby("category")["quantity"].sum()

    summary_parts = []
    for category, total in category_totals.items():
        summary_parts.append(f"{category}: {total}")

    summary = ", ".join(summary_parts)
    return summary

def generate_delivery(delivery_options):
    delivery_code = random.choice(list(delivery_options.keys()))
    delivery_type = random.choice(delivery_options[delivery_code])
    return delivery_code, delivery_type

def generate_customers(num_customers):
    customers = []
    for i in range(num_customers):
        customer_id = i + 1
        customer_name = fake.company()
        address = fake.street_address()
        city = fake.city()
        postcode = fake.postcode()
        customers.append((customer_id, customer_name, address, city, postcode))
    return customers

customers = generate_customers(40)

customers_df = pd.DataFrame(customers,columns=["customer_id", "customer_name", "address", "city", "postcode"])
customers_df.to_csv("data/raw/customers.csv", index=False)

def get_weekday_dates(start_date, end_date):
    all_dates = pd.date_range(start=start_date, end=end_date,freq='D')
    weekday_dates =  all_dates[all_dates.day_of_week <5]
    return list(weekday_dates)

weekday_dates = get_weekday_dates(date(2026, 1, 1), date(2026, 6, 30))

def generate_order(order_number, order_lines_df,customers,weekday_dates):
    order_date = random.choice(weekday_dates).date()
    customer = random.choice(customers)
    customer_id = customer[0]
    
    order_pool = random.choice(ORDER_POOLS)
    delivery_code, delivery_type = generate_delivery(DELIVERY_OPTIONS)
    work_id = generate_work_id()
    products_summary = summarize_order(order_number, order_lines_df)

    return (order_number, order_date, customer_id, order_pool, delivery_code, delivery_type, work_id, products_summary)

# generate order lines for multiple orders
all_order_lines = []
starting_sequence = 100000

for i in range(500):
    order_number = generate_order_number(starting_sequence + i)
    num_lines = random.randint(1,100)
    lines = generate_order_lines(parts_df, order_number, num_lines)
    all_order_lines.extend(lines)

order_lines_df = pd.DataFrame(all_order_lines, columns=["order_number", "line_number", "sku", "category", "quantity"])
order_lines_df.to_csv("data/raw/order_lines.csv", index=False)


#generates order table
orders_data = []
unique_orders = order_lines_df["order_number"].unique()

for order_number in unique_orders:
    order = generate_order(order_number, order_lines_df,customers,weekday_dates)
    orders_data.append(order)

orders_df = pd.DataFrame(orders_data, columns=["order_number","order_date", "customer_id", "order_pool",
                                               "delivery_code", "delivery_type","work_id", "products_summary"
                                               ])
orders_df.to_csv("data/raw/orders.csv", index=False)

print(order_lines_df.shape)
print(orders_df.head())
print(orders_df.shape)