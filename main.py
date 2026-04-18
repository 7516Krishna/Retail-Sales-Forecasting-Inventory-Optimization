from src.pipeline import run_pipeline


def main():
    print("Loading and preparing retail data...")
    results = run_pipeline()

    print(f"Data source: {results['source_name']}")
    print(f"Rows loaded: {results['raw_rows']}")
    print(f"Feature rows: {results['feature_rows']}")
    print(f"Inventory output: {results['inventory_path']}")

    if results["forecast_path"] is not None:
        print(f"Forecast output: {results['forecast_path']}")
    else:
        print("Forecast output: skipped because forecasting data was unavailable.")

    if results["plot_path"] is not None:
        print(f"Chart output: {results['plot_path']}")

    print("Retail forecasting pipeline completed successfully.")


if __name__ == "__main__":
    main()
