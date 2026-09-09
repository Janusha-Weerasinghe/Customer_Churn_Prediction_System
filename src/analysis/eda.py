from pathlib import Path

import pandas as pd

from src.data.loader import load_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)


def load_eda_dataset() -> pd.DataFrame:
    """
    Load the raw dataset for exploratory data analysis.
    """
    return load_dataset(DATASET_PATH)


def get_dataset_overview(df: pd.DataFrame) -> dict:
    """
    Return basic dataset dimensions and column information.
    """
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
    }


if __name__ == "__main__":
    df = load_eda_dataset()

    overview = get_dataset_overview(df)

    print("\n=== EDA Dataset Overview ===")
    print(f"Rows: {overview['rows']}")
    print(f"Columns: {overview['columns']}")