from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import load_dataset


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)


def test_load_dataset_returns_dataframe():
    df = load_dataset(DATASET_PATH)

    assert isinstance(df, pd.DataFrame)


def test_load_dataset_has_expected_columns():
    df = load_dataset(DATASET_PATH)

    expected_columns = {
        "customerID",
        "gender",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "Contract",
        "Churn",
    }

    assert expected_columns.issubset(df.columns)


def test_load_dataset_rejects_missing_file():
    with pytest.raises(FileNotFoundError):
        load_dataset("does_not_exist.csv")