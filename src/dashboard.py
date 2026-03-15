"""
Streamlit dashboard for Enter The Black Box: Robustness Lab.
Works with only synthetic_data.csv in data/.
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path so `from src.…` works regardless of CWD
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Project root (parent of src/)
ROOT = _PROJECT_ROOT
CSV_PATH = ROOT / "data" / "synthetic_data.csv"


def load_synthetic_data():
    """Load and preprocess synthetic_data.csv if it exists."""
    if not CSV_PATH.exists():
        return None, None, None, None, None
    from src.data_loader import load_data, preprocess_data, split_data
    df = load_data(str(CSV_PATH))
    df = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(df)
    return df, X_train, X_test, y_train, y_test


def get_shap_summary_figure(model, X_sample):
    """Compute SHAP values and return matplotlib figure for summary plot."""
    import matplotlib.pyplot as plt
    from src.explainability import compute_shap_values
    shap_values = compute_shap_values(model, X_sample)
    # summary_plot creates its own figure
    import shap
    shap.summary_plot(shap_values, X_sample, show=False)
    fig = plt.gcf()
    return fig


def main():
    st.set_page_config(page_title="Robustness Lab", layout="wide")
    st.title("Enter The Black Box: Robustness Lab")

    # ----- Lab Passport (Header Section) -----
    with st.container():
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                border-radius: 8px;
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;
                border-left: 4px solid #3b82f6;
                color: #e2e8f0;
                font-size: 0.95rem;
                line-height: 1.6;
            ">
            <strong style="color: #93c5fd;">Lab Passport</strong>
            <ul style="margin: 0.5rem 0 0 1rem; padding-left: 1rem;">
                <li><strong>Mission:</strong> Stress-test ML models against adversarial attacks & data drift.</li>
                <li><strong>Dataset Used:</strong> Synthetic Emulation of CIC-IDS2017 (Network Traffic).</li>
                <li><strong>Model Architecture:</strong> Random Forest / XGBoost.</li>
                <li><strong>Attack Vector:</strong> Mutation Engine (Noise, Zeroing, Feature Swapping).</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Engineered by: Lev Kosarev & [LazyDeve Agent](https://github.com/Lev-AI/LazyDeve-Agent) (AI-Assisted R&D demo)."
        )

    # Sidebar
    with st.sidebar:
        st.header("Settings")
        model_type_display = st.selectbox(
            "Select Model Type",
            ["RandomForest", "XGBoost"],
            key="model_type",
        )
        model_type = "rf" if model_type_display == "RandomForest" else "xgb"
        mutation_intensity = st.slider(
            "Mutation Intensity",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.05,
            help="Noise scale or fraction zeroed/swapped.",
        )

    # Load data once
    df, X_train, X_test, y_train, y_test = load_synthetic_data()
    if df is None:
        st.warning(
            f"No data found. Place `synthetic_data.csv` in `data/` (expected: {CSV_PATH})."
        )
        return

    # Session state for model, baseline metrics, and test data (for Attack Lab)
    if "model" not in st.session_state:
        st.session_state.model = None
    if "baseline_accuracy" not in st.session_state:
        st.session_state.baseline_accuracy = None
    if "baseline_f1" not in st.session_state:
        st.session_state.baseline_f1 = None
    st.session_state.X_test = X_test
    st.session_state.y_test = y_test
    if "X_current_mutated" not in st.session_state:
        st.session_state.X_current_mutated = None

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Data & Baseline", "Attack Lab", "X-Ray (Explainability)", "Drift Monitor"]
    )

    # ----- Tab 1: Data & Baseline -----
    with tab1:
        st.subheader("Data & Baseline")
        st.info(
            "**Methodology:** Establish a clean baseline model on trusted traffic data. "
            "Metrics (Accuracy, F1) here represent the *Golden Standard* before attacks."
        )
        st.write("**Raw data stats**")
        st.dataframe(df.head(), use_container_width=True)
        st.caption(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        if st.button("Train Baseline", key="train_baseline"):
            with st.spinner("Training baseline model..."):
                try:
                    from src.baseline_model import train_baseline, evaluate_model
                    model = train_baseline(X_train, y_train, model_type=model_type)
                    metrics = evaluate_model(model, X_test, y_test)
                    st.session_state.model = model
                    st.session_state.baseline_accuracy = metrics["accuracy"]
                    st.session_state.baseline_f1 = metrics["f1"]
                    st.success("Baseline trained.")
                except Exception as e:
                    st.error(f"Training failed: {e}")
                    raise

        if st.session_state.baseline_accuracy is not None:
            st.metric("Accuracy", f"{st.session_state.baseline_accuracy:.2%}")
            st.metric("F1 (weighted)", f"{st.session_state.baseline_f1:.2%}")

    # ----- Tab 2: Attack Lab -----
    with tab2:
        st.subheader("Attack Lab")
        st.info(
            "**Methodology:** Simulate adversarial attacks. "
            "*Noise:* Inject Gaussian noise to confuse decision boundaries. "
            "*Zeroing:* Simulate packet loss or sensor failure. "
            "*Swap:* Emulate protocol mismatch."
        )
        attack_type = st.selectbox(
            "Select Attack Type",
            ["Noise", "Zeroing", "Swap"],
            key="attack_type",
        )
        st.caption(
            "Mutation Intensity (sidebar) controls noise scale or zeroing probability."
        )
        if st.button("Run Attack", key="run_attack"):
            if st.session_state.model is None:
                st.warning("Train a baseline model first (Tab 1).")
            else:
                with st.spinner("Running attack..."):
                    try:
                        from src.robustness_eval import evaluate_robustness, get_mutated_X
                        result = evaluate_robustness(
                            st.session_state.model,
                            st.session_state.X_test,
                            st.session_state.y_test,
                            attack_type,
                            mutation_intensity,
                        )
                        st.session_state.attack_result = result
                        st.session_state.X_current_mutated = get_mutated_X(
                            st.session_state.X_test,
                            attack_type,
                            mutation_intensity,
                        )
                    except Exception as e:
                        st.error(f"Attack evaluation failed: {e}")
                        raise

        if "attack_result" in st.session_state:
            r = st.session_state.attack_result
            st.metric("Original Acc", f"{r['original_accuracy']:.0%}")
            st.metric("Attacked Acc", f"{r['new_accuracy']:.0%}")
            drop_pct = r["drop"]
            drop_str = f"{drop_pct:+.0f}%"
            st.markdown(
                f"**Drop:** <span style='color:red'>{drop_str}</span>",
                unsafe_allow_html=True,
            )

    # ----- Tab 3: X-Ray (Explainability) -----
    with tab3:
        st.subheader("X-Ray (Explainability)")
        st.info(
            "**Methodology:** Explainability module using SHAP (Shapley Additive Explanations). "
            "Reveals which features drove the model's decision."
        )
        if st.button("Explain with SHAP", key="explain_shap"):
            if st.session_state.model is None:
                st.warning("Train a baseline model first (Tab 1).")
            else:
                with st.spinner("Computing SHAP (this may take a moment)..."):
                    try:
                        # Use a small sample for speed
                        sample_size = min(100, len(X_train))
                        X_sample = X_train.iloc[:sample_size]
                        fig = get_shap_summary_figure(st.session_state.model, X_sample)
                        st.pyplot(fig)
                        import matplotlib.pyplot as plt
                        plt.close(fig)
                    except Exception as e:
                        st.error(f"SHAP failed: {e}")
                        raise

    # ----- Tab 4: Drift Monitor -----
    with tab4:
        st.subheader("Drift Monitor")
        st.info(
            "**Methodology:** Analyze statistical deviation using Kolmogorov–Smirnov tests (Evidently AI). "
            "Detects when data distribution shifts significantly from the training set."
        )
        # Reference = X_train (baseline); Current = mutated from Attack Lab or X_test
        reference_data = X_train
        current_data = (
            st.session_state.X_current_mutated
            if st.session_state.X_current_mutated is not None
            else X_test
        )
        st.caption(
            "Reference: training data (baseline). Current: last attacked data from Attack Lab, or test data if no attack ran yet."
        )
        if st.button("Analyze Drift", key="analyze_drift"):
            with st.spinner("Running drift detection..."):
                try:
                    from src.drift_detector import detect_drift
                    drift_detected, report_html = detect_drift(
                        reference_data, current_data
                    )
                    st.session_state.drift_detected = drift_detected
                    st.session_state.drift_report_html = report_html
                except Exception as e:
                    st.error(f"Drift analysis failed: {e}")
                    raise

        if "drift_detected" in st.session_state and "drift_report_html" in st.session_state:
            if st.session_state.drift_detected:
                st.metric("Status", "🔴 DRIFT DETECTED")
            else:
                st.metric("Status", "🟢 Stable")
            st.markdown("---")
            st.markdown("**Evidently Report**")
            components.html(
                st.session_state.drift_report_html,
                height=1000,
                scrolling=True,
            )


if __name__ == "__main__":
    main()
