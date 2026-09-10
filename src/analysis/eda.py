from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from src.data.loader import load_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

EDA_ARTIFACTS_DIR = PROJECT_ROOT / "artifacts" / "eda"

EDA_ARTIFACTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
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

def get_target_distribution(
    df: pd.DataFrame,
    target_column: str = "Churn",
) -> pd.DataFrame:
    """
    Calculate target class counts and percentages.
    """

    counts = df[target_column].value_counts()

    distribution = pd.DataFrame({
        "count": counts,
        "percentage": (
            counts / len(df) * 100
        ).round(2),
    })

    return distribution


def get_churn_rate(
    df: pd.DataFrame,
    target_column: str = "Churn",
) -> float:
    """
    Calculate the percentage of customers who churned.
    """

    churn_count = (
        df[target_column]
        .eq("Yes")
        .sum()
    )

    return round(
        churn_count / len(df) * 100,
        2,
    )


def get_class_imbalance_ratio(
    df: pd.DataFrame,
    target_column: str = "Churn",
) -> float:
    """
    Calculate the ratio between the majority and minority classes.
    """

    class_counts = df[target_column].value_counts()

    majority_count = class_counts.max()
    minority_count = class_counts.min()

    return round(
        majority_count / minority_count,
        2,
    )

def plot_target_distribution(
    df: pd.DataFrame,
    target_column: str = "Churn",
) -> None:
    """
    Plot the distribution of the target variable.
    """

    counts = df[target_column].value_counts()

    plt.figure(figsize=(7, 5))

    counts.plot(kind="bar")

    plt.title("Customer Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Number of Customers")

    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()

