"""
This module provides explainability for the model predictions using SHAP.
"""

import shap
import matplotlib.pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def compute_shap_values(model, X_sample):
    """
    Compute SHAP values for a sample of data.

    Parameters:
    model: Trained model for which SHAP values are to be computed.
    X_sample: DataFrame containing the sample data.

    Returns:
    shap_values: SHAP values for the sample data.
    """
    try:
        explainer = shap.Explainer(model)
        shap_values = explainer(X_sample)
        logger.info("SHAP values computed successfully.")
        return shap_values
    except Exception as e:
        logger.error(f"Error computing SHAP values: {e}")
        raise

def plot_shap_summary(shap_values, X_sample):
    """
    Create SHAP summary plot.

    Parameters:
    shap_values: SHAP values to be plotted.
    X_sample: DataFrame containing the sample data.
    """
    try:
        shap.summary_plot(shap_values, X_sample)
        logger.info("SHAP summary plot created successfully.")
    except Exception as e:
        logger.error(f"Error creating SHAP summary plot: {e}")
        raise

def generate_feature_importance(model, X_train):
    """
    Extract and plot feature importances for tree-based models.

    Parameters:
    model: Trained tree-based model.
    X_train: DataFrame containing the training data.
    """
    try:
        if hasattr(model, 'feature_importances_'):
            feature_importances = model.feature_importances_
            feature_names = X_train.columns
            importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
            importance_df = importance_df.sort_values(by='Importance', ascending=False)

            plt.figure(figsize=(10, 6))
            plt.barh(importance_df['Feature'], importance_df['Importance'])
            plt.xlabel('Importance')
            plt.title('Feature Importance')
            plt.show()
            logger.info("Feature importance plot created successfully.")
        else:
            logger.warning("The model does not have feature importances.")
    except Exception as e:
        logger.error(f"Error generating feature importance: {e}")
        raise
