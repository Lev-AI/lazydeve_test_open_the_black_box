"""
Generate a Laboratory-Quality synthetic CSV that emulates CIC-IDS2017-style columns.

Uses sklearn.make_classification with controlled difficulty so that a
RandomForest baseline achieves ~80-88% accuracy (realistic, not 99% fake).

Column names match what data_loader.py expects (auto-detects 'Label' column).
"""

import os
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

# ---------------------------------------------------------------------------
# Column schema — 20 features + 1 label, CIC-IDS2017 style
# ---------------------------------------------------------------------------
FEATURE_COLUMNS = [
    # Original 14
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Bwd Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Max",
    "Fwd Packet Length Min",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    # 6 additional features (to reach n_features=20)
    "Fwd IAT Total",
    "Bwd IAT Total",
    "Fwd PSH Flags",
    "Bwd PSH Flags",
    "Fwd Header Length",
    "Bwd Header Length",
]

LABEL_COLUMN = "Label"

# Physical-scale multipliers so values look like real network traffic
_SCALE = np.array([
    65535,   # Destination Port
    1e6,     # Flow Duration (microseconds)
    500,     # Total Fwd Packets
    500,     # Total Bwd Packets
    1e6,     # Total Length of Fwd Packets (bytes)
    1e6,     # Total Length of Bwd Packets (bytes)
    1500,    # Fwd Packet Length Max (MTU)
    64,      # Fwd Packet Length Min
    1500,    # Bwd Packet Length Max
    64,      # Bwd Packet Length Min
    1e6,     # Flow Bytes/s
    1e4,     # Flow Packets/s
    1e4,     # Flow IAT Mean (microseconds)
    1e4,     # Flow IAT Std
    1e5,     # Fwd IAT Total
    1e5,     # Bwd IAT Total
    1,       # Fwd PSH Flags (0/1-ish)
    1,       # Bwd PSH Flags (0/1-ish)
    200,     # Fwd Header Length (bytes)
    200,     # Bwd Header Length (bytes)
])


def generate_synthetic(
    n_rows: int = 2000,
    output_path: str = "data/synthetic_data.csv",
    seed: int = 42,
) -> str:
    """Generate a laboratory-quality synthetic CSV.

    Uses make_classification with controlled overlap (class_sep=1.0) and
    label noise (flip_y=0.01) to produce ~80-88% baseline accuracy.

    Args:
        n_rows: Number of samples.
        output_path: Destination CSV path.
        seed: Random seed for full reproducibility.

    Returns:
        Absolute path to the written CSV.
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    n_features = len(FEATURE_COLUMNS)  # 20

    # --- Core: realistic difficulty -------------------------------------------
    X_raw, y = make_classification(
        n_samples=n_rows,
        n_features=n_features,
        n_informative=12,
        n_redundant=2,
        n_clusters_per_class=2,
        n_classes=2,
        class_sep=0.6,
        flip_y=0.03,
        weights=[0.6, 0.4],
        random_state=seed,
    )

    # --- Scale to physical units ----------------------------------------------
    # make_classification outputs ~N(0,1); shift to positive then multiply
    # MinMax per-column to [0, 1], then scale by physical multiplier
    col_min = X_raw.min(axis=0)
    col_max = X_raw.max(axis=0)
    col_range = col_max - col_min
    col_range[col_range == 0] = 1.0  # avoid division by zero
    X_norm = (X_raw - col_min) / col_range  # [0, 1]
    X_scaled = X_norm * _SCALE

    # Ensure no negatives (belt-and-suspenders after normalization)
    X_scaled = np.abs(X_scaled)

    # Round integer-like columns (ports, packet counts, flags)
    int_cols = [0, 2, 3, 16, 17]  # Port, Fwd/Bwd Packets, PSH Flags
    for c in int_cols:
        X_scaled[:, c] = np.round(X_scaled[:, c])

    # --- Assemble DataFrame ---------------------------------------------------
    df = pd.DataFrame(X_scaled, columns=FEATURE_COLUMNS)
    df[LABEL_COLUMN] = np.where(y == 0, "BENIGN", "MALICIOUS")

    out_abs = os.path.abspath(output_path)
    df.to_csv(out_abs, index=False)
    return out_abs


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate laboratory-quality synthetic CIC-IDS2017-style CSV."
    )
    parser.add_argument(
        "--rows", type=int, default=2000, help="Number of rows (default: 2000)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/synthetic_data.csv",
        help="Output CSV path",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    path = generate_synthetic(n_rows=args.rows, output_path=args.output, seed=args.seed)
    print(f"Generated {args.rows} rows -> {path}")
    print(f"Features: {len(FEATURE_COLUMNS)} | Label: '{LABEL_COLUMN}' (BENIGN / MALICIOUS)")

    # Quick sanity check
    df = pd.read_csv(path)
    print(f"\nClass distribution:\n{df[LABEL_COLUMN].value_counts()}")
    print(f"\nSample:\n{df.head()}")


if __name__ == "__main__":
    main()
