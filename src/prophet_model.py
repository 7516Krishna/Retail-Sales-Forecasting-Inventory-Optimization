from src.series_utils import choose_reference_series


def forecast_sample(df, store_id=None, product_id=None, periods=30, min_history=30):
    try:
        from prophet import Prophet
    except ImportError:
        print("Warning: prophet is not installed. Skipping forecast generation.")
        return None

    subset, label = choose_reference_series(df, store_id=store_id, product_id=product_id)

    if len(subset) < min_history:
        print(
            "Warning: not enough history for Prophet forecast "
            f"({len(subset)} rows available)."
        )
        return None

    prophet_df = subset[["date", "sales"]].rename(columns={"date": "ds", "sales": "y"})

    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=len(prophet_df) >= 365,
    )
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    forecast["series"] = label

    return forecast
