import os
import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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

def preprocess_data(df: pd.DataFrame):
    """Clean and encode dataset for ML model compatibility."""
    df = df.dropna(axis=0)

    # Detect label column automatically
    target_col = next((c for c in df.columns if c.lower() in ["label", "target", "class"]), df.columns[-1])

    # Encode target if categorical
    if df[target_col].dtype == object or df[target_col].dtype.name == 'category':
        le = LabelEncoder()
        df[target_col] = le.fit_transform(df[target_col])

    # Ensure numeric features
    X = df.drop(columns=[target_col])
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    df = pd.concat([X, df[target_col]], axis=1)
    return df

def split_data(df: pd.DataFrame, test_size=0.2, random_state=42):
    """Split features and target into train/test sets."""
    target_col = next((c for c in df.columns if c.lower() in ["label", "target", "class"]), df.columns[-1])
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load and preview dataset.")
    parser.add_argument("--data", required=True, help="Path to dataset file (.csv, .arff, .parquet)")
    args = parser.parse_args()
    df = load_data(args.data)
    df = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(df)
    print("===== Dataset Info =====")
    print(df.head())
    print("\nShape:", df.shape)
    print("\nColumns:", list(df.columns))