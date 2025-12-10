# 🧠 Project Instruction – `test_open_the_black_box`

This document explains in detail how to **set up, understand, and run** your Machine Learning Robustness Lab project step-by-step. It covers everything — from environment preparation to pipeline execution, with simple explanations for why each step matters.

---

## 🏗️ 1. What This Project Does

**Goal:** Build a full automated system to test how robust your ML models are when data changes (drift, noise, or attacks).

It runs these main steps:
1. Load dataset (supports `.csv`, `.arff`, `.parquet`)
2. Train baseline model (RandomForest or XGBoost)
3. Apply mutations to data (noise, drift, feature changes)
4. Detect drift using advanced libraries (`evidently`, `alibi-detect`)
5. Evaluate robustness (compare baseline vs. mutated performance)
6. Compute SHAP-based explainability
7. Generate reports and logs via MLflow
8. Visualize results in Streamlit dashboard

Think of it as your own AI “black box” testing lab.

---

## ⚙️ 2. System Requirements

| Component | Minimum | Recommended | Why It’s Needed |
|------------|----------|--------------|-----------------|
| **Python** | 3.9+ | 3.10+ | Project uses modern ML libraries only available in recent Python versions |
| **RAM** | 8 GB | 16 GB+ | SHAP and drift analysis can be memory-heavy |
| **Disk Space** | 2 GB | 4 GB+ | For MLflow runs, SHAP plots, and reports |
| **OS** | Windows / macOS / Linux | Linux or macOS preferred for Streamlit performance |
| **Internet** | Optional | Only required for installing packages or syncing to GitHub |

---

## 🐍 3. Environment Setup

### Create a Python Virtual Environment
Using a virtual environment keeps dependencies isolated and prevents version conflicts.
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### Install Dependencies
Make sure `pip` is up to date:
```bash
pip install --upgrade pip
```

Then install all necessary packages:
```bash
pip install scikit-learn pandas numpy xgboost shap mlflow matplotlib plotly streamlit evidently alibi-detect
```

💡 *Alternatively:* Use the preconfigured file
```bash
pip install -r requirements.txt
```

---

## 🧱 4. Project Structure

Here’s what each folder and file does:

```
projects/test_open_the_black_box/
├── data/                     # Place your datasets here
├── src/
│   ├── data_loader.py        # Loads and preprocesses data (CSV, ARFF, Parquet)
│   ├── baseline_model.py     # Trains baseline RandomForest/XGBoost model
│   ├── mutation_engine.py    # Creates noisy/mutated datasets to simulate drift
│   ├── drift_detector.py     # Detects drift using Evidently + Alibi Detect
│   ├── robustness_eval.py    # Compares baseline vs. mutated results
│   ├── explainability.py     # Computes SHAP values and plots explainability
│   ├── report_generator.py   # Generates reports & summaries
│   ├── dashboard.py          # Streamlit visualization for results
│   └── run_experiment.py     # Main orchestrator — runs the full pipeline
├── notebooks/                # Optional: step-by-step Jupyter notebooks
├── mlruns/                   # MLflow experiment logs
├── outputs/                  # Saved charts, reports, and logs
└── requirements.txt          # Dependencies list
```

### Why This Structure
- Keeps **logic modular** (each file has one purpose)
- Allows **reusability** — you can replace one module without breaking others
- Makes debugging easier (e.g., test just `mutation_engine.py` independently)

---

## 📦 5. Adding Your Data

### Dataset Location
Place your dataset inside the `data/` folder:
```
projects/test_open_the_black_box/data/KDDTest+.arff
```

### Supported Formats
- `.csv` → Standard comma-separated values
- `.arff` → WEKA/KEEL datasets (used for KDDTest+)
- `.parquet` → Compressed binary tables

### Why ARFF Support Matters
ARFF files store metadata and categorical information directly. The project’s loader automatically converts this into a pandas DataFrame using SciPy.

---

## 🧠 6. Running the Experiment

The `run_experiment.py` script is your **main entry point**.
It runs all modules in sequence — data loading → training → drift detection → explainability → report generation.

### Run Command
```bash
python src/run_experiment.py --data data/KDDTest+.arff --model rf
```

### Parameters
| Argument | Description | Example |
|-----------|--------------|----------|
| `--data` | Path to dataset file (.csv/.arff/.parquet) | `--data data/KDDTest+.arff` |
| `--model` | Model type (`rf` = RandomForest, `xgb` = XGBoost) | `--model xgb` |

