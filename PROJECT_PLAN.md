# Thesis project plan & status

**Last updated:** 2026-04-07

This file is the **single overview** for scope, what is done, and what comes next. After each meaningful task, update **Last updated**, **Completed**, and **Next** (one minute).

---

## Phases (high level)


| Phase | Goal                                                          | Status      |
| ----- | ------------------------------------------------------------- | ----------- |
| P0    | Repo + Python stack + MLflow + DVC baseline                   | **Done**    |
| P1    | Fairness gate (Fairlearn) + SHAP gate + metrics in CI         | **Done**    |
| P2    | Human-in-the-loop gate (GitHub Actions) + latency measurement | Not started |
| P3    | Standard vs governed experiment + thesis write-up             | Not started |


---

## Completed

- Repository scaffold (`README`, `AGENTS`, `.gitignore`, layout)
- `requirements.txt` + `.venv` (local; not committed)
- UCI South German Credit UPDATE in `data/raw/SouthGermanCredit.asc` (from official zip; provenance in `docs/DATA_PROVENANCE.md`)
- `params.yaml` + `dvc.yaml`: **train** → **fairness_gate** → **shap_gate**
- `src/train.py` + `src/data_loading.py`: MLflow, metrics, artifacts for gates (`model.joblib`, `val_audit.csv`, `X_val.csv`, `X_background.csv`)
- `src/gate_fairness.py` — Equalized Odds (fairlearn), `metrics/fairness_gate.json`
- `src/gate_shap.py` — SHAP report `artifacts/shap_report.md`, `metrics/shap_gate.json`
- GitHub Actions **ci.yml** (Ubuntu): pip install → UCI download → train → gates
- `dvc repro` end-to-end green (Windows venv path in `dvc.yaml`)

---

## Next (priority order)

1. **Git identity:** set `user.name` / `user.email` for meaningful commits.
2. **Remote:** add GitHub origin and push (enables CI on `push`).
3. **Gate C (human oversight):** required approval + **latency** measurement (Sub-RQ2) in Actions or external tool.
4. **Standard vs governed:** second pipeline (performance-only) vs full gates; compare outcomes + velocity/latency.
5. **Thesis:** DSR write-up + traceability tables (MLflow run id, DVC `git` commit, CI run URL).

---

## Current focus

- Wire **human-in-the-loop** (P2) and define the **standard** baseline path for the controlled experiment (P3).

---

## Blockers / decisions


| Item                              | Owner | Notes                                                                                         |
| --------------------------------- | ----- | --------------------------------------------------------------------------------------------- |
| Git `user.name` / `user.email`    | You   | Set for meaningful commit attribution                                                         |
| Fairness threshold `0.70`         | You   | Baseline logistic is high EOD on `famges`; tighten after mitigation experiments in the thesis |
| `dvc.yaml` uses Windows venv path | You   | On Linux/Mac, change `cmd` to `.venv/bin/python src/...`                                      |


---

## How to update this file

1. Move finished items from **Next** into **Completed** (`[x]`).
2. Edit **Current focus** to one short line.
3. Bump **Last updated** to today’s date.
4. Optional: add MLflow run id / git commit next to completed items for audit trail.