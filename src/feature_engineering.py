def create_features(df):
    if df.empty:
        raise ValueError("Cannot create features from an empty dataset.")

    df = df.copy().sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["weekday"] = df["date"].dt.weekday

    df["lag_1"] = df.groupby(["store_id", "product_id"])["sales"].shift(1)
    df["lag_7"] = df.groupby(["store_id", "product_id"])["sales"].shift(7)
    df["rolling_mean_7"] = (
        df.groupby(["store_id", "product_id"])["sales"]
        .transform(lambda values: values.shift(1).rolling(7).mean())
    )

    df = df.dropna().reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "Feature engineering removed all rows. Use a dataset with at least 8 "
            "observations per store/product series."
        )

    return df
