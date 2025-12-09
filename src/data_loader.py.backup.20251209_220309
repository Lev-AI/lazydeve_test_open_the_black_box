"""
This module is responsible for loading data from various formats including .arff, .csv, and .parquet.
It provides functions to load, preprocess, and split the data for machine learning tasks.
"""

import logging
import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(path):
    """
    Load data from a specified file path. Supports .arff, .csv, and .parquet formats.

    Parameters:
    path (str): The file path to the dataset.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    logging.info(f"Loading data from {path}")
    if path.endswith('.arff'):
        data = arff.loadarff(path)
        df = pd.DataFrame(data[0])
        # Decode byte columns to string
        for col in df.select_dtypes([bytes]).columns:
            df[col] = df[col].str.decode('utf-8')
    elif path.endswith('.csv'):
        df = pd.read_csv(path)
    elif path.endswith('.parquet'):
        df = pd.read_parquet(path)
    else:
        logging.error("Unsupported file format. Please use .arff, .csv, or .parquet.")
        raise ValueError("Unsupported file format.")
    
    logging.info("Data loaded successfully.")
    return df

def preprocess_data(df):
    """
    Preprocess the DataFrame by handling missing values and encoding categorical variables.

    Parameters:
    df (pd.DataFrame): The DataFrame to preprocess.

    Returns:
    pd.DataFrame: The preprocessed DataFrame.
    """
    logging.info("Preprocessing data...")
    # Example preprocessing: fill missing values and encode categorical variables
    df.fillna(method='ffill', inplace=True)
    df = pd.get_dummies(df)
    logging.info("Data preprocessing completed.")
    return df

def split_data(X, y, test_size=0.2):
    """
    Split the data into training and testing sets.

    Parameters:
    X (pd.DataFrame): Features DataFrame.
    y (pd.Series): Target variable.
    test_size (float): Proportion of the dataset to include in the test split.

    Returns:
    tuple: X_train, X_test, y_train, y_test
    """
    logging.info("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    logging.info("Data split completed.")
    return X_train, X_test, y_train, y_test
