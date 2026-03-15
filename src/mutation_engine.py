"""
This module handles mutation operations.
"""

import numpy as np
import pandas as pd
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set a seed for reproducibility
np.random.seed(42)

# Label column must never be mutated
LABEL_COLUMN = "Label"


def _safe_columns(df, columns):
    """Return columns to mutate: only those in df that are not Label."""
    return [c for c in columns if c in df.columns and c != LABEL_COLUMN]


def apply_noise(df, columns, intensity):
    """
    Add random Gaussian noise to numerical columns with ADAPTIVE scaling.
    Noise scale per column = that column's standard deviation × intensity,
    so intensity 0.5 means "half the typical spread" of noise—visible to the model.
    'Label' is never mutated.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list): Column names to mutate (Label is always excluded).
    intensity (float): Multiplier on each column's std (e.g. 0.5 = half a std of noise).

    Returns:
    pd.DataFrame: New DataFrame with noise added to specified columns.
    """
    logger.info("Applying noise to dataset (adaptive scaling).")
    out = df.copy()
    cols = _safe_columns(out, columns)
    if not cols:
        return out
    for col in cols:
        if pd.api.types.is_numeric_dtype(out[col]):
            std = out[col].std()
            if std == 0 or (std != std):  # 0 or NaN
                std = 1.0
            noise = np.random.normal(0, std * intensity, size=len(out))
            out[col] = out[col].astype(float) + noise
    return out


def apply_zeroing(df, columns, intensity):
    """
    Randomly set values to 0 with probability equal to intensity.
    Intensity is treated as a probability: clipped to [0.0, 1.0].
    Values > 1.0 (e.g. 3.0) are treated as 1.0 (100% zeroing).
    'Label' is never mutated.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list): Column names to mutate (Label is always excluded).
    intensity (float): Probability per cell of being set to 0 (clipped to 0–1).

    Returns:
    pd.DataFrame: New DataFrame with zeroing applied to specified columns.
    """
    logger.info("Applying zeroing to dataset.")
    out = df.copy()
    cols = _safe_columns(out, columns)
    if not cols:
        return out
    # Treat intensity as probability: clip to [0, 1]; e.g. 3.0 -> 1.0
    intensity = float(intensity)
    intensity = max(0.0, min(1.0, intensity))
    rng = np.random.default_rng(42)
    for col in cols:
        mask = rng.random(size=len(out)) < intensity
        out.loc[mask, col] = 0
    return out


def add_noise(X, intensity=0.05):
    """
    Adds Gaussian noise to numerical features in the DataFrame.
    
    Parameters:
    X (pd.DataFrame): Input DataFrame with numerical features.
    intensity (float): The intensity of the noise to be added.
    
    Returns:
    pd.DataFrame: DataFrame with added noise.
    """
    logger.info("Adding noise to the dataset.")
    noise = np.random.normal(0, intensity, X.shape)
    return X + noise

def drop_features(X, drop_ratio=0.1):
    """
    Randomly drops a percentage of columns from the DataFrame.
    
    Parameters:
    X (pd.DataFrame): Input DataFrame.
    drop_ratio (float): The ratio of columns to drop.
    
    Returns:
    pd.DataFrame: DataFrame with some columns dropped.
    """
    logger.info("Dropping features from the dataset.")
    columns_to_drop = np.random.choice(X.columns, 
                                        size=int(len(X.columns) * drop_ratio), 
                                        replace=False)
    return X.drop(columns=columns_to_drop)

def drift_features(X, drift_ratio=0.1):
    """
    Shifts feature distributions to simulate data drift.
    
    Parameters:
    X (pd.DataFrame): Input DataFrame.
    drift_ratio (float): The ratio of drift to apply.
    
    Returns:
    pd.DataFrame: DataFrame with drifted features.
    """
    logger.info("Drifting features in the dataset.")
    drift = np.random.normal(0, drift_ratio, X.shape)
    return X + drift

def mutate_dataset(X):
    """
    Sequentially applies noise, drop, and drift to the dataset.
    
    Parameters:
    X (pd.DataFrame): Input DataFrame.
    
    Returns:
    pd.DataFrame: Mutated DataFrame.
    """
    logger.info("Mutating the dataset.")
    X = add_noise(X)
    X = drop_features(X)
    X = drift_features(X)
    return X

def log_memory_note(note: str):
    """
    Logs a note to the project memory using the specified API endpoint.
    
    Parameters:
    note (str): The note to log.
    """
    url = "/api/v1/context/test_open_the_black_box/user-memory"
    payload = {'note': note}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logger.info("Note logged successfully.")
        else:
            logger.error(f"Failed to log note: {response.text}")
    except Exception as e:
        logger.error(f"Error logging note: {str(e)}")
