# Agent context — EU AI Act GaC thesis

- **Lead mandate (thesis):** The user has delegated **lead** on fulfilling the **thesis deliverable** in-repo. The agent **prioritises**: expanding and refining `docs/thesis/MANUSCRIPT.md`, aligning all thesis-facing docs with `docs/THESIS_FOUNDATION.md` and committed `metrics/`, maintaining evidence cross-references, and applying **Dr. Voss** + **Thesis Excellence Mentor** rules. **Out of scope for the agent alone:** formal submission, defence, supervisor relationship, programme-specific bureaucracy, and any guarantee of grade or degree—the student remains accountable to their institution.
- **Documentation charter:** `docs/DOCUMENTATION_FOUNDATION.md` — precedence when docs disagree; MLflow/Gate C/metrics truths; maintenance triggers.
- **Thesis writing voice:** `.cursor/rules/thesis-excellence-mentor.mdc` — examiner-grade structure and prose; **`alwaysApply: true`** (works **with** Dr. Voss; compliance still wins on substance).
- **Goal:** Working MLOps instantiation with Governance-as-Code (fairness + explainability + human-oversight gates) vs a standard pipeline; DSR evaluation.
- **Data:** South German Credit Dataset (sensitive attributes for bias testing).
- **Non-goals:** Do not invent EU article text; cite or quote official sources when making legal claims.
- **Traceability:** Prefer MLflow run IDs, DVC revisions, and CI logs over undocumented claims.
- **Plan:** Read and update `PROJECT_PLAN.md` after substantive tasks (completed / next / current focus). **Granular checklist:** [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) (tracks A–F; tick as you go).
- **MLOps serving (committed scope):** [docs/deployment/TECHNICAL_EXTENSIONS.md](docs/deployment/TECHNICAL_EXTENSIONS.md); [docs/deployment/RUNBOOK.md](docs/deployment/RUNBOOK.md); [docs/deployment/ML_OPS_SERVING_ANALYSIS.md](docs/deployment/ML_OPS_SERVING_ANALYSIS.md); workflow [`.github/workflows/docker-build.yml`](.github/workflows/docker-build.yml).
- **Thesis (≥50 pp., Word + tables/figures):** Draft body in `docs/thesis/MANUSCRIPT.md` (Pandoc → Word per `docs/thesis/README.md`); start from `docs/THESIS_WRITING_HUB.md`; spine `docs/THESIS_FOUNDATION.md`; figures under `docs/figures/`.
- **Gates:** A Fairness (`gate_fairness.py`), B SHAP (`gate_shap.py`); thresholds in `params.yaml` under `gates.*`. Gate C is **GitHub Environment** `model-governance` + `governed_deploy.yml` (latency JSON).
- **Profiles:** `pipeline.profile` or `PIPELINE_PROFILE` = `standard` (train only) vs `governed` (full GaC); see `docs/compare_pipelines.md`.
