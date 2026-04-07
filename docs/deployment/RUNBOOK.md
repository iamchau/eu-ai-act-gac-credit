# Serving API — runbook (operations)

**Scope:** Local **Docker**, **uvicorn**, and **CI** artefacts. **Not** production banking operations.

---

## Prerequisites

1. **Python 3.12** (aligned with CI and `ci.yml`).
2. **Training** so **`artifacts/`** contains at least:
   - `model.joblib`
   - `feature_schema.json` (written by `src/train.py`)
   - Gate CSVs if you run fairness/SHAP locally (`scripts/compare_profiles.py` or `dvc repro`).

```bash
python src/train.py
# or: dvc repro   (Windows: .venv path in dvc.yaml)
```

---

## Run locally (no Docker)

```bash
pip install -r requirements-serving.txt
set PYTHONPATH=.
# Windows PowerShell: $env:PYTHONPATH=(Get-Location).Path
uvicorn serving.app:app --host 127.0.0.1 --port 8080
```

**Smoke test** (second terminal):

```bash
python scripts/smoke_serving.py
```

---

## Docker: `docker build` (baked model + schema)

The **`Dockerfile`** **COPY**s **`artifacts/model.joblib`** and **`artifacts/feature_schema.json`** into the image. **You must train first** so those files exist in the build context; otherwise `docker build` **fails** at COPY.

```bash
python src/train.py
docker build -t gac-credit-serving:local .
docker run --rm -p 8080:8080 gac-credit-serving:local
```

**Load image from CI:** download **`serving-image-<sha>.tar`** from the **docker-build** workflow artefact, then:

```bash
docker load -i serving-image.tar
docker run --rm -p 8080:8080 gac-credit-serving:<git-sha>
```

---

## Docker Compose (dev)

Mounts host **`./artifacts`** over **`/app/artifacts`**. You still need **`artifacts/`** on the host with trained files (or the API will fail readiness).

```bash
python src/train.py
docker compose up --build
```

---

## Endpoints (summary)

| Path | Role |
|------|------|
| `GET /health` | **Liveness** — process up (always **200** if server runs). |
| `GET /ready` | **Readiness** — model loaded (**503** if not). |
| `GET /version` | Git/params digests + paths (no secrets). |
| `POST /predict` | Scoring; optional **`X-API-Key`**; rate-limited (see below). |

---

## Environment variables

| Variable | Default | Notes |
|----------|---------|--------|
| `SERVING_API_KEY` | *(empty)* | If set, **`POST /predict`** requires **`X-API-Key`**. |
| `MAX_BODY_BYTES` | `1048576` | Max body size for **`/predict`**. |
| `RATE_LIMIT_PREDICT` | `120/minute` | slowapi limit; **`off`** / **`none`** / **`0`** = effectively unlimited (high ceiling). |
| `LOG_JSON_ACCESS` | `1` | JSON lines per request to stdout. |
| `MODEL_PATH` / `SCHEMA_PATH` | under `artifacts/` | Override for tests or custom layouts. |

---

## CI

- **`ci.yml`** — matrix train + gates; **`serving_import`** imports `serving.app`.
- **`docker-build.yml`** — train → **`docker build`** → upload **`serving-image.tar`** (artefact **per run**).

No container registry is configured; **push to a registry** is a separate manual step if you need it.

---

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| `COPY` failed in `docker build` | Train first; **`artifacts/`** missing. |
| `503` on **`/ready`** | Model path wrong or mount empty. |
| `401` on **`/predict`** | Set **`SERVING_API_KEY`** on server **and** pass header from client. |
| `429` on **`/predict`** | Rate limit; raise **`RATE_LIMIT_PREDICT`** or set to **`off`**. |

---

*See also [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md) and [ML_OPS_SERVING_ANALYSIS.md](ML_OPS_SERVING_ANALYSIS.md).*
