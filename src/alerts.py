def generate_alerts(inventory_df):
    alerts = []

    for _, row in inventory_df.iterrows():
        if row["current_stock"] <= row["reorder_point"]:
            alerts.append(
                f"Warning: product {row['product_id']} in store {row['store_id']} "
                "requires reorder"
            )

    return alerts
