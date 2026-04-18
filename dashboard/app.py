from pathlib import Path
import sys

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import run_pipeline


OUTPUT_DIR = PROJECT_ROOT / "outputs"
FORECAST_PATH = OUTPUT_DIR / "forecast.csv"
INVENTORY_PATH = OUTPUT_DIR / "inventory.csv"
PLOT_PATH = OUTPUT_DIR / "sample_trend.png"


def load_csv(path):
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    return pd.read_csv(path)


def ensure_outputs(refresh=False):
    if refresh or not INVENTORY_PATH.exists() or not FORECAST_PATH.exists():
        with st.spinner("Running the retail forecasting pipeline..."):
            return run_pipeline(output_dir=OUTPUT_DIR)
    return None


def prepare_forecast_table(forecast_df):
    if forecast_df.empty:
        return forecast_df

    prepared = forecast_df.copy()
    if "ds" in prepared.columns:
        prepared = prepared.rename(columns={"ds": "date"})
    if "yhat" in prepared.columns:
        prepared = prepared.rename(columns={"yhat": "forecast"})
    if "series" not in prepared.columns:
        prepared["series"] = "default"

    prepared["date"] = pd.to_datetime(prepared["date"], errors="coerce")
    return prepared


st.set_page_config(page_title="Retail Dashboard", layout="wide")
st.title("Retail Forecasting Dashboard")

run_result = ensure_outputs(refresh=False)

if st.button("Regenerate Outputs"):
    run_result = ensure_outputs(refresh=True)

if run_result is not None and run_result.get("source_name"):
    st.caption(f"Latest pipeline source: {run_result['source_name']}")
else:
    st.caption("Showing the latest saved outputs from the outputs folder.")

forecast = prepare_forecast_table(load_csv(FORECAST_PATH))
inventory = load_csv(INVENTORY_PATH)

metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
metric_col_1.metric("Inventory Rows", len(inventory))
metric_col_2.metric(
    "High-Risk Items",
    int((inventory["risk_level"] == "High Risk").sum()) if not inventory.empty else 0,
)
metric_col_3.metric("Forecast Rows", len(forecast))

if not forecast.empty:
    st.subheader("Forecast Data")
    st.dataframe(forecast.head(20), width="stretch")

    series_options = sorted(forecast["series"].astype(str).unique())
    selected_series = st.selectbox("Select Forecast Series", series_options)
    filtered_forecast = forecast[forecast["series"].astype(str) == selected_series]

    if not filtered_forecast.empty:
        st.subheader("Forecast Trend")
        chart_df = filtered_forecast.set_index("date")[["forecast"]]
        st.line_chart(chart_df)
else:
    st.info("Forecast output is not available yet.")

if not inventory.empty:
    st.subheader("Inventory Data")
    st.dataframe(inventory, width="stretch")

    product_options = sorted(inventory["product_id"].astype(str).unique())
    selected_product = st.selectbox("Select Inventory Product", product_options)
    filtered_inventory = inventory[inventory["product_id"].astype(str) == selected_product]
    st.subheader("Selected Product Details")
    st.dataframe(filtered_inventory, width="stretch")
else:
    st.warning("Inventory output is not available. Run `python main.py` first.")

if PLOT_PATH.exists():
    st.subheader("Trend Chart")
    st.image(str(PLOT_PATH), width="stretch")
