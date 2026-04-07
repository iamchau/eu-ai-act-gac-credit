# Thesis project plan & status

**Last updated:** 2026-04-07

This file is the **single overview** for scope, what is done, and what comes next. After each meaningful task, update **Last updated**, **Completed**, and **Next** (one minute).

---

## Phases (high level)


| Phase | Goal                                                          | Status          |
| ----- | ------------------------------------------------------------- | --------------- |
| P0    | Repo + Python stack + MLflow + DVC baseline                   | **Done**        |
| P1    | Fairness gate (Fairlearn) + SHAP gate + metrics in CI         | **Done**        |
| P2    | Human-in-the-loop gate (GitHub Actions) + latency measurement | **Done** (CI)   |
| P3    | Standard vs governed experiment + thesis write-up             | **In progress** |


---

## Completed

- Repository scaffold (`README`, `AGENTS`, `.gitignore`, layout)
- `requirements.txt` + `.venv` (local; not committed)
- UCI South German Credit UPDATE in `data/raw/SouthGermanCredit.asc` + `docs/DATA_PROVENANCE.md`
- `params.yaml` + `dvc.yaml`: **train** → **fairness_gate** → **shap_gate**; `**pipeline.profile`** (`standard`  `governed`)
- `src/train.py` + `src/data_loading.py`: MLflow + `**pipeline_profile**`; gate artifacts
- Gates A–B: `gate_fairness.py`, `gate_shap.py` + metrics JSON
- **Gate C:** `governed_deploy.yml` — Environment `**model-governance`**, `**metrics/human_oversight_latency.json**` (see `docs/human_oversight.md`)
- **CI matrix:** `ci.yml` runs **standard** (train only) and **governed** (train + gates)
- `docs/compare_pipelines.md` — standard vs governed comparison table

---

## Next (priority order)

1. **GitHub:** add `origin`, push; create Environment `**model-governance`** with required reviewers; run `**governed_deploy**` once and archive `**human_oversight_latency.json**` for the thesis.
2. **Git identity:** `user.name` / `user.email` for commits.
3. **P3 experiment:** tabulate **standard vs governed** (CI duration, gate outcomes, MLflow run ids) for the same `seed`.
4. **Thesis:** DSR narrative + limitations (CI proxy for Art. 14; fairness threshold 0.70).

---

## Current focus

- Collect **one governed_deploy** latency sample and **standard vs governed** CI metrics for the evaluation chapter.

---

## Blockers / decisions


| Item                              | Owner | Notes                                                                                         |
| --------------------------------- | ----- | --------------------------------------------------------------------------------------------- |
| Git `user.name` / `user.email`    | You   | Set for meaningful commit attribution                                                         |
| Fairness threshold `0.70`         | You   | Baseline logistic is high EOD on `famges`; tighten after mitigation experiments in the thesis |
| `dvc.yaml` uses Windows venv path | You   | On Linux/Mac, change `cmd` to `.venv/bin/python src/...`                                      |
| Environment `model-governance`    | You   | Add reviewers in repo Settings for real Gate C waits                                          |


---

## How to update this file

1. Move finished items from **Next** into **Completed** (`[x]`).
2. Edit **Current focus** to one short line.
3. Bump **Last updated** to today’s date.
4. Optional: add MLflow run id / git commit next to completed items for audit trail.

