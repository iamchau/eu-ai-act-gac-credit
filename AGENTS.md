# Agent context — EU AI Act GaC thesis

- **Goal:** Working MLOps instantiation with Governance-as-Code (fairness + explainability + human-oversight gates) vs a standard pipeline; DSR evaluation.
- **Data:** South German Credit Dataset (sensitive attributes for bias testing).
- **Non-goals:** Do not invent EU article text; cite or quote official sources when making legal claims.
- **Traceability:** Prefer MLflow run IDs, DVC revisions, and CI logs over undocumented claims.
- **Plan:** Read and update `PROJECT_PLAN.md` after substantive tasks (completed / next / current focus).
- **Gates:** A Fairness (`gate_fairness.py`), B SHAP (`gate_shap.py`); thresholds in `params.yaml` under `gates.*`. Gate C is **GitHub Environment** `model-governance` + `governed_deploy.yml` (latency JSON).
- **Profiles:** `pipeline.profile` or `PIPELINE_PROFILE` = `standard` (train only) vs `governed` (full GaC); see `docs/compare_pipelines.md`.
