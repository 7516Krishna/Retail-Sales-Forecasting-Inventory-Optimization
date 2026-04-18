import pandas as pd


def compare_models(ml_metrics=None, prophet_metrics=None):
    ml_metrics = ml_metrics or {}
    prophet_metrics = prophet_metrics or {}

    return pd.DataFrame(
        {
            "Model": ["ML", "Prophet"],
            "Accuracy": [
                ml_metrics.get("Forecast Accuracy (%)", 0),
                prophet_metrics.get("Forecast Accuracy (%)", 0),
            ],
        }
    )
