# EU AI Act Governance-as-Code (GaC) — Credit Scoring

Design Science Research (DSR) thesis artifact: MLOps pipeline with fairness (Fairlearn), explainability (SHAP), and human-oversight gates (CI/CD), evaluated against a standard performance-only pipeline.

## Documentation

**Charter** (precedence, deprecations, full thesis-doc map): [docs/DOCUMENTATION_FOUNDATION.md](docs/DOCUMENTATION_FOUNDATION.md). Use it to resolve **any** conflict between README text and thesis docs—then fix the weaker document.

## Stack (target)

- Python, MLflow, DVC  
- South German Credit Dataset  
- GitHub Actions (gates)

## Layout

| Path | Purpose |
|------|---------|
| `docs/` | Thesis source; **[docs/thesis/MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md)** (draft thesis); [docs/figures/](docs/figures/) for figures |
| `src/` | Training, evaluation, gate scripts |
| `serving/` | MLOps FastAPI scoring API — see **Serving** below |
| `scripts/` | `compare_profiles.py` (P3); `smoke_serving.py` (serving health check) |
| `.github/workflows/` | GitHub Actions (CI matrix, `docker-build`, governed deploy / Gate C) |
| `pipelines/` | Placeholder (reserved); workflows live under `.github/workflows/` |
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

Tracking: `params.yaml` → `mlflow.tracking_uri` is **`sqlite:///./mlflow.db`** (file `mlflow.db`). UI: `mlflow ui --backend-store-uri sqlite:///./mlflow.db` from repo root. (`mlruns/` is gitignored; used only if you switch to a file store.)  
**P3 experiment (local):** `python scripts/compare_profiles.py` → [metrics/experiment_comparison.json](metrics/experiment_comparison.json).

**GitHub / Gate C:** [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md) · **Troubleshoot governed-deploy:** [docs/GATE_C_RUNBOOK.md](docs/GATE_C_RUNBOOK.md) · **Thesis eval notes:** [docs/THESIS_EVAL_NOTES.md](docs/THESIS_EVAL_NOTES.md) · **Thesis spine (RQs, DSR, scope):** [docs/THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md).

**Foundation:** MLflow **SQLite** store (`mlflow.db`); run context (**git**, **params**, **dvc.lock** digests) on each train. Lockfile: [requirements.lock.txt](requirements.lock.txt). **Compliance map:** [docs/COMPLIANCE_MATRIX.md](docs/COMPLIANCE_MATRIX.md). **Sub-RQ1 policy demo:** [docs/SUB_RQ1_DEMO.md](docs/SUB_RQ1_DEMO.md).

**Thesis writing:** [docs/DOCUMENTATION_FOUNDATION.md](docs/DOCUMENTATION_FOUNDATION.md) (charter) → [docs/THESIS_WRITING_HUB.md](docs/THESIS_WRITING_HUB.md) (**≥50 pages**, tables/figures plan, anchors) → [docs/THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) · [docs/EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md) · [docs/THESIS_CUT_LIST.md](docs/THESIS_CUT_LIST.md) · [docs/SUB_RQ2_ALTERNATIVES.md](docs/SUB_RQ2_ALTERNATIVES.md).

**Plan & status:** [PROJECT_PLAN.md](PROJECT_PLAN.md) · **Journey checklist (detailed):** [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) · **Review log:** [docs/DR_VOSS_REVIEW_LOG.md](docs/DR_VOSS_REVIEW_LOG.md).

## Serving (MLOps — Docker)

Illustrative **scoring API** for CV/thesis discussion; not bank production. **`artifacts/`** is **gitignored** — train first so **`model.joblib`** and **`feature_schema.json`** exist, then run the container with a **volume** mount.

1. **Train:** `python src/train.py` (or `dvc repro`) — writes `artifacts/model.joblib`, `artifacts/feature_schema.json` (column contract for inference), and gate CSVs.
2. **Install serving deps** (local run without Docker): `pip install -r requirements-serving.txt`
3. **Run API:** `docker compose up --build` from the repo root (port **8080**), **or** `uvicorn serving.app:app --host 127.0.0.1 --port 8080` from repo root with `PYTHONPATH=.`

**Endpoints:** `GET /health` (liveness) · `GET /ready` (readiness) · `GET /version` · `GET /metrics` (minimal process JSON, not Prometheus) · `POST /predict` with body `{"records": [ { "<feature>": <value>, ... } ]}` (columns must match `feature_schema.json`).

**Operational knobs (environment):**

| Variable | Role |
|----------|------|
| `SERVING_API_KEY` | If set, `POST /predict` requires header `X-API-Key` (same value). `/health`, `/ready`, `/version`, and `/metrics` stay open. |
| `MAX_BODY_BYTES` | Max `Content-Length` for `POST /predict` (default **1048576**). **413** if larger. |
| `RATE_LIMIT_PREDICT` | Per-IP limit for `POST /predict` (default **`120/minute`**; **`off`** = effectively unlimited). |
| `LOG_JSON_ACCESS` | `1` (default): one JSON access log line per request to stdout (no request body logged). Set `0` to disable. |
| `MODEL_PATH` / `SCHEMA_PATH` | Override paths to model and schema (defaults under `artifacts/`). |

**Smoke test** (API must be running): `python scripts/smoke_serving.py` — optional `SERVING_API_KEY`. Options: `--base-url`, `--artifacts`.

**CI:** [`.github/workflows/docker-build.yml`](.github/workflows/docker-build.yml) — **train → Docker build → upload `serving-image.tar`** (every run; download from **Actions** → **Artifacts**). On **`push`** / **`workflow_dispatch`** (not **`pull_request`**), also **push** to **GHCR** (`ghcr.io/<owner>/<repo>:serving-<sha>` and `:latest`).

**Reference docs:** [docs/deployment/TECHNICAL_EXTENSIONS.md](docs/deployment/TECHNICAL_EXTENSIONS.md) · [docs/deployment/RUNBOOK.md](docs/deployment/RUNBOOK.md) · [docs/deployment/ML_OPS_SERVING_ANALYSIS.md](docs/deployment/ML_OPS_SERVING_ANALYSIS.md) (§8 career note).

## Rules

Project rules live in `.cursor/rules/` (Dr. Ingrid Voss persona for DSR/compliance tone).
