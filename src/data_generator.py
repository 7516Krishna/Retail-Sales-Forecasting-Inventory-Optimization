from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_data(
    num_days=365,
    num_stores=3,
    num_products=5,
    save_path="data/raw/synthetic_sales.csv",
):
    np.random.seed(42)

    dates = pd.date_range(start="2023-01-01", periods=num_days)
    data = []

    for store in range(1, num_stores + 1):
        for product in range(1, num_products + 1):
            base_demand = np.random.randint(20, 50)

            for index, date in enumerate(dates):
                trend = index * 0.02
                seasonality = 10 * np.sin(2 * np.pi * index / 30)
                weekday_effect = 5 if date.weekday() >= 5 else 0
                noise = np.random.normal(0, 3)

                sales = base_demand + trend + seasonality + weekday_effect + noise
                sales = max(0, round(sales))

                data.append([date, store, product, sales])

    df = pd.DataFrame(data, columns=["date", "store", "item", "sales"])

    destination = Path(save_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)

    print(f"Synthetic data saved at: {destination}")

    return df
