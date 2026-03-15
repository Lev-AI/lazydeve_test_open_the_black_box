"""
This module evaluates the robustness of the model.
"""
import logging
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)


def _apply_swap(X, intensity, rng=None):
    """Swap two random columns; intensity unused but kept for API consistency."""
    if rng is None:
        rng = np.random.default_rng(42)
    cols = list(X.columns)
    if len(cols) < 2:
        return X.copy()
    i, j = rng.choice(len(cols), 2, replace=False)
    c1, c2 = cols[i], cols[j]
    out = X.copy()
    out[c1], out[c2] = X[c2].copy(), X[c1].copy()
    return out


def get_mutated_X(X_test, attack_type, intensity):
    """
    Return a mutated copy of X_test (same logic as in evaluate_robustness).
    Useful for drift detection: use this as "current" data vs X_train as reference.
    """
    from src.mutation_engine import apply_noise, apply_zeroing

    X_mut = X_test.copy()
    columns = list(X_test.columns)
    if attack_type == "Noise":
        X_mut = apply_noise(X_mut, columns, intensity)
    elif attack_type == "Zeroing":
        X_mut = apply_zeroing(X_mut, columns, intensity)
    elif attack_type == "Swap":
        X_mut = _apply_swap(X_mut, intensity)
    else:
        raise ValueError(f"Unknown attack_type: {attack_type}")
    return X_mut


def evaluate_robustness(model, X_test, y_test, attack_type, intensity):
    """
    Evaluate the model on original X_test and on a mutated copy.
    Mutation is applied inside this function; Label is never mutated.

    Parameters:
    model: The model to evaluate.
    X_test: Original test features (DataFrame).
    y_test: Test labels.
    attack_type: One of "Noise", "Zeroing", "Swap".
    intensity: Noise scale (Noise), zeroing probability 0–1 (Zeroing), or unused (Swap).

    Returns:
    dict: original_accuracy, new_accuracy, drop (percentage points: new - old, so negative = performance drop).
    """
    logger.info("Evaluating robustness of the model.")

    # Original accuracy
    y_pred_orig = model.predict(X_test)
    original_accuracy = accuracy_score(y_test, y_pred_orig)

    # Mutated X (same logic as get_mutated_X)
    X_mut = get_mutated_X(X_test, attack_type, intensity)

    # Attacked accuracy
    y_pred_mut = model.predict(X_mut)
    new_accuracy = accuracy_score(y_test, y_pred_mut)

    # Drop in percentage points (negative = performance dropped)
    drop = (new_accuracy - original_accuracy) * 100

    return {
        "original_accuracy": original_accuracy,
        "new_accuracy": new_accuracy,
        "drop": drop,
    }

def compute_robustness_score(metrics_ref, metrics_mut):
    """
    Compute degradation percentage for each scalar metric.

    Parameters:
    metrics_ref: Metrics from the reference dataset.
    metrics_mut: Metrics from the mutated dataset.

    Returns:
    dict: A dictionary containing degradation percentages for each metric (scalars only).
    """
    logger.info("Computing robustness score.")
    degradation = {}
    for key in metrics_ref.keys():
        ref_val = metrics_ref[key]
        mut_val = metrics_mut.get(key)
        # Only compute degradation for scalar metrics (skip e.g. confusion_matrix)
        if mut_val is None or getattr(ref_val, "ndim", 0) > 0:
            continue
        try:
            ref_val = float(ref_val)
            mut_val = float(mut_val)
        except (TypeError, ValueError):
            continue
        if ref_val > 0:
            degradation[key] = ((ref_val - mut_val) / ref_val) * 100
        else:
            degradation[key] = 0.0
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
