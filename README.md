# 🧠 Enter The Black Box

A Machine Learning Robustness Lab for Evolving Cyber Attacks
(Stress-Testing ML Models for Cybersecurity Drift, Mutation & Resilience)

---

## ⭐ Overview
Enter The Black Box — это исследовательская ML-платформа, созданная для анализа устойчивости (robustness) моделей кибербезопасности к изменяющимся паттернам атак.

Проект показывает:
- как изменения трафика или логов ломают ML-модель,
- какие признаки критичны,
- как растут False Negatives / False Positives,
- где модель становится слепой,
- как ведёт себя при data drift, noise injection, adversarial perturbations.

Это не просто IDS-модель.
Это лаборатория, которая помогает понять, насколько хрупки ML-решения в кибербезопасности — и как их улучшать.

---

## 🎯 Key Features
- Baseline ML-модель IDS (RandomForest/XGBoost)
- Attack Mutation Engine (drop features, add noise, create drift, mutate patterns)
- Data Drift Detection (Evidently AI, Alibi Detect)
- Concept Drift Detection
- Adversarial Sample Simulation (простые perturbations)
- Robustness Scoring & Metrics Comparison
- Explainability (SHAP) — выявляет, какие признаки ломают модель
- Interactive Streamlit Dashboard
- MLflow Experiment Tracking
- Clear reports for SOC / Threat Research teams

---

## 🔬 Why This Project Is Important
Современные IDS/NDR системы всё чаще включают ML. Но почти никто не тестирует:
- как модель ведёт себя под дрейфом данных
- видит ли она новые атаки, слегка отличающиеся
- что произойдёт при повреждении логов
- какие признаки являются “single points of failure”
- где модель начинает делать опасные False Negatives

Этот проект помогает увидеть слабые места ML-моделей безопасности.

---

## 🏗 Architecture
```
Enter-The-Black-Box/
│
├── data/                     # Datasets (CIC-IDS2017 / UNSW-NB15)
│
├── src/
│   ├── data_loader.py        # Загрузка и очистка данных
│   ├── baseline_model.py     # RandomForest/XGBoost baseline
│   ├── mutation_engine.py    # Уникальный модуль изменения паттернов
│   ├── drift_detector.py     # Evidently + Alibi Detect
│   ├── robustness_eval.py    # Сравнение baseline vs mutated
│   ├── explainability.py     # SHAP графики
│   ├── report_generator.py   # Автоматические отчёты
│   └── dashboard.py          # Streamlit интерфейс
│
├── notebooks/
│   ├── 01_baseline.ipynb
│   ├── 02_mutations.ipynb
│   ├── 03_drift_tests.ipynb
│   └── 04_shap_analysis.ipynb
│
├── mlruns/                   # Логи MLflow (авто-создаётся)
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Core Components
### 🔥 1. Attack Mutation Engine
Симулирует изменения паттернов атак: удаление признаков, добавление шума, мутации портов и создание новых атак.

### 📈 2. Drift Detection Layer
Использует **Evidently AI** и **Alibi Detect** для анализа дрейфа и adversarial detection.

### 🤖 3. ML Baseline
Модели **RandomForest** или **XGBoost**, обучаемые на **CIC-IDS2017** или **UNSW-NB15**.

### 🧠 4. Explainability (SHAP)
SHAP помогает визуализировать влияние признаков и причины ошибок модели.

### 📊 5. Streamlit Dashboard
Интерактивный интерфейс для тестирования сценариев мутаций и визуализации результатов.

### 📜 6. MLflow Logging
Хранит метрики, параметры и результаты экспериментов.

---

## 🚀 How It Works (Workflow)
1. Load dataset (CIC-IDS2017 / UNSW)
2. Train baseline model
3. Run mutation scenario
4. Re-evaluate model
5. Detect drift
6. Explain errors (SHAP)
7. Generate report
8. Visualize results через Streamlit

---

## 📊 Example Use Cases
- Проверка ML-модели на устойчивость
- Оценка готовности IDS к новым атакам
- Анализ слабых мест detection-pipeline
- Исследование adversarial-атак
- Создание whitepaper или R&D отчёта

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
**MVP (1–2 недели)**
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
MIT — свободно для обучения и исследований.

---

## ✉️ Contact
Created by **Kapitan Lev ⚓**  
AI-powered Cyber Analyst & ML Researcher