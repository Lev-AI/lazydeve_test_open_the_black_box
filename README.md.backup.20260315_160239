<p align="center">
  <img src="docs/images/banner.png" alt="Enter The Black Box" width="800"/>
</p>

<h1 align="center">Enter The Black Box</h1>
<h3 align="center">ML Robustness & Security Research Laboratory</h3>

<p align="center">
  <em>Stress-testing ML models against data drift, adversarial mutations & silent failure</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent-LazyDeve-7B68EE?logo=robot&logoColor=white" alt="Built with LazyDeve"/>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/MLflow-Tracking-0194E2?logo=mlflow&logoColor=white" alt="MLflow"/>
  <img src="https://img.shields.io/badge/SHAP-Explainability-blueviolet" alt="SHAP"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
</p>

---

> ⚙️ **Project Note:**
> This project is a special test case created to demonstrate the capabilities of the **LazyDeve Agent**.
> Project planing, the codebase, , documentation, and feature implementation were generated, structured, and committed under the automated supervision of the LazyDeve agent.

https://github.com/Lev-AI/LazyDeve-Agent

---

## 🛡️ Concept: Security Research Lab

> **"Security is not a product, but a process. And AI is the new perimeter."**

Modern cybersecurity relies heavily on Machine Learning. However, hackers know the main weakness of these models: they learn from static patterns. By exploiting this, attackers craft **"Adversarial Examples"** — malicious traffic disguised as normal behavior.

**Enter The Black Box** is a Red Teaming laboratory designed to demonstrate **Model Evasion**. It proves that high Accuracy on a test set is meaningless if the model is brittle to statistical manipulation.

### This project simulates the cyber warfare loop:
1. **Build Defense**: Train a baseline classifier (Random Forest) on network traffic.
2. **Simulate Attack**: Use the **Mutation Engine** to inject noise and corrupt features, mimicking how attackers hide their tracks.
3. **Expose Failure**: Visualize how "State of the Art" models degrade from 90% to 50% accuracy under attack.
4. **Detect Breach**: Use advanced **Drift Detection** (Evidently AI) to catch attacks that bypass the model's logic.

---

## 📸 Laboratory Screenshots

| Main Dashboard | Attack Lab | Drift Report |
|:-:|:-:|:-:|
| ![Dashboard](docs/images/dashboard_main.png) | ![Attack Lab](docs/images/attack_lab.png) | ![Drift](docs/images/drift_report.png) |

---

## 🎯 Key Features

| | Feature | Description |
|---|---|---|
| :shield: | **Baseline Training** | Train RandomForest or XGBoost classifiers. All metrics (Accuracy, F1, Precision) are automatically logged to MLflow. |
| :crossed_swords: | **Mutation Engine** | Three attack modes: **Noise** (injection), **Zeroing** (sensor failure/evasion), **Swap** (protocol mismatch). Adjustable intensity. |
| :rotating_light: | **Drift Detection** | Integration of **Evidently AI** (`DataDriftPreset`) to generate professional HTML reports on statistical data shifts. |
| :chart_with_downwards_trend: | **Explainability (X-Ray)** | Uses **SHAP** (TreeExplainer) to X-ray the model: revealing exactly which features drove the AI's decision. |
| :bar_chart: | **Interactive Dashboard** | Full Streamlit UI: Data & Baseline → Attack Lab → X-Ray → Drift Monitor. Run experiments without writing code. |
| :clipboard: | **Automated Reports** | Automatic generation of experiment artifacts and datasets. |

---

## 🚀 Quick Start

The entire environment can be deployed in minutes.

### 1. Clone & Install

```bash
git clone https://github.com/Lev-AI/lazydeve_test_open_the_black_box.git
cd lazydeve_test_open_the_black_box
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

The LazyDeve agent created a generator to create "Laboratory Quality" data for testing:

```bash
python src/generate_synthetic.py
```

Creates `data/synthetic_data.csv` — a balanced dataset for experiments.

### 3. Launch Dashboard

```bash
streamlit run src/dashboard.py
```

Windows users can simply use the one-click launcher:

```bash
run_dashboard.bat
```

---

## 🏗️ Project Architecture (LazyDeve Structure)

The project follows the Onion Architecture principle enforced by the agent, separating core logic, data handling, and UI layers.

```
enter-the-black-box/
│
├── src/                        # Core Logic
│   ├── data_loader.py          # Data loading & Preprocessing
│   ├── baseline_model.py      # Training logic (RF/XGB)
│   ├── mutation_engine.py      # Attack Logic (Noise, Zeroing, Swap)
│   ├── drift_detector.py      # Evidently AI Integration
│   ├── robustness_eval.py     # Metric comparison logic
│   ├── explainability.py      # SHAP visualization
│   ├── report_generator.py    # Markdown reporting
│   ├── dashboard.py           # Streamlit UI (4 Tabs)
│   └── generate_synthetic.py  # Data Generator
│
├── notebooks/                  # Jupyter Notebooks for Analysis
│   ├── 01_baseline.ipynb
│   ├── 02_mutations.ipynb
│   ├── 03_drift_tests.ipynb
│   └── 04_shap_analysis.ipynb
│
├── data/                       # Datasets (CIC-IDS2017 / Synthetic)
├── docs/                       # Documentation & Assets
├── mlruns/                     # MLflow Experiment Logs
├── run_dashboard.bat           # Quick Launcher
└── README.md
```

---

## ⚙️ How It Works (Pipeline)

```
 Dataset ──► Data Loader ──► Baseline Training ──► Trained Model
                                                        │
                              ┌──────────────────────────┤
                              ▼                          ▼
                      Mutation Engine            SHAP Explainer
                     (Noise/Zero/Swap)           (feature X-Ray)
                              │
                              ▼
                   Drift Detector (Evidently + Alibi)
                              │
                              ▼
                    Robustness Evaluator
                     (Δ accuracy, Δ F1)
                              │
                              ▼
                   Report Generator ──► MLflow + Markdown
```

---

## 📘 Roadmap (Status)

| Phase | Status | Scope |
|-------|--------|-------|
| **MVP** | :white_check_mark: Complete | Baseline, Mutation Engine, Drift Detection, Dashboard |
| **Phase 2** | :white_check_mark: Complete | Streamlit UI, MLflow integration, Reporting |
| **Phase 3** | :construction: Planned | Synthetic attack generation (GAN/VAE), Adversarial ML |
| **Phase 4** | :construction: Planned | Real-time monitoring, Zeek/Suricata log integration |

---

## 👤 Credits

<p align="center">
  <strong>Created & Engineered by LazyDeve Agent</strong> 🤖<br/>
  <em>Under the supervision of Kapitan Lev ⚓</em>
</p>

<p align="center">
  AI-powered Cyber Analyst & ML Researcher<br/>
  License: MIT — free for education and research.
</p>
