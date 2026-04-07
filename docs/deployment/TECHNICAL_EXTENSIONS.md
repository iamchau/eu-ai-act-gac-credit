# Technical extensions catalog — serving & MLOps

**Purpose:** Single index of **implemented** and **planned** technical extensions for the scoring API and training path. Thesis **RQs** are unchanged unless you run new supervised experiments; these items support **portfolio**, **operations hygiene**, and **Primary RQ** instantiation narrative.

**Authority:** Runtime behaviour is defined by **`serving/app.py`**, **`src/train.py`**, and **`params.yaml`** — update this file when you add or change extensions.

---

## Implemented (Tier A + B4 + B6)

| ID | Extension | Location / mechanism |
|----|-----------|----------------------|
| **A1** | Optional API key | Env **`SERVING_API_KEY`**. When set, **`POST /predict`** requires header **`X-API-Key`** (same value). **`GET /health`** and **`GET /version`** stay unauthenticated for probes. |
| **A2** | Smoke test script | **`scripts/smoke_serving.py`** — calls `/health`, `/version`, **`POST /predict`** using **`artifacts/feature_schema.json`** for column names (falls back to minimal probe if schema missing). |
| **A3** | Max request body size | Env **`MAX_BODY_BYTES`** (default **1048576** = 1 MiB). **`POST /predict`** rejected with **413** if `Content-Length` exceeds limit (defence-in-depth; not a substitute for WAF). |
| **B4** | Feature schema artefact | **`train.py`** writes **`artifacts/feature_schema.json`** after fit (`feature_names`, `dtypes`, digests). **`serving/app.py`** validates request columns against schema when file is present (aligns train/serve contract). |
| **B6** | Structured JSON access logs | Env **`LOG_JSON_ACCESS`** (default **`1`**). One **JSON object per line** to stdout: `event`, `method`, `path`, `status_code`, `duration_ms`, `request_id` — **no** request body or raw features logged. |

**Environment variables (serving)**

| Variable | Default | Role |
|----------|---------|------|
| `MODEL_PATH` | `artifacts/model.joblib` | Trained pipeline |
| `SERVING_API_KEY` | *(empty)* | If set, protects `POST /predict` |
| `MAX_BODY_BYTES` | `1048576` | Max `Content-Length` for `POST /predict` |
| `LOG_JSON_ACCESS` | `1` | `1` / `true` / `yes` → JSON access logs |
| `GIT_COMMIT`, `PARAMS_SHA16` | — | Optional overrides for `/version` in containers |
| `PORT` | `8080` | Uvicorn (local `python -m serving.app`) |

---

## Planned / backlog (not implemented here)

| ID | Extension | Notes |
|----|-----------|--------|
| **B5** | CI: train → `docker build` | GitHub Actions; image artefact or registry — see [ML_OPS_SERVING_ANALYSIS.md](ML_OPS_SERVING_ANALYSIS.md) §7 |
| **C7** | `/health` vs `/ready` split | Liveness vs model-loaded readiness |
| **C8** | Minimal `/metrics` | Process stats; not full Prometheus |
| **C9** | Rate limiting | e.g. `slowapi` or reverse proxy |

---

## Operational notes

- **`artifacts/`** remains **gitignored**; **`feature_schema.json`** is produced with **`model.joblib`** on each train.
- **Bank / production:** This stack is still **research / demo** scope — API key and body limits are **minimal** patterns, not enterprise IAM or DDoS protection.

---

*Maintainer: when adding an extension, update this file, [ML_OPS_SERVING_ANALYSIS.md](ML_OPS_SERVING_ANALYSIS.md), and [README.md](../../README.md) **Serving**.*
