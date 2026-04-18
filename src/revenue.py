import pandas as pd


def calculate_revenue(df):
    revenue_df = df.copy()

    product_codes, _ = pd.factorize(revenue_df["product_id"])
    revenue_df["price"] = 100 + (product_codes + 1) * 10
    revenue_df["revenue"] = revenue_df["sales"] * revenue_df["price"]

    return revenue_df
