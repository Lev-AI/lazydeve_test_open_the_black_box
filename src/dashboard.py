import streamlit as st
import logging
from src.data_loader import load_data
from src.baseline_model import train_baseline
from src.mutation_engine import add_noise, drop_features, drift_features
from src.drift_detector import detect_drift_evidently, detect_drift_alibi
from src.robustness_eval import evaluate_robustness
from src.explainability import compute_shap_values, plot_shap_summary
from src.report_generator import generate_experiment_report, save_report

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Test Open the Black Box - Experiment Dashboard")

    # Dataset Upload & Loading
    st.header("1. Dataset Upload & Loading")
    uploaded_file = st.file_uploader("Upload ARFF/CSV file", type=["arff", "csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write("Data Loaded Successfully")
        st.dataframe(data)

    # Baseline Model Training
    st.header("2. Baseline Model Training")
    model_type = st.selectbox("Select Model Type", ["RandomForest", "XGBoost"])
    if st.button("Train Model"):
        with st.spinner("Training model..."):
            model = train_baseline(data, model_type=model_type)
            st.success("Model trained successfully!")

    # Mutation Engine
    st.header("3. Mutation Engine")
    if st.button("Apply Noise"):
        mutated_data = add_noise(data)
        st.write("Noise applied to dataset.")
    if st.button("Drop Features"):
        mutated_data = drop_features(data)
        st.write("Features dropped from dataset.")
    if st.button("Drift Features"):
        mutated_data = drift_features(data)
        st.write("Drift applied to dataset.")

    # Drift Detection
    st.header("4. Drift Detection")
    if st.button("Detect Drift Evidently"):
        drift_report_evidently = detect_drift_evidently(data, mutated_data)
        st.write(drift_report_evidently)
    if st.button("Detect Drift Alibi"):
        drift_report_alibi = detect_drift_alibi(data, mutated_data)
        st.write(drift_report_alibi)

    # Robustness Evaluation
    st.header("5. Robustness Evaluation")
    if st.button("Evaluate Robustness"):
        robustness_report = evaluate_robustness(model, data, mutated_data)
        st.write(robustness_report)

    # SHAP Explainability
    st.header("6. SHAP Explainability")
    if st.button("Compute SHAP Values"):
        shap_values = compute_shap_values(model, data)
        plot_shap_summary(shap_values, data)
        st.write("SHAP values computed and plotted.")

    # Experiment Report Display
    st.header("7. Experiment Report Display")
    if st.button("Generate Experiment Report"):
        report = generate_experiment_report(drift_report_evidently, drift_report_alibi, robustness_report)
        save_report(report)
        st.write("Experiment report generated and saved.")

if __name__ == "__main__":
    main()
