from pathlib import Path

from src.data_generator import generate_synthetic_data
from src.feature_engineering import create_features
from src.inventory import calculate_inventory
from src.ml_model import train_ml
from src.preprocessing import load_kaggle_data
from src.prophet_model import forecast_sample
from src.visualization import plot_sample


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "kaggle_sales.csv"
SYNTHETIC_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "synthetic_sales.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"


def run_pipeline(data_path=None, output_dir=None):
    source_path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    output_path = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        df_raw = load_kaggle_data(source_path)
    except ValueError:
        if not SYNTHETIC_DATA_PATH.exists() or SYNTHETIC_DATA_PATH.stat().st_size == 0:
            generate_synthetic_data(save_path=SYNTHETIC_DATA_PATH)
        df_raw = load_kaggle_data(SYNTHETIC_DATA_PATH)

    feature_df = create_features(df_raw)
    model_df, model = train_ml(feature_df)
    forecast_df = forecast_sample(df_raw)
    inventory_df = calculate_inventory(df_raw)

    forecast_path = None
    if forecast_df is not None and not forecast_df.empty:
        forecast_path = output_path / "forecast.csv"
        forecast_df.to_csv(forecast_path, index=False)

    inventory_path = output_path / "inventory.csv"
    inventory_df.to_csv(inventory_path, index=False)

    plot_path = plot_sample(df_raw, output_dir=output_path)

    return {
        "source_path": df_raw.attrs.get("source_path"),
        "source_name": df_raw.attrs.get("source_name"),
        "raw_rows": len(df_raw),
        "feature_rows": len(feature_df),
        "model_rows": len(model_df),
        "model": model,
        "forecast_df": forecast_df,
        "forecast_path": forecast_path,
        "inventory_df": inventory_df,
        "inventory_path": inventory_path,
        "plot_path": plot_path,
    }