---

## 🧩 7. What Happens Internally

### Step-by-Step Breakdown

1. **Dataset Loading**  
   The loader reads `.arff` via SciPy, decodes text columns, and returns a DataFrame.

2. **Preprocessing**  
   - Detects label/target column automatically (`label`, `target`, `class`, or last column)
   - Encodes labels if categorical
   - Converts all features to numeric and fills missing values

3. **Train-Test Split**  
   Randomly splits the data into 80% train / 20% test.

4. **Model Training**  
   Trains a RandomForest or XGBoost model and stores baseline metrics.

5. **Mutation (Data Drift Simulation)**  
   Introduces controlled feature noise to test model stability.

6. **Drift Detection**  
   Uses `Evidently` and `Alibi Detect` to find which features drifted.

7. **Robustness Evaluation**  
   Compares model accuracy, precision, recall, F1 between clean vs. mutated data.

8. **Explainability (SHAP)**  
   Generates SHAP values and summary plots for feature importance.

9. **Reporting & Logging**  
   Saves report and logs results to MLflow. All artifacts (plots, metrics, SHAP summaries) go under `/outputs/`.

10. **Git Sync (optional)**  
    If used with the LazyDeve Agent, every change is automatically committed and pushed to GitHub.

---

## 📊 8. Checking the Results

### Expected Outputs
| Folder | Content |
|---------|----------|
| `/outputs/` | Plots, text reports, visual summaries |
| `/mlruns/` | MLflow experiment metadata and metrics |
| `/data/` | Input datasets |
| `/src/` | All code modules |

### Example Console Output
```
===== Pipeline Summary =====
✔ Loaded dataset: data/KDDTest+.arff (125,973 rows, 42 features)
✔ Trained baseline RandomForest model
✔ Simulated drift on 5 features
✔ Drift detected: 3 significant features
✔ Robustness delta: -4.8% accuracy
✔ SHAP summary generated (outputs/shap_summary.png)
✔ Report saved under /outputs/
```

---

## 📺 9. Streamlit Dashboard

You can visualize the experiment interactively:
```bash
streamlit run src/dashboard.py
```
Then open the local web app in your browser at:
👉 http://localhost:8501

**What You’ll See:**
- Feature drift plots
- SHAP value summary
- Model performance comparison

---

## 🔍 10. Troubleshooting & Tips

| Problem | Likely Cause | Fix |
|----------|---------------|------|
| ImportError (e.g., evidently missing) | Dependency not installed | `pip install evidently alibi-detect` |
| SHAP plot too slow | Large dataset | Use smaller sample or limit features |
| MLflow not logging | No MLflow server running | Use local tracking (default `/mlruns/`) |
| Unicode decode error | ARFF byte columns not decoded | Re-run loader with decoding (already handled) |
| Drift report empty | Small test dataset | Try full dataset or adjust detection threshold |

---

## 🧾 11. Rational Summary

Each module and tool was chosen for practical reasons:

| Module | Why It’s Used |
|---------|---------------|
| **scikit-learn** | Reliable baseline ML framework |
| **xgboost** | High-performance tree model for robustness tests |
| **evidently** | Industry-grade data drift detection |
| **alibi-detect** | Adds statistical and ML-based drift detectors |
| **shap** | Feature explainability for transparency |
| **mlflow** | Experiment tracking and result comparison |
| **streamlit** | Quick visualization dashboard |
| **matplotlib / plotly** | Visual analytics and report charts |

By combining these, the system gives a **complete lifecycle** from dataset ingestion → robustness testing → explainability → visualization.

---

## ✅ 12. Quick Run Recap

1. 🧱 Clone or open the project folder
2. 🐍 Set up virtual environment
3. 📦 Install dependencies
4. 📂 Add dataset to `/data/`
5. 🚀 Run:
   ```bash
   python src/run_experiment.py --data data/KDDTest+.arff --model rf
   ```
6. 📊 Check `/outputs/` for reports
7. 📺 (Optional) Launch Streamlit dashboard

---

## 🏁 13. Final Notes

- The pipeline is modular: you can swap any module (e.g., try different drift detectors)
- All file operations are tracked and Git-synced automatically if running under LazyDeve
- Designed for **educational, research, and production benchmarking**

---

**Maintainer:** @LazyDeve  
**Agent Version:** 6.x (with unified extraction and auto Git sync)  
**Status:** 🟢 Stable & Ready to Run