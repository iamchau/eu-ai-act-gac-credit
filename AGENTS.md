# Agent context — EU AI Act GaC thesis

- **Documentation charter:** `docs/DOCUMENTATION_FOUNDATION.md` — precedence when docs disagree; MLflow/Gate C/metrics truths; maintenance triggers.
- **Thesis writing voice:** `.cursor/rules/thesis-excellence-mentor.mdc` — examiner-grade structure and prose; **`alwaysApply: true`** (works **with** Dr. Voss; compliance still wins on substance).
- **Goal:** Working MLOps instantiation with Governance-as-Code (fairness + explainability + human-oversight gates) vs a standard pipeline; DSR evaluation.
- **Data:** South German Credit Dataset (sensitive attributes for bias testing).
- **Non-goals:** Do not invent EU article text; cite or quote official sources when making legal claims.
- **Traceability:** Prefer MLflow run IDs, DVC revisions, and CI logs over undocumented claims.
- **Plan:** Read and update `PROJECT_PLAN.md` after substantive tasks (completed / next / current focus).
- **Thesis (≥50 pp., Word + tables/figures):** Draft body in `docs/thesis/MANUSCRIPT.md` (Pandoc → Word per `docs/thesis/README.md`); start from `docs/THESIS_WRITING_HUB.md`; spine `docs/THESIS_FOUNDATION.md`; figures under `docs/figures/`.
- **Gates:** A Fairness (`gate_fairness.py`), B SHAP (`gate_shap.py`); thresholds in `params.yaml` under `gates.*`. Gate C is **GitHub Environment** `model-governance` + `governed_deploy.yml` (latency JSON).
- **Profiles:** `pipeline.profile` or `PIPELINE_PROFILE` = `standard` (train only) vs `governed` (full GaC); see `docs/compare_pipelines.md`.
