# ARCHITECTURE

> **Status:** ACTIVE — Onion Context Layer 0
> **Last updated:** 2025-01-29 (auto-generated from code audit)

---

## Purpose

**Enter The Black Box** is an ML Robustness Research Laboratory. It trains baseline classifiers on cybersecurity datasets (e.g., CIC-IDS2017, UNSW-NB15), systematically mutates input data (noise, feature drop, distribution drift), measures model degradation, detects data drift, and explains predictions via SHAP — producing reproducible experiment reports tracked by MLflow.

---

## Modules

| Module | File | Responsibility |
|--------|------|----------------|
| **Data Loader** | `src/data_loader.py` | Load CSV/ARFF/Parquet, auto-detect label column, encode categoricals, train/test split |
| **Baseline Model** | `src/baseline_model.py` | Train RandomForest or XGBoost classifier, evaluate (accuracy/precision/recall/F1/confusion matrix), log to MLflow |
| **Mutation Engine** | `src/mutation_engine.py` | Apply Gaussian noise, random feature drop, distribution drift to DataFrames. *Contains simulated attack vector — see below* |
| **Drift Detector** | `src/drift_detector.py` | Detect data drift via Evidently (DataDriftPreset) and Alibi Detect (MMDDrift), compare results |
| **Robustness Evaluator** | `src/robustness_eval.py` | Evaluate model on reference vs. mutated data, compute per-metric degradation percentage |
| **Explainability** | `src/explainability.py` | SHAP value computation & summary plots, feature importance bar charts |
| **Report Generator** | `src/report_generator.py` | Compile markdown experiment report, save to disk, log to MLflow |
| **Dashboard** | `src/dashboard.py` | Streamlit UI exposing all pipeline stages interactively |
| **Pipeline Orchestrator** | `src/run_experiment.py` | CLI entry point (`--data`, `--model`) chaining all modules end-to-end |
| **Visualizer** | `src/visualize_results.py` | Load saved reports and render performance comparison charts |

---

## Data Flow

```
┌──────────────┐
│  Raw Dataset  │  (CSV / ARFF / Parquet in data/)
└──────┬───────┘
       │ data_loader.load_data() + preprocess_data()
       ▼
┌──────────────┐
│ Clean DataFrame │ (numeric features + encoded label)
└──────┬───────┘
       │ data_loader.split_data()
       ├─────────────────────────────┐
       ▼                             ▼
  X_train / y_train            X_test / y_test
       │                             │
       │ baseline_model              │
       │   .train_baseline()         │
       ▼                             │
   Trained Model ────────────────────┤
       │                             │
       │                    mutation_engine
       │                      .mutate_dataset(X_test.copy())
       │                             │
       │                             ▼
       │                         X_mutated
       │                             │
       ├──── drift_detector.compare_drift(X_test, X_mutated)
       │                             │
       ├──── robustness_eval.generate_robustness_report(ref, mut)
       │                             │
       ├──── explainability.compute_shap_values(model, X_test)
       │                             │
       ▼                             ▼
  report_generator ◄──── all metrics + drift + robustness
       │
       ├─► outputs/experiment_report.txt
       └─► MLflow tracking (mlruns/)
```

---

## Key Invariants (Non-Negotiable)

1. **Mutation Engine must NOT overwrite original datasets.** All mutations operate on `.copy()` of DataFrames. The orchestrator enforces `mutate_dataset(X_test.copy())`.
2. **LLMs are executors, not sources of truth.** Git repo is authoritative.
3. **Architecture docs take precedence over code.** Decisions are written (ADR), not implied.
4. **Reproducibility seed:** `np.random.seed(42)` is set in `mutation_engine.py` and `split_data()` uses `random_state=42`.
5. **Context is rebuilt from the repository snapshot**, not from chat history.

---

## Simulated Attack Vectors

### SAV-001: `log_memory_note()` — Data Exfiltration Simulation

- **Location:** `src/mutation_engine.py`, lines 80-97
- **Behavior:** Sends an HTTP POST with a `note` payload to the **relative URL** `/api/v1/context/test_open_the_black_box/user-memory`.
- **Verdict: LOW RISK (simulation / dead code)**
  - The URL is a **relative path** (no scheme, no host). `requests.post("/api/v1/...")` will fail with `MissingSchema` exception in any standard environment — it cannot reach an external server.
  - The path pattern (`/api/v1/context/.../user-memory`) resembles an internal MCP / context-management API, not a public exfiltration endpoint.
  - The function is called once in `run_experiment.py` (line 57) with a hardcoded test string `'test_note_phase 4'` — no sensitive data (no model weights, no dataset content, no credentials).
  - The call is wrapped in a try/except that silently logs errors, so pipeline execution is unaffected by its failure.
- **Recommendation:** Keep for research documentation. If live simulation is needed, point to `http://localhost:<port>` explicitly and document in this file.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.x |
| ML Models | scikit-learn (RandomForest), XGBoost |
| Drift Detection | Evidently, Alibi Detect |
| Explainability | SHAP |
| Experiment Tracking | MLflow |
| Dashboard | Streamlit |
| Data Formats | CSV, ARFF (scipy), Parquet |
| Dependencies | `requirements.txt` |

---

## Context Strategy (Onion Model)

| Layer | Content | When Loaded |
|-------|---------|-------------|
| **Layer 0** | `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, latest ADRs | Always |
| **Layer 1** | `git diff` against base branch, changed file contents | On each task |
| **Layer 2** | Callers, references, dependency graph (dynamic expansion) | On demand |

---

## Operating Rules

- Use **meaningful commits** as checkpoints of intent (even if small).
- After each commit: regenerate snapshot (`.mcp/context.xml`).
- Use ADRs (`docs/adr/`) for architectural decisions that change boundaries, invariants, or contracts.
