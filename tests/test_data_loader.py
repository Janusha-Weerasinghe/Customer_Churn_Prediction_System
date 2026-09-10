from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import load_dataset
from src.validation.validator import validate_schema, validate_target_integrity
from src.validation.validator import validate_data_types
from src.validation.validator import validate_missing_values
from src.validation.validator import validate_empty_strings
from src.validation.validator import validate_numerical_values
from src.validation.validator import validate_categorical_values
from src.validation.validator import validate_duplicate_rows
from src.validation.validator import validate_duplicate_customer_ids

from src.analysis.eda import (
    get_churn_by_numerical_feature,
    get_churn_rate,
    get_class_imbalance_ratio,
    get_column_groups,
    get_dataset_overview,
    get_numerical_statistics,
    get_numerical_summary,
    get_target_distribution,
    get_unique_value_summary,
)

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

def test_numerical_values_are_valid():
    df = load_dataset(DATASET_PATH)

    numerical_issues = validate_numerical_values(df)

    assert numerical_issues == {}

def test_categorical_values_are_valid():
    df = load_dataset(DATASET_PATH)

    categorical_issues = validate_categorical_values(df)

    assert categorical_issues == {}

def test_duplicate_rows_are_valid():
    df = load_dataset(DATASET_PATH)

    duplicate_row_issues = validate_duplicate_rows(df)

    assert duplicate_row_issues == {}

def test_customer_ids_are_unique():
    df = load_dataset(DATASET_PATH)

    duplicate_customer_id_issues = (
        validate_duplicate_customer_ids(df)
    )

    assert duplicate_customer_id_issues == {}

def test_target_integrity_is_valid():
    df = load_dataset(DATASET_PATH)

    target_issues = validate_target_integrity(df)

    assert target_issues == {}

def test_dataset_overview_is_correct():
    df = load_dataset(DATASET_PATH)

    overview = get_dataset_overview(df)

    assert overview["rows"] == 7043
    assert overview["columns"] == 21


def test_column_groups_are_not_empty():
    df = load_dataset(DATASET_PATH)

    groups = get_column_groups(df)

    assert groups["numerical"]
    assert groups["categorical"]


def test_numerical_summary_contains_expected_columns():
    df = load_dataset(DATASET_PATH)

    summary = get_numerical_summary(df)

    assert "SeniorCitizen" in summary.index
    assert "tenure" in summary.index
    assert "MonthlyCharges" in summary.index


def test_unique_value_summary_contains_all_columns():
    df = load_dataset(DATASET_PATH)

    summary = get_unique_value_summary(df)

    assert len(summary) == 21

def test_target_distribution_contains_both_classes():
    df = load_dataset(DATASET_PATH)

    distribution = get_target_distribution(df)

    assert "Yes" in distribution.index
    assert "No" in distribution.index


def test_target_distribution_counts_are_correct():
    df = load_dataset(DATASET_PATH)

    distribution = get_target_distribution(df)

    assert distribution.loc["No", "count"] == 5174
    assert distribution.loc["Yes", "count"] == 1869


def test_churn_rate_is_correct():
    df = load_dataset(DATASET_PATH)

    churn_rate = get_churn_rate(df)

    assert churn_rate == 26.54


def test_class_imbalance_ratio_is_correct():
    df = load_dataset(DATASET_PATH)

    ratio = get_class_imbalance_ratio(df)

    assert ratio == 2.77

def test_numerical_statistics_contains_expected_features():
    df = load_dataset(DATASET_PATH)

    statistics = get_numerical_statistics(df)

    assert "SeniorCitizen" in statistics.index
    assert "tenure" in statistics.index
    assert "MonthlyCharges" in statistics.index

    assert "median" in statistics.columns
    assert "skewness" in statistics.columns


def test_churn_numerical_summary_contains_both_classes():
    df = load_dataset(DATASET_PATH)

    summary = get_churn_by_numerical_feature(
        df,
        "tenure",
    )

    assert "No" in summary.index
    assert "Yes" in summary.index


def test_churn_numerical_summary_contains_expected_statistics():
    df = load_dataset(DATASET_PATH)

    summary = get_churn_by_numerical_feature(
        df,
        "MonthlyCharges",
    )

    expected_columns = {
        "count",
        "mean",
        "median",
        "minimum",
        "maximum",
    }

    assert expected_columns.issubset(summary.columns)