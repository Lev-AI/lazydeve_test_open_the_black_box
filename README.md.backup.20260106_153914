# 🧠 Enter The Black Box

A Machine Learning Robustness Lab for Evolving Cyber Attacks
(Stress-Testing ML Models for Cybersecurity Drift, Mutation & Resilience)

---

## 🚀 Overview
**Enter The Black Box** is a modular research platform designed to analyze and improve the **robustness of ML-based cybersecurity models**. It enables testing how intrusion detection systems (IDS/NDR) behave under **data drift, adversarial noise, and feature corruption**.

---

## 🧩 Key Capabilities
- **Baseline Training** — Train ML models (RandomForest, XGBoost) on IDS datasets like NSL-KDD.
- **Attack Mutation Engine** — Simulate adversarial noise, drift, and missing features.
- **Drift Detection** — Detect and visualize data drift using Evidently AI and Alibi Detect.
- **Robustness Evaluation** — Measure performance degradation between baseline and mutated datasets.
- **Explainability** — Understand feature importance and model behavior with SHAP.
- **Visualization Tools** — Static (Matplotlib) and interactive (Streamlit) dashboards for analysis.
- **Experiment Tracking** — Full MLflow integration for logging models, metrics, and reports.

---

## 🏗 Project Structure
```
Enter-The-Black-Box/
│
├── data/                     # Datasets
├── src/
│   ├── data_loader.py        # Dataset loading and preprocessing
│   ├── baseline_model.py     # Baseline model training and evaluation
│   ├── mutation_engine.py    # Data mutation and drift simulation
│   ├── drift_detector.py     # Evidently + Alibi drift detection
│   ├── robustness_eval.py    # Compare baseline vs mutated results
│   ├── explainability.py     # SHAP explainability
│   ├── report_generator.py   # MLflow report generation
│   ├── dashboard.py          # Streamlit dashboard
│   ├── run_experiment.py     # Full automation pipeline
│   └── visualize_results.py  # Offline result visualization
│
├── notebooks/                # Jupyter notebooks for experiments
│   ├── 01_baseline.ipynb
│   ├── 02_mutations.ipynb
│   ├── 03_drift_tests.ipynb
│   └── 04_shap_analysis.ipynb
│
├── outputs/                  # Generated reports and plots
├── mlruns/                   # MLflow tracking logs
├── requirements.txt          # Dependencies
└── README.md
```

---

## ⚙️ How to Use

### 🧠 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 📊 2. Run an Automated Experiment
```bash
python src/run_experiment.py --data data/KDDTest+.arff --model rf
```

This will:
1. Load and preprocess the dataset.
2. Train a baseline model.
3. Mutate the data (noise, drift, feature drop).
4. Evaluate drift and robustness.
5. Compute SHAP explainability.
6. Generate and save experiment reports and plots in `outputs/`.

### 🖥️ 3. Launch Streamlit Dashboard
```bash
streamlit run src/dashboard.py
```
Explore the full lab visually — upload data, mutate it, visualize SHAP, and generate reports.

### 📈 4. Visualize Saved Results
```bash
python src/visualize_results.py
```
Displays saved performance charts, drift summaries, and SHAP plots.

---

## 🧪 Supported Datasets
- NSL-KDD (KDDTrain+, KDDTest+.arff)
- CIC-IDS2017 *(planned Phase 2)*
- UNSW-NB15 *(planned Phase 2)*

---

## 📘 Roadmap
**Phase 1 (✅ Done):** Core pipeline, dashboards, and drift analysis.  
**Phase 2 (🚧 Next):** Modern IDS datasets (CIC-IDS2017, UNSW-NB15).  
**Phase 3 (🔬 Planned):** Adversarial sample generation (GAN/VAE).  
**Phase 4 (☁️ Planned):** Real-time drift monitoring and deployment.

---

## 📄 License
MIT — Free for education and research.

---

## ✉️ Contact
Created by **Kapitan Lev ⚓**  
AI-powered Cyber Analyst & ML Researcher