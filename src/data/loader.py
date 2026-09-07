from pathlib import Path

import pandas as pd


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Load the raw customer churn dataset from a CSV file.

    Parameters
    ----------
    file_path:
        Path to the CSV dataset.

    Returns
    -------
    pd.DataFrame
        Loaded customer churn dataset.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV file, received: {path.suffix}")

    return pd.read_csv(path)