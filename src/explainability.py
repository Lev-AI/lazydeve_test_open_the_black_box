"""
This module provides explainability for the model predictions using SHAP.
"""

import numpy as np
import shap
import matplotlib.pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Reproducible RNG (avoids deprecated np.random.seed; pass explicitly where needed)
DEFAULT_SEED = 42
_rng = np.random.default_rng(DEFAULT_SEED)


def compute_shap_values(model, X_sample, seed=None):
    """
    Compute SHAP values for a sample of data.

    Parameters:
    model: Trained model for which SHAP values are to be computed.
    X_sample: DataFrame containing the sample data.
    seed: Optional int for reproducibility; uses module default if None.

    Returns:
    shap_values: SHAP values for the sample data.
    """
    try:
        # Use explicit RNG for reproducibility (avoids deprecated np.random.seed)
        rng = np.random.default_rng(seed if seed is not None else DEFAULT_SEED)
        # Pass seed for SHAP reproducibility; rng= avoids np.random.seed FutureWarning where supported
        explainer = shap.Explainer(model, X_sample, seed=DEFAULT_SEED)
        shap_values = explainer(X_sample)
        logger.info("SHAP values computed successfully.")
        return shap_values
    except Exception as e:
        logger.error(f"Error computing SHAP values: {e}")
        raise

def plot_shap_summary(shap_values, X_sample, rng=None):
    """
    Create SHAP summary plot.

    Parameters:
    shap_values: SHAP values to be plotted.
    X_sample: DataFrame containing the sample data.
    rng: Optional numpy random Generator for reproducibility; uses module default if None.
    """
    try:
        if rng is None:
            rng = _rng
        shap.summary_plot(shap_values, X_sample, rng=rng)
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
