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

See `requirements.txt` (to be added) and project rules in `.cursor/rules/`.
