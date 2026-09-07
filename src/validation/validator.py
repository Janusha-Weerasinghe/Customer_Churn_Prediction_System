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


EXPECTED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]
EXPECTED_DTYPES = {
    "customerID": "string",
    "gender": "string",
    "SeniorCitizen": "integer",
    "Partner": "string",
    "Dependents": "string",
    "tenure": "integer",
    "PhoneService": "string",
    "MultipleLines": "string",
    "InternetService": "string",
    "OnlineSecurity": "string",
    "OnlineBackup": "string",
    "DeviceProtection": "string",
    "TechSupport": "string",
    "StreamingTV": "string",
    "StreamingMovies": "string",
    "Contract": "string",
    "PaperlessBilling": "string",
    "PaymentMethod": "string",
    "MonthlyCharges": "float",
    "TotalCharges": "numeric",
    "Churn": "string",
}

EXPECTED_CATEGORIES = {
    "gender": {"Female", "Male"},
    "Partner": {"Yes", "No"},
    "Dependents": {"Yes", "No"},
    "PhoneService": {"Yes", "No"},
    "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": {"Yes", "No", "No internet service"},
    "OnlineBackup": {"Yes", "No", "No internet service"},
    "DeviceProtection": {"Yes", "No", "No internet service"},
    "TechSupport": {"Yes", "No", "No internet service"},
    "StreamingTV": {"Yes", "No", "No internet service"},
    "StreamingMovies": {"Yes", "No", "No internet service"},
    "Contract": {
        "Month-to-month",
        "One year",
        "Two year",
    },
    "PaperlessBilling": {"Yes", "No"},
    "PaymentMethod": {
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    },
    "Churn": {"Yes", "No"},
}

def validate_schema(df: pd.DataFrame) -> None:
    """Validate that the dataset contains the expected columns."""

    actual_columns = df.columns.tolist()

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    unexpected_columns = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: {missing_columns}"
        )

    if unexpected_columns:
        raise ValueError(
            f"Unexpected columns found: {unexpected_columns}"
        )

    if actual_columns != EXPECTED_COLUMNS:
        raise ValueError(
            "Column order does not match the expected schema."
        )

def validate_data_types(df: pd.DataFrame) -> dict:
    """
    Check whether dataset columns have the expected data types.

    Returns a dictionary containing columns that require investigation.
    """

    issues = {}

    for column, expected_type in EXPECTED_DTYPES.items():
        actual_dtype = str(df[column].dtype)

        if expected_type == "string":
           if actual_dtype not in {"object", "string", "str"}:
                issues[column] = {
                    "expected": expected_type,
                    "actual": actual_dtype,
                }

        elif expected_type == "integer":
            if not pd.api.types.is_integer_dtype(df[column]):
                issues[column] = {
                    "expected": expected_type,
                    "actual": actual_dtype,
                }

        elif expected_type == "float":
            if not pd.api.types.is_float_dtype(df[column]):
                issues[column] = {
                    "expected": expected_type,
                    "actual": actual_dtype,
                }

        elif expected_type == "numeric":
            if not pd.api.types.is_numeric_dtype(df[column]):
                issues[column] = {
                    "expected": expected_type,
                    "actual": actual_dtype,
                }

    return issues

def validate_missing_values(df: pd.DataFrame) -> dict:
    """
    Identify missing values in the dataset.

    Returns a dictionary containing columns with missing values.
    """

    missing_counts = df.isna().sum()

    return {
        column: int(count)
        for column, count in missing_counts.items()
        if count > 0
    }

def validate_empty_strings(df: pd.DataFrame) -> dict:
    """
    Identify empty or whitespace-only string values.

    Returns a dictionary containing columns with empty/whitespace values.
    """

    empty_counts = {}

    for column in df.select_dtypes(include=["object", "string"]).columns:
        count = df[column].astype("string").str.strip().eq("").sum()

        if count > 0:
            empty_counts[column] = int(count)

    return empty_counts

