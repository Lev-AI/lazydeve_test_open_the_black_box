"""
This module detects data drift using Evidently and Alibi Detect.
"""

import json
import logging
import numpy as np
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
from alibi_detect.cd import MMDDrift

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default drift threshold: share of drifted columns >= this means "drift detected"
DEFAULT_DRIFT_SHARE_THRESHOLD = 0.5


def detect_drift(reference_data, current_data):
    """
    Detect data drift using Evidently's DataDriftPreset.

    Parameters:
    - reference_data: Reference (baseline) dataset (pandas DataFrame).
    - current_data: Current dataset to compare (pandas DataFrame).

    Returns:
    - drift_detected (bool): True if drift is detected (share of drifted columns >= threshold).
    - report_html (str): HTML string of the Evidently report for display.
    """
    try:
        report = Report([DataDriftPreset()])
        snapshot = report.run(
            reference_data=reference_data,
            current_data=current_data,
        )
        d = snapshot.dict()
        # First metric is DriftedColumnsCount; value has 'share' (0–1)
        drift_share = 0.0
        for m in d.get("metrics", []):
            if "DriftedColumnsCount" in str(m.get("metric_name", "")):
                val = m.get("value") or {}
                drift_share = float(val.get("share", 0.0))
                break
        drift_detected = drift_share >= DEFAULT_DRIFT_SHARE_THRESHOLD
        report_html = snapshot.get_html_str(as_iframe=False)
        logger.info("Drift detection completed. drift_detected=%s", drift_detected)
        return drift_detected, report_html
    except Exception as e:
        logger.error("Error in detect_drift: %s", e)
        raise


def _align_to_ref(X_new: pd.DataFrame, X_ref: pd.DataFrame) -> np.ndarray:
    """Align X_new to X_ref columns (same order); fill missing with 0. Return numpy array."""
    aligned = X_new.reindex(columns=X_ref.columns, fill_value=0)
    return np.asarray(aligned, dtype=np.float64)


def detect_drift_evidently(X_ref, X_new):
    """
    Detects data drift using Evidently's DataDriftTable.

    Parameters:
    - X_ref: Reference dataset (Pandas DataFrame).
    - X_new: New dataset (Pandas DataFrame).

    Returns:
    - A JSON-serializable summary of drift metrics.
    """
    try:
        report = Report([DataDriftPreset()])
        my_eval = report.run(reference_data=X_ref, current_data=X_new)
        drift_summary = my_eval.dict()
        logger.info("Drift detected using Evidently.")
        return drift_summary
    except Exception as e:
        logger.error(f"Error in detect_drift_evidently: {e}")
        return {"error": str(e)}

def detect_drift_alibi(X_ref, X_new):
    """
    Detects data drift using Alibi Detect's MMDDrift.

    Parameters:
    - X_ref: Reference dataset (Pandas DataFrame).
    - X_new: New dataset (Pandas DataFrame); may have fewer columns (aligned to X_ref).

    Returns:
    - A JSON-serializable drift score and p-value.
    """
    try:
        # Align columns and pass numpy arrays; MMDDrift(x_ref) then .predict(x)
        x_ref = _align_to_ref(X_ref, X_ref)
        x_new = _align_to_ref(X_new, X_ref)
        backend = "pytorch"
        try:
            import torch  # noqa: F401
        except ImportError:
            backend = "tensorflow"
        mmd = MMDDrift(x_ref, backend=backend)
        pred = mmd.predict(x_new)
        # predict returns dict with 'data' containing 'distance' and 'p_val'
        data = pred.get("data", pred)
        drift_score = float(data.get("distance", data.get("distance_threshold", 0.0)))
        p_value = float(data.get("p_val", data.get("p_value", 0.0)))
        logger.info("Drift detected using Alibi Detect.")
        return {"drift_score": drift_score, "p_value": p_value}
    except Exception as e:
        logger.error(f"Error in detect_drift_alibi: {e}")
        return {"error": str(e)}

def compare_drift(X_ref, X_new):
    """
    Compares drift detection results from both Evidently and Alibi Detect.

    Parameters:
    - X_ref: Reference dataset (Pandas DataFrame).
    - X_new: New dataset (Pandas DataFrame).

    Returns:
    - A JSON-serializable report dict containing results from both methods.
    """
    evidently_results = detect_drift_evidently(X_ref, X_new)
    alibi_results = detect_drift_alibi(X_ref, X_new)
    
    report = {
        "evidently": evidently_results,
        "alibi": alibi_results
    }
    
    logger.info("Drift comparison report generated.")
    return report
