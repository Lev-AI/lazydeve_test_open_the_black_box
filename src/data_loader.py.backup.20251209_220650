import os
import pandas as pd
from scipy.io import arff

def load_data(file_path: str):
    """Load dataset from CSV, ARFF, or Parquet files."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext == ".parquet":
        df = pd.read_parquet(file_path)
    elif ext == ".arff":
        data, meta = arff.loadarff(file_path)
        df = pd.DataFrame(data)
        # Decode byte columns (common in ARFF)
        for col in df.select_dtypes([object]):
            df[col] = df[col].apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load and preview dataset.")
    parser.add_argument("--data", required=True, help="Path to dataset file (.csv, .arff, .parquet)")
    args = parser.parse_args()
    df = load_data(args.data)
    print("===== Dataset Info =====")
    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:", list(df.columns))