import pandas as pd

def generate_dim_date(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date,freq="D")
    dim_date = pd.DataFrame({"date": dates} )
    dim_date["day_of_week"] = dim_date["date"].dt.day_name()
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["is_weekend"] = dim_date["date"].dt.day_of_week >=5
    return dim_date

dim_date = generate_dim_date("2026-01-01", "2026-06-30")
dim_date.to_csv("data/raw/dim_date.csv", index=False)
print(dim_date.shape)
print(dim_date.head()) 
