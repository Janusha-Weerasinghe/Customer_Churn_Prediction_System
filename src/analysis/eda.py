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


def get_column_groups(df: pd.DataFrame) -> dict:
    """
    Identify numerical and categorical columns.

    TotalCharges is excluded from numerical columns here because
    it is still represented as a string in the raw dataset.
    """

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "string", "str"]
    ).columns.tolist()

    return {
        "numerical": numerical_columns,
        "categorical": categorical_columns,
    }


def get_numerical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate descriptive statistics for numerical columns.
    """
    return df.describe().T


def get_unique_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of unique values for every column.
    """
    summary = pd.DataFrame({
        "column": df.columns,
        "unique_values": [
            df[column].nunique(dropna=False)
            for column in df.columns
        ],
    })

    return summary


if __name__ == "__main__":
    df = load_eda_dataset()

    overview = get_dataset_overview(df)
    column_groups = get_column_groups(df)
    numerical_summary = get_numerical_summary(df)
    unique_summary = get_unique_value_summary(df)

    print("\n=== EDA Dataset Overview ===")
    print(f"Rows: {overview['rows']}")
    print(f"Columns: {overview['columns']}")

    print("\n=== Numerical Columns ===")
    for column in column_groups["numerical"]:
        print(f"- {column}")

    print("\n=== Categorical Columns ===")
    for column in column_groups["categorical"]:
        print(f"- {column}")

    print("\n=== Numerical Statistical Summary ===")
    print(numerical_summary.to_string())

    print("\n=== Unique Value Summary ===")
    print(unique_summary.to_string(index=False))