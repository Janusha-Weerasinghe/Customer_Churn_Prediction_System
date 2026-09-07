from pathlib import Path

from loader import load_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)


def main() -> None:
    df = load_dataset(DATASET_PATH)

    print("\n=== Dataset Shape ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n=== Column Names ===")
    for column in df.columns:
        print(f"- {column}")

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== First 5 Rows ===")
    print(df.head().to_string())

    print("\n=== Dataset Information ===")
    df.info()

    print("\n=== Target Distribution ===")
    print(df["Churn"].value_counts(dropna=False))

    print("\n=== Target Distribution (%) ===")
    print(
        (df["Churn"].value_counts(normalize=True, dropna=False) * 100)
        .round(2)
    )


if __name__ == "__main__":
    main()