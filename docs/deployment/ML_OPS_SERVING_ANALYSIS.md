# MLOps serving slice — analysis (thesis extension)

**Purpose:** Bounded **production-adjacent** artefact: containerised **scoring API** for the trained pipeline, without claiming bank-grade operations. **Does not** replace Sub-RQ1/2 evidence; extends **Primary RQ** “instantiation” and **Discussion**.

---

## 1. What we already have (foundation)


| Asset            | Location                                  | Role                                                                                         |
| ---------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------- |
| Trained pipeline | `artifacts/model.joblib`                  | sklearn `Pipeline` (ColumnTransformer + LogisticRegression); **full** preprocessing in-model |
| Training         | `src/train.py`                            | Fits pipeline, writes joblib + gate CSVs                                                     |
| Features         | Same as UCI raw                           | `load_xy_from_config` → feature matrix `X`                                                   |
| Repro metadata   | `metrics/train_metrics.json`, MLflow tags | `git_commit`, `params_yaml_sha16`, `dvc_lock_sha16`                                          |
| Params           | `params.yaml`                             | Single source for hyperparameters                                                            |
| CI               | `.github/workflows/ci.yml` + **`docker-build.yml`** | Train + gates; **serving import**; **train → Docker image** artefact (`serving-image.tar`) |


**Inference rule:** `pipeline.predict` / `predict_proba` expect a **DataFrame** (or array) with **columns matching training `X`** — same names and compatible dtypes as after `load_xy_from_config`.

---

## 2. Constraints (important)


| Constraint                     | Implication                                                                                                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`artifacts/` is gitignored** | `model.joblib` and `feature_schema.json` are **not** in git. Use **runtime volume** (docker-compose) or copy into image after train. |
| **No production data**         | API is a **demo**; optional **`SERVING_API_KEY`** and **`MAX_BODY_BYTES`** — see [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md). |
| **Thesis RQs**                 | Sub-RQ1/2 stay tied to **committed JSON + CI** unless you run a **new** supervised experiment; this slice supports **narrative + Primary RQ** only unless you add an explicit deploy-gate story later. |


---

## 3. What was added (this slice)


| File | Purpose |
|------|---------|
| `serving/app.py` | FastAPI: `/health`, `/version`, `/predict`; optional **`SERVING_API_KEY`**, **`MAX_BODY_BYTES`**, JSON access logs — see [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md) |
| `requirements-serving.txt` | Minimal deps — **no** MLflow/DVC/SHAP in image |
| `Dockerfile` | Serving image; **bakes** `artifacts/model.joblib` + `feature_schema.json` (requires **train before `docker build`** — [RUNBOOK.md](RUNBOOK.md)) |
| `docker-compose.yml` | Mount `./artifacts`, `MODEL_PATH`, `SCHEMA_PATH`, env template |
| `.github/workflows/docker-build.yml` | CI: fetch data → train → **`docker build`** → upload **`serving-image-<sha>.tar`** |
| `src/train.py` | Writes **`artifacts/feature_schema.json`** after fit |
| `scripts/smoke_serving.py` | Smoke: **`/health`**, **`/ready`**, **`/version`**, **`POST /predict`** |
| [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md) | Catalog: implemented + small backlog |
| [RUNBOOK.md](RUNBOOK.md) | Operations: local, Docker, CI artefact, `docker load` |


**Documentation wired in:** `README.md` (**Serving**), `docs/thesis/MANUSCRIPT.md` (§5.4), `docs/DOCUMENTATION_FOUNDATION.md`, `PROJECT_PLAN.md`.

**Training:** Column contract is **both** `pipeline.feature_names_in_` at load time **and** **`feature_schema.json`** on disk for tooling and serving validation.

---

## 4. What we do **not** add (out of scope for this slice)

- Kubernetes manifests, service mesh, multi-region  
- Full auth (OAuth, mTLS) — **`SERVING_API_KEY`** is a **toy** demo pattern only  
- Online drift monitoring, Prometheus stack (future work sentence in thesis)  
- Treating this API as **evidence** for Sub-RQ1/2 without new supervised experiments — see **§2** (thesis RQs)

---

## 5. Operational flow

1. **Train:** `python src/train.py` (or `dvc repro`) → `artifacts/model.joblib` exists.
2. **Local API:** `docker compose up --build` → mounts `artifacts/`, starts uvicorn.
3. **Predict:** `POST /predict` with JSON `{"records": [{ "<col>": <val>, ... }, ...]}` — columns must match **`feature_schema.json`** (and the model pipeline). Optional **API key** / **body limit** / **JSON logs** — [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md).  
4. **Smoke:** `python scripts/smoke_serving.py` (with API running).  
5. **Thesis:** Cite as **deployment illustration**; link git SHA from `/version` to reproducibility narrative.

---

## 6. Effort recap (initial slice)


| Task                                 | Rough time                         |
| ------------------------------------ | ---------------------------------- |
| Serving files + README + thesis §5.4 | **~2–4 h**                         |
| First-time Docker install + debug    | **variable** (user machine)        |
| Remaining **§7** backlog items       | **~1–4 h** each, depending on item |


---

## 7. Future extensions (backlog)

**Committed project scope:** items below are **planned completion work** (not out-of-scope extras). **Implemented elsewhere:** [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md) (includes **B5** CI Docker, **C7** `/ready`, **C9** rate limit).

**Still open (not implemented):**

| Item | Notes |
|------|--------|
| **Minimal `/metrics`** | Process stats; not full Prometheus |
| **Container registry push** (GHCR, etc.) | Needs secrets + policy decision |

**Relationship to §4:** Backlog items are **planned completion work**; §4 still lists what we are **not** claiming as full production scope.

---

## 8. Career / portfolio note (outside thesis claims)

This slice is **not** bank-regulated production and **does not** substitute for certifications or on-the-job controls in a real bank. For **career** purposes it can still **signal useful skills** when described honestly:


| Signal                 | What the repo demonstrates                                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Governance-aware MLOps | Gates, CI, traceability (git/params digests), EU AI Act–aligned **thesis** narrative                                                                         |
| Serving hygiene        | Containerised API, `/health`, `/version`, `/predict`, reproducibility hooks                                                                                  |
| Professional framing   | Clear **scope limits** (research data, illustrative deploy) and a credible story for **what you would add** in enterprise (auth, monitoring, change control) |


**Interview-safe one-liner:** *“Research repo with governed training and CI gates; I added a containerised scoring API to practise deployment-shaped MLOps—not production banking stack, but the same building blocks at student scope.”*

The backlog ([§7](#7-future-extensions-backlog) and [TECHNICAL_EXTENSIONS.md](TECHNICAL_EXTENSIONS.md)) deepens that signal without changing thesis RQs.

---

*Maintainer: if `train.py` changes feature construction, update serving docs and re-train before building images.*