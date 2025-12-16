import argparse
import logging
import os
import matplotlib.pyplot as plt
import mlflow
import requests

from src import data_loader, baseline_model, mutation_engine, drift_detector, robustness_eval, explainability, report_generator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main(dataset_path: str, model_type: str):
    """Run the full ML robustness pipeline with visualization."""
    os.makedirs('outputs', exist_ok=True)

    logging.info("Loading dataset...")
    df = data_loader.load_data(dataset_path)
    df = data_loader.preprocess_data(df)
    X = df.drop('label', axis=1, errors='ignore')
    y = df.get('label')
    X_train, X_test, y_train, y_test = data_loader.split_data(X, y)

    logging.info("Training baseline model...")
    metrics_ref, model = baseline_model.train_baseline(X_train, y_train, X_test, y_test, model_type)

    logging.info("Applying mutation engine...")
    X_mut = mutation_engine.mutate_dataset(X_test.copy())

    logging.info("Evaluating drift...")
    drift_report = drift_detector.compare_drift(X_test, X_mut)

    logging.info("Evaluating robustness...")
    robustness_report = robustness_eval.generate_robustness_report(
        metrics_ref,
        baseline_model.evaluate_model(model, X_mut, y_test)
    )

    logging.info("Generating SHAP explainability plots...")
    shap_values = explainability.compute_shap_values(model, X_test.sample(min(200, len(X_test))))
    explainability.plot_shap_summary(shap_values, X_test)

    logging.info("Creating and saving experiment report...")
    report = report_generator.generate_experiment_report(
        metrics_ref, metrics_ref, str(drift_report), str(robustness_report)
    )
    report_generator.save_report(report, 'outputs/experiment_report.txt')

    logging.info("Logging experiment to MLflow...")
    mlflow.start_run()
    mlflow.log_params({'model_type': model_type, 'dataset': os.path.basename(dataset_path)})
    mlflow.log_metrics({k: v for k, v in metrics_ref.items() if isinstance(v, (int, float))})
    mlflow.end_run()

    logging.info("Logging memory note...")
    log_memory_note('test_note_phase 4')

    logging.info("Visualizing results...")
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    values_ref = [metrics_ref[m] for m in metrics]
    values_mut = [robustness_report['mutated_metrics'][m] for m in metrics]

    plt.figure(figsize=(8, 5))
    plt.bar(metrics, values_ref, alpha=0.6, label='Baseline')
    plt.bar(metrics, values_mut, alpha=0.6, label='Mutated')
    plt.title('Baseline vs Mutated Model Performance')
    plt.legend()
    plt.savefig('outputs/performance_comparison.png')
    plt.close()

    logging.info("Experiment completed successfully.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Enter The Black Box experiment pipeline.')
    parser.add_argument('--data', type=str, required=True, help='Path to dataset (.arff, .csv, etc.)')
    parser.add_argument('--model', type=str, default='rf', choices=['rf', 'xgb'], help='Model type (rf or xgb)')
    args = parser.parse_args()

    main(args.data, args.model)
