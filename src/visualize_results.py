import os
import json
import logging
import matplotlib.pyplot as plt
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_experiment_results(report_path='outputs/experiment_report.txt'):
    """Load and parse the experiment report."""
    try:
        with open(report_path, 'r') as f:
            report = f.read()
        logging.info(f"Loaded report from {report_path}")
        return report
    except FileNotFoundError:
        logging.error(f"Report not found at {report_path}")
        return None


def visualize_performance_comparison(perf_path='outputs/performance_comparison.png'):
    """Display saved model performance comparison plot."""
    if os.path.exists(perf_path):
        logging.info(f"Displaying saved performance plot: {perf_path}")
        img = plt.imread(perf_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    else:
        logging.warning(f"Performance comparison plot not found at {perf_path}")


def visualize_drift_summary(drift_json_path='outputs/drift_summary.json'):
    """Visualize drift summary if saved as JSON."""
    if not os.path.exists(drift_json_path):
        logging.warning(f"No drift summary found at {drift_json_path}")
        return

    with open(drift_json_path, 'r') as f:
        drift_data = json.load(f)

    if 'evidently' in drift_data:
        features = list(drift_data['evidently'].get('metrics', {}).keys())
        drift_scores = [v['drift_score'] for v in drift_data['evidently'].get('metrics', {}).values()]

        plt.figure(figsize=(10, 6))
        plt.barh(features, drift_scores)
        plt.xlabel('Drift Score')
        plt.title('Feature Drift Summary (Evidently)')
        plt.show()
    else:
        logging.warning("Drift data format not recognized.")


def visualize_shap_summary(shap_summary_path='outputs/shap_summary.png'):
    """Display SHAP summary visualization if it exists."""
    if os.path.exists(shap_summary_path):
        logging.info(f"Displaying SHAP summary plot: {shap_summary_path}")
        img = plt.imread(shap_summary_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    else:
        logging.warning(f"No SHAP summary found at {shap_summary_path}")


def main():
    logging.info("=== Enter The Black Box: Results Visualization ===")

    # Load experiment report
    report = load_experiment_results()
    if report:
        print("\n===== EXPERIMENT REPORT =====\n")
        print(report[:1500])  # Print preview of report
        print("\n... (truncated) ...\n")

    # Display saved visualizations
    visualize_performance_comparison()
    visualize_drift_summary()
    visualize_shap_summary()


if __name__ == '__main__':
    main()