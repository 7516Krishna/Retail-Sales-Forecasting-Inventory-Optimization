import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    non_zero_mask = y_true != 0
    if non_zero_mask.any():
        mape = (
            np.mean(
                np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask])
            )
            * 100
        )
    else:
        mape = 0.0

    accuracy = max(0.0, 100 - mape)

    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE (%)": round(mape, 2),
        "Forecast Accuracy (%)": round(accuracy, 2),
    }