def validate_numerical_values(df: pd.DataFrame) -> dict:
    """
    Validate numerical feature values against expected business rules.

    Returns a dictionary containing detected validation issues.
    """

    issues = {}

    # SeniorCitizen must contain only 0 or 1.
    invalid_senior_citizen = ~df["SeniorCitizen"].isin([0, 1])

    if invalid_senior_citizen.any():
        issues["SeniorCitizen"] = {
            "issue": "Contains values other than 0 or 1",
            "count": int(invalid_senior_citizen.sum()),
        }

    # Tenure must be greater than or equal to zero.
    invalid_tenure = df["tenure"] < 0

    if invalid_tenure.any():
        issues["tenure"] = {
            "issue": "Contains negative values",
            "count": int(invalid_tenure.sum()),
        }

    # MonthlyCharges must be numeric and non-negative.
    if not pd.api.types.is_numeric_dtype(df["MonthlyCharges"]):
        issues["MonthlyCharges"] = {
            "issue": "Column is not numeric",
            "count": len(df),
        }
    else:
        invalid_monthly_charges = df["MonthlyCharges"] < 0

        if invalid_monthly_charges.any():
            issues["MonthlyCharges"] = {
                "issue": "Contains negative values",
                "count": int(invalid_monthly_charges.sum()),
            }

    # TotalCharges should contain numeric values,
    # except for known empty/whitespace values.
    total_charges_clean = (
        df["TotalCharges"]
        .astype("string")
        .str.strip()
    )

    non_empty_total_charges = total_charges_clean[
        total_charges_clean != ""
    ]

    converted_total_charges = pd.to_numeric(
        non_empty_total_charges,
        errors="coerce",
    )

    invalid_total_charges = converted_total_charges.isna()

    if invalid_total_charges.any():
        issues["TotalCharges"] = {
            "issue": "Contains non-numeric non-empty values",
            "count": int(invalid_total_charges.sum()),
        }

    return issues

def validate_categorical_values(df: pd.DataFrame) -> dict:
    """
    Validate categorical columns against their expected values.

    Returns a dictionary containing unexpected values.
    """

    issues = {}

    for column, allowed_values in EXPECTED_CATEGORIES.items():
        actual_values = set(df[column].dropna().unique())

        unexpected_values = actual_values - allowed_values

        if unexpected_values:
            issues[column] = {
                "unexpected_values": sorted(unexpected_values),
                "count": int(
                    df[column].isin(unexpected_values).sum()
                ),
            }

    return issues

def main() -> None:
    df = load_dataset(DATASET_PATH)

    print("\n=== Schema Validation ===")

    try:
        validate_schema(df)
        print("Schema validation: PASSED")
    except ValueError as error:
        print("Schema validation: FAILED")
        print(error)

    print("\n=== Data Type Validation ===")

    dtype_issues = validate_data_types(df)

    if dtype_issues:
        print("Data type validation: INVESTIGATION REQUIRED")

        for column, issue in dtype_issues.items():
            print(
                f"- {column}: "
                f"expected={issue['expected']}, "
                f"actual={issue['actual']}"
            )
    else:
        print("Data type validation: PASSED")

        print("\n=== Missing Value Validation ===")

    missing_values = validate_missing_values(df)

    if missing_values:
        print("Missing value validation: INVESTIGATION REQUIRED")

        for column, count in missing_values.items():
            print(f"- {column}: {count} missing values")
    else:
        print("Missing value validation: PASSED")

        print("\n=== Empty/Whitespace Value Validation ===")

    empty_values = validate_empty_strings(df)

    if empty_values:
        print("Empty/whitespace validation: INVESTIGATION REQUIRED")

        for column, count in empty_values.items():
            print(f"- {column}: {count} empty/whitespace values")
    else:
        print("Empty/whitespace validation: PASSED")   

    if "TotalCharges" in empty_values:
        print("\n=== TotalCharges Empty Records ===")

        empty_mask = (
            df["TotalCharges"]
            .astype("string")
            .str.strip()
            .eq("")
        )

        print(
            df.loc[
                empty_mask,
                ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]
            ].to_string(index=False)
        )
        print("\n=== Numerical Value Validation ===")

    numerical_issues = validate_numerical_values(df)

    if numerical_issues:
        print("Numerical validation: INVESTIGATION REQUIRED")

    for column, issue in numerical_issues.items():
        print(
            f"- {column}: "
            f"{issue['issue']} "
            f"(count={issue['count']})"
        )
    else:
        print("Numerical validation: PASSED")

        print("\n=== Categorical Value Validation ===")

    categorical_issues = validate_categorical_values(df)

    if categorical_issues:
        print("Categorical validation: INVESTIGATION REQUIRED")

        for column, issue in categorical_issues.items():
            print(
                f"- {column}: "
                f"unexpected values={issue['unexpected_values']} "
                f"(count={issue['count']})"
            )
    else:
        print("Categorical validation: PASSED")

if __name__ == "__main__":
    main()