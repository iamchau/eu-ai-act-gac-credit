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

**Data:** Prefer UCI **South German Credit UPDATE** (dataset 573). Use `data/raw/SouthGermanCredit.asc` and/or `data/raw/south_german_credit.csv` (see [docs/DATA_PROVENANCE.md](docs/DATA_PROVENANCE.md)). If neither is present, training falls back to OpenML **credit-g**; check MLflow `data_provenance`.

**Pipelines:** **Standard** = train only (performance baseline). **Governed** = train + fairness + SHAP. See [docs/compare_pipelines.md](docs/compare_pipelines.md). Set `pipeline.profile` in `params.yaml` or `PIPELINE_PROFILE=standard|governed` for CI/local.

**Governance gates:** **A Fairness** — `src/gate_fairness.py`. **B SHAP** — `src/gate_shap.py` → `artifacts/shap_report.md`. **C Human oversight** — GitHub Environment `model-governance` + [governed_deploy.yml](.github/workflows/governed_deploy.yml) (latency JSON). Setup: [docs/human_oversight.md](docs/human_oversight.md).

Run full local pipeline: `dvc repro`. CI: [.github/workflows/ci.yml](.github/workflows/ci.yml) runs **both** profiles in a matrix.

Tracking: MLflow UI → `mlruns/` (see `params.yaml` → `mlflow.tracking_uri`).  
**P3 experiment (local):** `python scripts/compare_profiles.py` → [metrics/experiment_comparison.json](metrics/experiment_comparison.json).

**GitHub / Gate C:** [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md) · **Troubleshoot governed-deploy:** [docs/GATE_C_RUNBOOK.md](docs/GATE_C_RUNBOOK.md) · **Thesis eval notes:** [docs/THESIS_EVAL_NOTES.md](docs/THESIS_EVAL_NOTES.md) · **Thesis spine (RQs, DSR, scope):** [docs/THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md).

**Foundation:** MLflow **SQLite** store (`mlflow.db`); run context (**git**, **params**, **dvc.lock** digests) on each train. Lockfile: [requirements.lock.txt](requirements.lock.txt). **Compliance map:** [docs/COMPLIANCE_MATRIX.md](docs/COMPLIANCE_MATRIX.md). **Sub-RQ1 policy demo:** [docs/SUB_RQ1_DEMO.md](docs/SUB_RQ1_DEMO.md).

**Thesis writing:** [docs/THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) (positioning, RQ answers, limitations) · [docs/EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md) · [docs/THESIS_CUT_LIST.md](docs/THESIS_CUT_LIST.md).

**Plan & status:** [PROJECT_PLAN.md](PROJECT_PLAN.md) · **Review log:** [docs/DR_VOSS_REVIEW_LOG.md](docs/DR_VOSS_REVIEW_LOG.md).

## Rules

Project rules live in `.cursor/rules/` (Dr. Ingrid Voss persona for DSR/compliance tone).
