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
    print(df.shape)

    print("\n=== Columns ===")
    print(df.columns.tolist())

    print("\n=== Data Types ===")
    print(df.dtypes)

    print("\n=== First 5 Rows ===")
    print(df.head())

    print("\n=== Target Distribution ===")
    print(df["Churn"].value_counts(dropna=False))


if __name__ == "__main__":
    main()