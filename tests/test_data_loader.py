from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import load_dataset
from src.validation.validator import validate_schema
from src.validation.validator import validate_data_types
from src.validation.validator import validate_missing_values
from src.validation.validator import validate_empty_strings


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

def test_dataset_schema_is_valid():
    df = load_dataset(DATASET_PATH)

    validate_schema(df)

def test_dataset_data_types_are_valid_or_flagged():
    df = load_dataset(DATASET_PATH)

    issues = validate_data_types(df)

    assert "TotalCharges" in issues

def test_dataset_has_no_pandas_missing_values():
    df = load_dataset(DATASET_PATH)

    missing_values = validate_missing_values(df)

    assert missing_values == {}

def test_empty_string_validation_detects_total_charges_issue():
    df = load_dataset(DATASET_PATH)

    empty_values = validate_empty_strings(df)

    assert "TotalCharges" in empty_values
    assert empty_values["TotalCharges"] == 11