def get_numerical_statistics(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate extended descriptive statistics for numerical features.
    """

    numerical_columns = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
    ]

    statistics = df[numerical_columns].describe().T

    statistics["median"] = (
        df[numerical_columns].median()
    )

    statistics["skewness"] = (
        df[numerical_columns].skew()
    )

    return statistics

# Add numerical-analysis functions
def get_churn_by_numerical_feature(
    df: pd.DataFrame,
    feature: str,
) -> pd.DataFrame:
    """
    Calculate numerical feature statistics grouped by churn.
    """

    return (
        df.groupby("Churn")[feature]
        .agg(
            count="count",
            mean="mean",
            median="median",
            minimum="min",
            maximum="max",
        )
        .round(2)
    )


#Add numerical distribution plots
def plot_numerical_distributions(
    df: pd.DataFrame,
) -> None:
    """
    Plot distributions for numerical features.
    """

    numerical_columns = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
    ]

    for column in numerical_columns:
        plt.figure(figsize=(8, 5))

        df[column].plot(
            kind="hist",
            bins=30,
        )

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

# Add churn comparison plots
def plot_numerical_features_by_churn(
    df: pd.DataFrame,
) -> None:
    """
    Compare numerical feature distributions between churn classes.
    """

    numerical_columns = [
        "tenure",
        "MonthlyCharges",
    ]

    for column in numerical_columns:
        plt.figure(figsize=(8, 5))

        df.boxplot(
            column=column,
            by="Churn",
        )

        plt.title(f"{column} by Churn")
        plt.suptitle("")
        plt.xlabel("Churn")
        plt.ylabel(column)

        plt.tight_layout()
        plt.show()
def save_target_distribution(
    df: pd.DataFrame,
) -> None:
    """
    Save target distribution statistics.
    """

    distribution = get_target_distribution(df)

    output_path = (
        EDA_ARTIFACTS_DIR
        / "target_distribution.csv"
    )

    distribution.to_csv(output_path)


def save_numerical_statistics(
    df: pd.DataFrame,
) -> None:
    """
    Save numerical feature statistics.
    """

    statistics = get_numerical_statistics(df)

    output_path = (
        EDA_ARTIFACTS_DIR
        / "numerical_statistics.csv"
    )

    statistics.to_csv(output_path)


def save_churn_numerical_summary(
    df: pd.DataFrame,
) -> None:
    """
    Save numerical feature statistics grouped by churn.
    """

    rows = []

    for feature in ["tenure", "MonthlyCharges"]:
        summary = get_churn_by_numerical_feature(
            df,
            feature,
        )

        summary = summary.reset_index()
        summary.insert(0, "feature", feature)

        rows.append(summary)

    combined_summary = pd.concat(
        rows,
        ignore_index=True,
    )

    output_path = (
        EDA_ARTIFACTS_DIR
        / "churn_numerical_summary.csv"
    )

    combined_summary.to_csv(
        output_path,
        index=False,
    )

def get_category_churn_rates(
    df: pd.DataFrame,
    feature: str,
    target_column: str = "Churn",
) -> pd.DataFrame:
    """
    Calculate customer count and churn rate for each category.
    """

    summary = (
        df.groupby(feature)[target_column]
        .agg(
            customers="count",
            churned=lambda x: (x == "Yes").sum(),
        )
    )

    summary["churn_rate"] = (
        summary["churned"]
        / summary["customers"]
        * 100
    ).round(2)

    return summary.sort_values(
        "churn_rate",
        ascending=False,
    )

def get_categorical_churn_summary(
    df: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """
    Generate churn-rate summaries for multiple categorical features.
    """

    results = []

    for feature in features:
        summary = get_category_churn_rates(df, feature)

        for category, row in summary.iterrows():
            results.append({
                "feature": feature,
                "category": category,
                "customers": int(row["customers"]),
                "churned": int(row["churned"]),
                "churn_rate": float(row["churn_rate"]),
            })

    return pd.DataFrame(results)

def plot_churn_rate_by_category(
    df: pd.DataFrame,
    feature: str,
) -> None:
    """
    Plot churn rate for each category of a categorical feature.
    """

    summary = get_category_churn_rates(df, feature)

    plt.figure(figsize=(9, 5))

    summary["churn_rate"].plot(
        kind="bar",
    )

    plt.title(f"Churn Rate by {feature}")
    plt.xlabel(feature)
    plt.ylabel("Churn Rate (%)")

    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    plt.show()

def save_categorical_churn_summary(
    df: pd.DataFrame,
    features: list[str],
) -> None:
    """
    Save categorical churn analysis results.
    """

    summary = get_categorical_churn_summary(
        df,
        features,
    )

    output_path = (
        EDA_ARTIFACTS_DIR
        / "categorical_churn_summary.csv"
    )

    summary.to_csv(
        output_path,
        index=False,
    )

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

    target_distribution = get_target_distribution(df)
    churn_rate = get_churn_rate(df)
    imbalance_ratio = get_class_imbalance_ratio(df)

    print("\n=== Target Distribution ===")
    print(target_distribution.to_string())

    print("\n=== Churn Rate ===")
    print(f"Churn rate: {churn_rate}%")

    print("\n=== Class Imbalance ===")
    print(
        f"Majority/minority class ratio: "
        f"{imbalance_ratio}:1"
    )

    plot_target_distribution(df)

    numerical_statistics = get_numerical_statistics(df)

    print("\n=== Extended Numerical Statistics ===")
    print(numerical_statistics.to_string())

    print("\n=== Numerical Features by Churn ===")

    for feature in ["tenure", "MonthlyCharges"]:
        print(f"\n--- {feature} ---")

        churn_summary = get_churn_by_numerical_feature(
            df,
            feature,
        )

        print(churn_summary.to_string())

    plot_numerical_distributions(df)
    plot_numerical_features_by_churn(df)

    save_target_distribution(df)
    save_numerical_statistics(df)
    save_churn_numerical_summary(df)

    print("\n=== EDA Artifacts ===")
    print(
        f"Saved EDA outputs to: "
        f"{EDA_ARTIFACTS_DIR}"
    )

    categorical_features = [
        "Contract",
        "InternetService",
        "PaymentMethod",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "PaperlessBilling",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "StreamingTV",
        "StreamingMovies",
        "gender",
    ]

    categorical_summary = get_categorical_churn_summary(
        df,
        categorical_features,
    )

    print("\n=== Categorical Churn Analysis ===")
    print(categorical_summary.to_string(index=False))

    save_categorical_churn_summary(
        df,
        categorical_features,
    )