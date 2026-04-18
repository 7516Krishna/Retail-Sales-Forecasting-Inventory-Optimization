import pandas as pd


def choose_reference_series(df, store_id=None, product_id=None):
    if df.empty:
        return pd.DataFrame(columns=["date", "sales"]), "no data"

    if store_id is not None and product_id is not None:
        requested = _filter_series(df, store_id, product_id)
        if not requested.empty:
            return requested, f"store={store_id}, product={product_id}"

    series_sizes = (
        df.groupby(["store_id", "product_id"]).size().sort_values(ascending=False)
    )

    if not series_sizes.empty:
        selected_store, selected_product = series_sizes.index[0]
        selected = _filter_series(df, selected_store, selected_product)
        return selected, f"store={selected_store}, product={selected_product}"

    daily_sales = (
        df.groupby("date", as_index=False)["sales"].sum().sort_values("date")
    )
    return daily_sales, "all stores / all products"


def _filter_series(df, store_id, product_id):
    series_df = df[
        (df["store_id"].astype(str) == str(store_id))
        & (df["product_id"].astype(str) == str(product_id))
    ].copy()
    return series_df.sort_values("date").reset_index(drop=True)
