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
- `scripts/compare_profiles.py` + `metrics/experiment_comparison.json` — local P3 tabulation (same seed)
- `docs/GITHUB_SETUP.md` — remote, Environment, governed-deploy
- `docs/THESIS_EVAL_NOTES.md` — limitations + artifact checklist for writing
- **GitHub:** `origin` → `https://github.com/iamchau/eu-ai-act-gac-credit.git`, branch **`main`**, pushed

---

## Next (priority order)

1. **Gate C sample (you):** In GitHub: create Environment **`model-governance`** (optional reviewers) → **Actions** → **governed-deploy** → Run workflow → download **`human-oversight-latency-*`** artifact → keep `human_oversight_latency.json` for Sub-RQ2. Details: [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md).
2. **Git identity (you):** If needed: `git config user.email "your@email"` (global or repo).
3. **Thesis writing:** Use [docs/THESIS_EVAL_NOTES.md](docs/THESIS_EVAL_NOTES.md) + tables from `experiment_comparison.json`; cite MLflow run URLs from the UI.
4. **Optional:** After `params.yaml` changes, run `python scripts/compare_profiles.py` and commit updated JSON.

---

## Current focus

- **Collect one Gate C latency artifact** on GitHub, then **draft thesis evaluation** using `experiment_comparison.json` + eval notes.

---

## Blockers / decisions

| Item                              | Owner | Notes                                                      |
| --------------------------------- | ----- | ---------------------------------------------------------- |
| Environment `model-governance`    | You   | Create in repo Settings; add reviewers for real approval waits |
| Fairness threshold `0.70`         | You   | Document sensitivity; tighten after mitigation experiments |
| `dvc.yaml` uses Windows venv path | You   | On Linux/Mac, change `cmd` to `.venv/bin/python src/...`   |

---

## How to update this file

1. Move finished items from **Next** into **Completed** (`[x]`).
2. Edit **Current focus** to one short line.
3. Bump **Last updated** to today’s date.
4. Optional: add MLflow run id / git commit next to completed items for audit trail.
