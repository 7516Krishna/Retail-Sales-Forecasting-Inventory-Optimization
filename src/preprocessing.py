from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError


def load_kaggle_data(path, fallback_paths=None):
    candidates = [Path(path)]
    if fallback_paths:
        candidates.extend(Path(candidate) for candidate in fallback_paths)

    errors = []

    for candidate in candidates:
        try:
            raw_df = _read_csv(candidate)
            retail_df = _standardize_retail_schema(raw_df)
            if retail_df.empty:
                raise ValueError("dataset is empty after cleaning")

            retail_df.attrs["source_path"] = str(candidate)
            retail_df.attrs["source_name"] = candidate.name
            return retail_df
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")

    error_details = "\n".join(errors)
    raise ValueError(f"Unable to load a usable retail dataset.\n{error_details}")


def _read_csv(path):
    if not path.exists():
        raise FileNotFoundError("file does not exist")

    if path.stat().st_size == 0:
        raise EmptyDataError("file is empty")

    return pd.read_csv(path)


def _standardize_retail_schema(df):
    column_map = {_normalize_name(column): column for column in df.columns}

    date_column = _find_column(column_map, ["date", "order date", "data"])
    sales_column = _find_column(column_map, ["sales", "venda"])
    stock_column = _find_column(column_map, ["stock", "inventory", "estoque"])

    if date_column is None:
        raise ValueError("missing a supported date column")

    if sales_column is None:
        raise ValueError("missing a supported sales column")

    store_column = _find_column(column_map, ["store_id", "store", "region", "state"])
    product_column = _find_column(column_map, ["product_id", "item", "product id"])

    retail_df = pd.DataFrame(
        {
            "date": pd.to_datetime(df[date_column], errors="coerce"),
            "sales": pd.to_numeric(df[sales_column], errors="coerce"),
        }
    )

    if store_column is None:
        retail_df["store_id"] = "Store-1"
    else:
        retail_df["store_id"] = df[store_column].fillna("Store-1").astype(str)

    if product_column is None:
        retail_df["product_id"] = "Product-1"
    else:
        retail_df["product_id"] = df[product_column].fillna("Product-1").astype(str)

    if stock_column is not None:
        retail_df["stock_on_hand"] = pd.to_numeric(df[stock_column], errors="coerce")

    retail_df = retail_df.dropna(subset=["date", "sales"]).copy()
    retail_df["sales"] = retail_df["sales"].astype(float)

    aggregation = {"sales": "sum"}
    if "stock_on_hand" in retail_df.columns:
        aggregation["stock_on_hand"] = "last"

    retail_df = (
        retail_df.groupby(["date", "store_id", "product_id"], as_index=False)
        .agg(aggregation)
        .sort_values(["store_id", "product_id", "date"])
        .reset_index(drop=True)
    )

    return retail_df


def _find_column(column_map, aliases):
    for alias in aliases:
        if alias in column_map:
            return column_map[alias]
    return None


def _normalize_name(value):
    return str(value).strip().lower().replace("_", " ").replace("-", " ")
