# Thesis project plan & status

**Last updated:** 2026-04-07

This file is the **single overview** for scope, what is done, and what comes next. After each meaningful task, update **Last updated**, **Completed**, and **Next** (one minute).

---

## Phases (high level)


| Phase | Goal                                                          | Status          |
| ----- | ------------------------------------------------------------- | --------------- |
| P0    | Repo + Python stack + MLflow + DVC baseline                   | **In progress** |
| P1    | Fairness gate (Fairlearn) + SHAP gate + metrics in CI         | Not started     |
| P2    | Human-in-the-loop gate (GitHub Actions) + latency measurement | Not started     |
| P3    | Standard vs governed experiment + thesis write-up             | Not started     |


---

## Completed

- Repository scaffold (`README`, `AGENTS`, `.gitignore`, layout)
- `requirements.txt` + `.venv` (local; not committed)
- `params.yaml` + `dvc.yaml` train stage (params tracked; `dvc repro` uses `.venv\Scripts\python.exe` on Windows)
- `src/train.py`: sklearn pipeline, MLflow run + `data_provenance`, metrics JSON
- Dataset policy: **local CSV** `data/raw/south_german_credit.csv` for thesis runs; **OpenML credit-g** fallback for dev if CSV absent
- `dvc init` + `dvc.lock` generated from successful `dvc repro`
- `PROJECT_PLAN.md` (this overview)

---

## Next (priority order)

1. **South German CSV:** obtain UPDATE dataset (UCI 573 / your institution copy) → `data/raw/south_german_credit.csv` → rerun `dvc repro` for thesis numbers.
2. **MLflow UI:** `mlflow ui --backend-store-uri file:./mlruns` and confirm runs + `data_provenance`.
3. **Gate A (fairness):** Fairlearn equalized odds + fail pipeline if below threshold.
4. **Gate B (SHAP):** export report artifact per run.
5. **Gate C (oversight):** GitHub Actions approval + latency (Sub-RQ2).
6. **Thesis writing:** DSR cycles + traceability (MLflow run id, DVC commit, CI logs).

---

## Current focus

- Acquire South German Credit **UPDATE** CSV and replace the OpenML fallback for all **reported** experiments.

---

## Blockers / decisions


| Item                              | Owner | Notes                                                         |
| --------------------------------- | ----- | ------------------------------------------------------------- |
| Git `user.name` / `user.email`    | You   | Set for meaningful commit attribution                         |
| DVC remote (optional)             | You   | Local-only is fine until collaboration                        |
| `dvc.yaml` uses Windows venv path | You   | On Linux/Mac, change `cmd` to `.venv/bin/python src/train.py` |


---

## How to update this file

1. Move finished items from **Next** into **Completed** (`[x]`).
2. Edit **Current focus** to one short line.
3. Bump **Last updated** to today’s date.
4. Optional: add MLflow run id / git commit next to completed items for audit trail.

