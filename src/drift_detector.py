"""
This module detects data drift using Evidently and Alibi Detect.
"""

import json
import logging
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from alibi_detect.cd import MMDDrift

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        column_mapping = ColumnMapping()
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=X_ref, current_data=X_new, column_mapping=column_mapping)
        drift_summary = report.as_dict()
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
    - X_new: New dataset (Pandas DataFrame).

    Returns:
    - A JSON-serializable drift score and p-value.
    """
    try:
        mmd = MMDDrift(X_ref, X_new)
        drift_score = mmd.get_drift_score()
        p_value = mmd.get_p_value()
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
