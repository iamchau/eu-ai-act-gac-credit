# Thesis project plan & status

**Last updated:** 2026-04-07 (Sub-RQ2 alternatives + Discussion stubs)

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
- `params.yaml` + `dvc.yaml`: train → fairness_gate → shap_gate; `pipeline.profile` (`standard`  `governed`)
- `src/train.py` + `src/data_loading.py`: MLflow + `pipeline_profile`; gate artifacts
- Gates A–B: `gate_fairness.py`, `gate_shap.py` + metrics JSON
- Gate C: `governed_deploy.yml` + `**metrics/human_oversight_latency.json`** archived (run [24081106560](https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560), **7 s** human-oversight latency)
- CI matrix: `ci.yml` runs standard (train only) and governed (train + gates)
- `docs/compare_pipelines.md` — standard vs governed comparison table
- `scripts/compare_profiles.py` + `metrics/experiment_comparison.json` — local P3 tabulation (same seed)
- `docs/GITHUB_SETUP.md`, `docs/GATE_C_RUNBOOK.md`
- `docs/THESIS_EVAL_NOTES.md` — limitations + artifact checklist for writing
- **GitHub:** `origin` → `https://github.com/iamchau/eu-ai-act-gac-credit.git`, branch `**main`**, pushed
- **Foundation (2026-04-07):** MLflow **SQLite** (`mlflow.db`), `src/run_context.py` digests (**git**, **params.yaml**, **dvc.lock**), `requirements.lock.txt`
- **Docs:** [COMPLIANCE_MATRIX.md](docs/COMPLIANCE_MATRIX.md), [SUB_RQ1_DEMO.md](docs/SUB_RQ1_DEMO.md), [stress_experiment.md](docs/stress_experiment.md), [DR_VOSS_REVIEW_LOG.md](docs/DR_VOSS_REVIEW_LOG.md), **[THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md)** (RQs, DSR, scope, chapter spine)
- **Thesis draft pack (2026-04-07):** [THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md), [EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md), [THESIS_CUT_LIST.md](docs/THESIS_CUT_LIST.md); §10 in [THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md) links them
- **Sub-RQ2 + Discussion (2026-04-07):** [SUB_RQ2_ALTERNATIVES.md](docs/SUB_RQ2_ALTERNATIVES.md) (optional Sub-RQ2 wordings); [THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) §3b–3c (Sub-RQ relationship, velocity vs governance), Art. 14 one-liner

---

## Next (priority order)

1. **Sub-RQ1 (once):** Run [docs/SUB_RQ1_DEMO.md](docs/SUB_RQ1_DEMO.md) (tighten fairness threshold → gate fails) → export metrics → **revert** threshold to `0.70`.
2. **Thesis writing:** Use [docs/THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) + [docs/EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md); [docs/THESIS_EVAL_NOTES.md](docs/THESIS_EVAL_NOTES.md) + `experiment_comparison.json` + `human_oversight_latency.json` (Sub-RQ2: **7 s**).
3. **Git identity (optional):** `git config user.email "your@email"` if you still use a placeholder.
4. **Optional:** `python scripts/compare_profiles.py` after `params.yaml` changes; commit updated JSON.

---

## Current focus

- **Draft thesis evaluation** (DSR + Sub-RQ1 / Sub-RQ2) using committed metrics and the run link above.

---

## Blockers / decisions


| Item                              | Owner | Notes                                                      |
| --------------------------------- | ----- | ---------------------------------------------------------- |
| Fairness threshold `0.70`         | You   | Document sensitivity; tighten after mitigation experiments |
| `dvc.yaml` uses Windows venv path | You   | On Linux/Mac, change `cmd` to `.venv/bin/python src/...`   |


---

## How to update this file

1. Move finished items from **Next** into **Completed** (`[x]`).
2. Edit **Current focus** to one short line.
3. Bump **Last updated** to today’s date.
4. Optional: add MLflow run id / git commit next to completed items for audit trail.