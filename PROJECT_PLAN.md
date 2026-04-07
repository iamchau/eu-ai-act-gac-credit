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
- `params.yaml` + `dvc.yaml`: train → fairness_gate → shap_gate; `pipeline.profile` (`standard` \| `governed`)
- `src/train.py` + `src/data_loading.py`: MLflow + `pipeline_profile`; gate artifacts
- Gates A–B: `gate_fairness.py`, `gate_shap.py` + metrics JSON
- Gate C: `governed_deploy.yml` — Environment `model-governance`, `metrics/human_oversight_latency.json` (see `docs/human_oversight.md`)
- CI matrix: `ci.yml` runs standard (train only) and governed (train + gates)
- `docs/compare_pipelines.md` — standard vs governed comparison table
- **`scripts/compare_profiles.py`** + **`metrics/experiment_comparison.json`** — local P3 tabulation (same seed)
- **`docs/GITHUB_SETUP.md`** — remote, Environment, governed-deploy
- **`docs/THESIS_EVAL_NOTES.md`** — limitations + artifact checklist for writing

---

## Next (priority order)

1. **GitHub (you):** follow `docs/GITHUB_SETUP.md` — add `origin`, push, create Environment **`model-governance`**, run **`governed_deploy`**, save **`human_oversight_latency.json`**.
2. **Git identity (you):** replace placeholder email if needed: `git config user.email "…"`.
3. **Thesis writing:** use `docs/THESIS_EVAL_NOTES.md` + paste tables from `experiment_comparison.json`; add MLflow run links from UI.
4. **Optional:** re-run `python scripts/compare_profiles.py` after any `params.yaml` change; commit the new JSON for traceability.

---

## Current focus

- **Push to GitHub** and collect **one** Gate C latency artifact; finish thesis chapters using **`experiment_comparison.json`** + eval notes.

---

## Blockers / decisions

| Item                              | Owner | Notes                                                                                         |
| --------------------------------- | ----- | --------------------------------------------------------------------------------------------- |
| Git remote + push                 | You   | See `docs/GITHUB_SETUP.md`                                                                    |
| Fairness threshold `0.70`         | You   | Document sensitivity; tighten after mitigation experiments                                    |
| `dvc.yaml` uses Windows venv path | You   | On Linux/Mac, change `cmd` to `.venv/bin/python src/...`                                      |
| Environment `model-governance`    | You   | Add reviewers in repo Settings for real Gate C waits                                          |

---

## How to update this file

1. Move finished items from **Next** into **Completed** (`[x]`).
2. Edit **Current focus** to one short line.
3. Bump **Last updated** to today’s date.
4. Optional: add MLflow run id / git commit next to completed items for audit trail.
