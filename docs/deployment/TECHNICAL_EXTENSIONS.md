# Technical extensions catalog — serving & MLOps

**Purpose:** Single index of **implemented** and **planned** technical extensions for the scoring API and training path. Thesis **RQs** are unchanged unless you run new supervised experiments; these items support **portfolio**, **operations hygiene**, and **Primary RQ** instantiation narrative.

**Authority:** Runtime behaviour is defined by **`serving/app.py`**, **`src/train.py`**, and **`params.yaml`** — update this file when you add or change extensions.

---

## Implemented

| ID | Extension | Location / mechanism |
|----|-----------|----------------------|
| **A1** | Optional API key | Env **`SERVING_API_KEY`**. When set, **`POST /predict`** requires header **`X-API-Key`**. **`GET /health`**, **`GET /ready`**, **`GET /version`**, and **`GET /metrics`** stay unauthenticated for probes. |
| **A2** | Smoke test script | **`scripts/smoke_serving.py`** — **`/health`**, **`/ready`**, **`/version`**, **`/metrics`**, **`POST /predict`**. |
| **A3** | Max request body size | Env **`MAX_BODY_BYTES`** (default **1048576**). **`POST /predict`** → **413** if `Content-Length` exceeds limit. |
| **B4** | Feature schema artefact | **`train.py`** writes **`artifacts/feature_schema.json`**. Serving validates columns when file is present. |
| **B5** | CI: train → Docker image artefact + GHCR | **`.github/workflows/docker-build.yml`** — train → **`docker build`** → upload **`serving-image.tar`**; on **`push`** / **`workflow_dispatch`**, **`docker push`** to **GHCR** (`:serving-<sha>`, `:latest`). |
| **B6** | Structured JSON access logs | Env **`LOG_JSON_ACCESS`** (default **`1`**). One JSON line per request — **no** body or features. |
| **C7** | **`/health` vs `/ready`** | **`GET /health`** = liveness (**200**). **`GET /ready`** = readiness (**503** if model missing). |
| **C8** | Minimal **`/metrics`** | **`GET /metrics`** — JSON: uptime, PID, Python version, model/schema flags, **`predict_success_total`** (not Prometheus text format). |
| **C9** | Rate limiting (`/predict`) | **`slowapi`**; env **`RATE_LIMIT_PREDICT`** (default **`120/minute`**); **`off`** / **`none`** / **`0`** = effectively unlimited (high ceiling). |

**Environment variables (serving)**

| Variable | Default | Role |
|----------|---------|------|
| `MODEL_PATH` | `artifacts/model.joblib` | Trained pipeline |
| `SCHEMA_PATH` | `artifacts/feature_schema.json` | Optional schema contract |
| `SERVING_API_KEY` | *(empty)* | If set, protects `POST /predict` |
| `MAX_BODY_BYTES` | `1048576` | Max `Content-Length` for `POST /predict` |
| `RATE_LIMIT_PREDICT` | `120/minute` | Per-IP rate limit for `POST /predict`; **`off`** disables strict cap |
| `LOG_JSON_ACCESS` | `1` | JSON access logs |
| `GIT_COMMIT`, `PARAMS_SHA16` | — | Optional overrides for `/version` |
| `PORT` | `8080` | Uvicorn |

**Operations guide:** [RUNBOOK.md](RUNBOOK.md).

---

## Planned / backlog (to complete)

*None — MLOps backlog (**`/metrics`**, **GHCR push**) is implemented; see **Implemented** above.*

---

## Operational notes

- **`artifacts/`** remains **gitignored**; **`docker build`** requires a **prior train** so COPY succeeds (see [RUNBOOK.md](RUNBOOK.md)).
- **Bank / production:** Research / demo scope — patterns are **illustrative**, not enterprise IAM or DDoS protection.

---

*Maintainer: when adding an extension, update this file, [ML_OPS_SERVING_ANALYSIS.md](ML_OPS_SERVING_ANALYSIS.md), and [README.md](../../README.md) **Serving**.*
