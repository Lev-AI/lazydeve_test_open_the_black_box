"""
This module contains the baseline model implementation.
"""

import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_baseline(X_train, y_train, model_type='rf'):
    """
    Train a baseline model.

    Parameters:
    X_train (DataFrame): Training features.
    y_train (Series): Training labels.
    model_type (str): Type of model to train ('rf' for RandomForest, 'xgb' for XGBoost).

    Returns:
    model: Trained model.
    """
    if model_type == 'rf':
        model = RandomForestClassifier()
    elif model_type == 'xgb':
        model = XGBClassifier()
    else:
        raise ValueError("Invalid model_type. Choose 'rf' or 'xgb'.")

    model.fit(X_train, y_train)
    logger.info(f"Trained {model_type} model.")
    
    # Log the model
    mlflow.start_run()
    mlflow.log_param("model_type", model_type)
    mlflow.sklearn.log_model(model, "model")
    mlflow.end_run()

    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model.

    Parameters:
    model: Trained model.
    X_test (DataFrame): Test features.
    y_test (Series): Test labels.

    Returns:
    dict: Dictionary containing accuracy, precision, recall, F1 score, and confusion matrix.
    """
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred)

    logger.info("Model evaluation metrics:")
    logger.info(f"Accuracy: {accuracy}")
    logger.info(f"Precision: {precision}")
    logger.info(f"Recall: {recall}")
    logger.info(f"F1 Score: {f1}")
    logger.info(f"Confusion Matrix:\n{conf_matrix}")

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": conf_matrix
    }
