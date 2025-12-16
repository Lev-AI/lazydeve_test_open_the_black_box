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
