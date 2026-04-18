from sklearn.ensemble import RandomForestRegressor


def train_ml(df):
    if df.empty:
        raise ValueError("Cannot train a model on an empty feature set.")

    features = ["day", "month", "weekday", "lag_1", "lag_7", "rolling_mean_7"]

    training_df = df.copy()
    X = training_df[features]
    y = training_df["sales"]

    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=1)
    model.fit(X, y)

    training_df["ml_pred"] = model.predict(X)

    return training_df, model
