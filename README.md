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

**Data:** Prefer UCI **South German Credit UPDATE** (dataset 573). Use `data/raw/SouthGermanCredit.asc` and/or `data/raw/south_german_credit.csv` (see [`docs/DATA_PROVENANCE.md`](docs/DATA_PROVENANCE.md)). If neither is present, training falls back to OpenML **credit-g**; check MLflow `data_provenance`.

**Governance gates:** **Fairness** — `src/gate_fairness.py` (equalized odds vs `gates.fairness.max_equalized_odds_difference`). **SHAP** — `src/gate_shap.py` → `artifacts/shap_report.md`. Run full pipeline: `dvc repro`. CI mirrors this in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

Tracking: MLflow UI → `mlruns/` (see `params.yaml` → `mlflow.tracking_uri`).  
**Plan & status:** [`PROJECT_PLAN.md`](PROJECT_PLAN.md).

## Rules

Project rules live in `.cursor/rules/` (Dr. Ingrid Voss persona for DSR/compliance tone).
