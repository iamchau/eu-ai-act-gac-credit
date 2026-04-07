# EU AI Act Governance-as-Code (GaC) — Credit Scoring

Design Science Research (DSR) thesis artifact: MLOps pipeline with fairness (Fairlearn), explainability (SHAP), and human-oversight gates (CI/CD), evaluated against a standard performance-only pipeline.

## Stack (target)

- Python, MLflow, DVC  
- South German Credit Dataset  
- GitHub Actions (gates)  

## Layout

| Path | Purpose |
|------|---------|
| `docs/` | Thesis source (Markdown/LaTeX) and figures |
| `src/` | Training, evaluation, gate scripts |
| `pipelines/` | CI workflow definitions and pipeline orchestration |
| `data/` | Raw data (gitignored); DVC-tracked artifacts |

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
dvc init   # once
# Training (either):
.venv\Scripts\python.exe src\train.py
dvc repro  # uses .venv\Scripts\python.exe from dvc.yaml (Windows)
```

**Data:** Put the South German Credit UPDATE CSV at `data/raw/south_german_credit.csv` and document the source in your thesis. If that file is missing, `train.py` falls back to OpenML **credit-g** (Statlog German Credit, ~1000 rows) for pipeline development—log `data_provenance` in MLflow and switch to the thesis CSV for reported experiments.

Tracking: MLflow UI → `mlruns/` (see `params.yaml` → `mlflow.tracking_uri`).  
**Plan & status:** [`PROJECT_PLAN.md`](PROJECT_PLAN.md).

## Rules

Project rules live in `.cursor/rules/` (Dr. Ingrid Voss persona for DSR/compliance tone).
