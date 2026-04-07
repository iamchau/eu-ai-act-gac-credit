# Agent context — EU AI Act GaC thesis

- **Goal:** Working MLOps instantiation with Governance-as-Code (fairness + explainability + human-oversight gates) vs a standard pipeline; DSR evaluation.
- **Data:** South German Credit Dataset (sensitive attributes for bias testing).
- **Non-goals:** Do not invent EU article text; cite or quote official sources when making legal claims.
- **Traceability:** Prefer MLflow run IDs, DVC revisions, and CI logs over undocumented claims.
- **Plan:** Read and update `PROJECT_PLAN.md` after substantive tasks (completed / next / current focus).
- **Gates:** Fairness (`gate_fairness.py`) and SHAP (`gate_shap.py`) must pass for governed deploys; thresholds live in `params.yaml` under `gates.*`.
