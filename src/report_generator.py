"""
This module generates reports based on the analysis.
"""
import logging
import mlflow

logger = logging.getLogger(__name__)

def log_experiment_to_mlflow(params, metrics, model=None, artifacts=None):
    """
    Logs parameters, metrics, and optional model/plots to MLflow.

    Args:
        params (dict): Parameters used in the experiment.
        metrics (dict): Metrics obtained from the experiment.
        model (optional): The model object to log.
        artifacts (optional): Artifacts to log.

    Raises:
        Exception: If logging fails.
    """
    try:
        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            if model:
                mlflow.sklearn.log_model(model, "model")
            if artifacts:
                for artifact in artifacts:
                    mlflow.log_artifact(artifact)
        logger.info("Experiment logged to MLflow successfully.")
    except Exception as e:
        logger.error(f"Failed to log experiment to MLflow: {e}")
        raise

def generate_experiment_report(metrics_ref, metrics_mut, drift_report, robustness_report):
    """
    Compiles a markdown/text report combining all experiment results.

    Args:
        metrics_ref (dict): Reference metrics.
        metrics_mut (dict): Mutated metrics.
        drift_report (str): Report on drift analysis.
        robustness_report (str): Report on robustness analysis.

    Returns:
        str: Compiled report as a string.
    """
    report = "# Experiment Report\n\n"
    report += "## Reference Metrics\n"
    for key, value in metrics_ref.items():
        report += f"- {key}: {value}\n"
    
    report += "\n## Mutated Metrics\n"
    for key, value in metrics_mut.items():
        report += f"- {key}: {value}\n"
    
    report += "\n## Drift Report\n"
    report += drift_report + "\n"
    
    report += "\n## Robustness Report\n"
    report += robustness_report + "\n"
    
    logger.info("Experiment report generated successfully.")
    return report

def save_report(report, path='reports/experiment_report.txt'):
    """
    Saves the report locally.

    Args:
        report (str): The report content to save.
        path (str): The path where the report will be saved.

    Raises:
        Exception: If saving the report fails.
    """
    try:
        with open(path, 'w') as f:
            f.write(report)
        logger.info(f"Report saved successfully at {path}.")
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        raise
