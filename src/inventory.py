import numpy as np
import pandas as pd


def calculate_inventory(df):
    results = []

    grouped = df.groupby(["store_id", "product_id"])

    for (store, product), group in grouped:
        ordered_group = group.sort_values("date")
        avg = group["sales"].mean()
        std = group["sales"].std()

        if np.isnan(std):
            std = 0

        lead_time = 7
        z_score = 1.65

        safety_stock = z_score * std * np.sqrt(lead_time)
        reorder_point = avg * lead_time + safety_stock

        if "stock_on_hand" in ordered_group.columns and ordered_group["stock_on_hand"].notna().any():
            current_stock = ordered_group["stock_on_hand"].dropna().iloc[-1]
        else:
            current_stock = ordered_group["sales"].tail(lead_time + 1).sum()

        results.append(
            {
                "store_id": store,
                "product_id": product,
                "avg_demand": round(avg, 2),
                "safety_stock": round(safety_stock, 2),
                "reorder_point": round(reorder_point, 2),
                "current_stock": round(current_stock, 2),
            }
        )

    if not results:
        return pd.DataFrame(
            columns=[
                "store_id",
                "product_id",
                "avg_demand",
                "safety_stock",
                "reorder_point",
                "current_stock",
                "risk_level",
                "reorder_qty",
            ]
        )

    inventory_df = pd.DataFrame(results)
    inventory_df["risk_level"] = inventory_df.apply(
        lambda row: "High Risk"
        if row["current_stock"] < row["reorder_point"]
        else "Safe",
        axis=1,
    )
    inventory_df["reorder_qty"] = (
        inventory_df["reorder_point"] - inventory_df["current_stock"]
    ).clip(lower=0).round(2)

    return inventory_df
