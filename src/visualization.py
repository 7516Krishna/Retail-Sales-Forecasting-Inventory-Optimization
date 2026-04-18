from pathlib import Path

import matplotlib.pyplot as plt

from src.series_utils import choose_reference_series


def plot_sample(df, output_dir="outputs", store_id=None, product_id=None):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    subset, label = choose_reference_series(df, store_id=store_id, product_id=product_id)

    if subset.empty:
        print("Warning: no data available for visualization.")
        return None

    chart_path = output_path / "sample_trend.png"

    plt.figure(figsize=(10, 5))
    plt.plot(subset["date"], subset["sales"])
    plt.title(f"Sales Trend ({label})")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    return chart_path
