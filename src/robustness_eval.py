"""
This module evaluates the robustness of the model.
"""
import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)

def evaluate_robustness(model, X_ref, y_ref, X_mut, y_mut):
    """
    Evaluate the model on reference and mutated datasets.

    Parameters:
    model: The model to evaluate.
    X_ref: Features of the reference dataset.
    y_ref: Labels of the reference dataset.
    X_mut: Features of the mutated dataset.
    y_mut: Labels of the mutated dataset.

    Returns:
    dict: A dictionary containing metrics for both datasets.
    """
    logger.info("Evaluating robustness of the model.")
    
    # Evaluate on reference dataset
    y_pred_ref = model.predict(X_ref)
    metrics_ref = {
        'accuracy': accuracy_score(y_ref, y_pred_ref),
        'precision': precision_score(y_ref, y_pred_ref, average='weighted'),
        'recall': recall_score(y_ref, y_pred_ref, average='weighted'),
        'f1': f1_score(y_ref, y_pred_ref, average='weighted')
    }
    
    # Evaluate on mutated dataset
    y_pred_mut = model.predict(X_mut)
    metrics_mut = {
        'accuracy': accuracy_score(y_mut, y_pred_mut),
        'precision': precision_score(y_mut, y_pred_mut, average='weighted'),
        'recall': recall_score(y_mut, y_pred_mut, average='weighted'),
        'f1': f1_score(y_mut, y_pred_mut, average='weighted')
    }
    
    return metrics_ref, metrics_mut

def compute_robustness_score(metrics_ref, metrics_mut):
    """
    Compute degradation percentage for each metric.

    Parameters:
    metrics_ref: Metrics from the reference dataset.
    metrics_mut: Metrics from the mutated dataset.

    Returns:
    dict: A dictionary containing degradation percentages for each metric.
    """
    logger.info("Computing robustness score.")
    degradation = {}
    for key in metrics_ref.keys():
        degradation[key] = ((metrics_ref[key] - metrics_mut[key]) / metrics_ref[key]) * 100 if metrics_ref[key] > 0 else 0
    return degradation

def generate_robustness_report(metrics_ref, metrics_mut):
    """
    Summarize degradation in JSON-style dict for logging and reporting.

    Parameters:
    metrics_ref: Metrics from the reference dataset.
    metrics_mut: Metrics from the mutated dataset.

    Returns:
    dict: A summary report of the robustness evaluation.
    """
    logger.info("Generating robustness report.")
    degradation = compute_robustness_score(metrics_ref, metrics_mut)
    report = {
        'reference_metrics': metrics_ref,
        'mutated_metrics': metrics_mut,
        'degradation': degradation
    }
    return report
