# 🧠 Enter The Black Box

A Machine Learning Robustness Lab for Evolving Cyber Attacks
(Stress-Testing ML Models for Cybersecurity Drift, Mutation & Resilience)

---

> ⚙️ *Note: This is a special test project created to demonstrate and test the capabilities of the LazyDeve agent, including synchronization, file management, and AI-assisted development.*

---

## ⭐ Overview
Enter The Black Box is a research ML platform designed to analyze the robustness of cybersecurity models against evolving attack patterns.
It shows:
- how traffic or log changes break ML models
- which features are critical
- how False Negatives / False Positives grow
- where the model becomes blind
- how it behaves under data drift, noise injection, and adversarial perturbations.

This is not just an IDS model — it's a lab that helps understand how fragile ML-based cybersecurity systems can be and how to improve them.

---

## 🏗 Architecture
```
Enter-The-Black-Box/
│
├── data/                     # Datasets (CIC-IDS2017 / UNSW-NB15)
│
├── src/
│   ├── data_loader.py        # Data loading and cleaning
│   ├── baseline_model.py     # RandomForest/XGBoost baseline
│   ├── mutation_engine.py    # Attack pattern mutation module
│   ├── drift_detector.py     # Evidently + Alibi Detect
│   ├── robustness_eval.py    # Baseline vs mutated comparison
│   ├── explainability.py     # SHAP visualizations
│   ├── report_generator.py   # Automatic reports
│   └── dashboard.py          # Streamlit dashboard
│
├── notebooks/
│   ├── 01_baseline.ipynb
│   ├── 02_mutations.ipynb
│   ├── 03_drift_tests.ipynb
│   └── 04_shap_analysis.ipynb
│
├── mlruns/                   # MLflow logs (auto-created)
│
├── README.md
└── requirements.txt
```

---

## 🎯 Key Features
- Baseline ML IDS model (RandomForest/XGBoost)
- Attack Mutation Engine (drop features, add noise, create drift, mutate patterns)
- Data Drift Detection (Evidently AI, Alibi Detect)
- Concept Drift Detection
- Adversarial Sample Simulation
- Robustness Scoring & Metrics Comparison
- Explainability (SHAP)
- Interactive Streamlit Dashboard
- MLflow Experiment Tracking
- Clear reports for SOC / Threat Research teams

---

## 🔬 Why This Project Is Important
Modern IDS/NDR systems increasingly use ML — but very few test:
- how models behave under data drift
- if they detect slightly modified attacks
- what happens with corrupted logs
- which features are single points of failure
- where dangerous False Negatives appear

This project reveals weak points in ML-based security models.

---

## ⚙️ Core Components
### 🔥 1. Attack Mutation Engine
Simulates attack pattern changes — feature removal, noise injection, frequency mutation, or adversarial tweaks.

### 📈 2. Drift Detection Layer
Uses **Evidently AI** and **Alibi Detect** for drift and adversarial detection.

### 🤖 3. ML Baseline
Models: **RandomForest** or **XGBoost**, trained on **CIC-IDS2017** or **UNSW-NB15** datasets.

### 🧠 4. Explainability (SHAP)
Visualizes feature importance and explains model behavior.

### 📊 5. Streamlit Dashboard
Interactive UI to run mutation scenarios and visualize results.

### 📜 6. MLflow Logging
Tracks parameters, metrics, and experiment outcomes.

---

## 🚀 How It Works (Workflow)
1. Load dataset (CIC-IDS2017 / UNSW)
2. Train baseline model
3. Run mutation scenario
4. Re-evaluate model
5. Detect drift
6. Explain errors (SHAP)
7. Generate report
8. Visualize results with Streamlit

---

## 📊 Example Use Cases
- Test ML model robustness
- Evaluate IDS readiness for new attacks
- Analyze detection pipeline weaknesses
- Study adversarial attacks
- Build whitepapers or R&D reports

---

## 👤 For Who This Project Is
- SOC Analysts
- Threat Researchers
- Data Scientists
- Cybersecurity ML Engineers
- Students and Researchers
- Red Teamers
- Anyone studying ML + Cybersecurity

---

## 🛠 Requirements
```
python >= 3.10
scikit-learn
xgboost
pandas
numpy
evidently
alibi-detect
shap
matplotlib
plotly
streamlit
mlflow
```

---

## 📘 Roadmap
**MVP (1–2 weeks)**
- baseline model
- mutation engine
- drift detection
- notebooks

**Phase 2**
- Streamlit dashboard
- MLflow integration

**Phase 3**
- synthetic attack generation
- adversarial ML
- GAN/VAE for attack synthesis

**Phase 4**
- real-time drift detector
- integration with Zeek logs
- integration with Suricata alerts

---

## 📄 License
MIT — free for education and research.

---

## ✉️ Contact
Created by **Kapitan Lev ⚓**  
AI-powered Cyber Analyst & ML Researcher