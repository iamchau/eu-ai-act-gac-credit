# Thesis project plan & status

**Last updated:** 2026-04-07 (agent lead mandate — thesis)

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
- `params.yaml` + `dvc.yaml`: train → fairness_gate → shap_gate; `pipeline.profile` (`standard` or `governed`)
- `src/train.py` + `src/data_loading.py`: MLflow + `pipeline_profile`; gate artifacts
- Gates A–B: `gate_fairness.py`, `gate_shap.py` + metrics JSON
- Gate C: `governed_deploy.yml` + `metrics/human_oversight_latency.json` archived (run [24081106560](https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560), **7 s** human-oversight latency)
- CI matrix: `ci.yml` runs standard (train only) and governed (train + gates)
- `docs/compare_pipelines.md` — standard vs governed comparison table
- `scripts/compare_profiles.py` + `metrics/experiment_comparison.json` — local P3 tabulation (same seed)
- `docs/GITHUB_SETUP.md`, `docs/GATE_C_RUNBOOK.md`
- `docs/THESIS_EVAL_NOTES.md` — limitations + artifact checklist for writing
- **GitHub:** `origin` → `https://github.com/iamchau/eu-ai-act-gac-credit.git`, branch `main`, pushed
- **Foundation (2026-04-07):** MLflow **SQLite** (`mlflow.db`), `src/run_context.py` digests (**git**, **params.yaml**, **dvc.lock**), `requirements.lock.txt`
- **Docs:** [COMPLIANCE_MATRIX.md](docs/COMPLIANCE_MATRIX.md), [SUB_RQ1_DEMO.md](docs/SUB_RQ1_DEMO.md), [stress_experiment.md](docs/stress_experiment.md), [DR_VOSS_REVIEW_LOG.md](docs/DR_VOSS_REVIEW_LOG.md), **[THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md)** (RQs, DSR, scope, chapter spine)
- **Thesis draft pack (2026-04-07):** [THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md), [EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md), [THESIS_CUT_LIST.md](docs/THESIS_CUT_LIST.md); §10 in [THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md) links them
- **Sub-RQ2 + Discussion (2026-04-07):** [SUB_RQ2_ALTERNATIVES.md](docs/SUB_RQ2_ALTERNATIVES.md) (optional Sub-RQ2 wordings); [THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) §3b–3c (Sub-RQ relationship, velocity vs governance), Art. 14 one-liner
- **Thesis documentation anchor (2026-04-07):** [THESIS_WRITING_HUB.md](docs/THESIS_WRITING_HUB.md) — **≥50 pages** budget, journey-stage anchors, table/figure checklist, Word workflow; [figures/README.md](docs/figures/README.md); §10 [THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md)
- **Documentation foundation (2026-04-07):** [DOCUMENTATION_FOUNDATION.md](docs/DOCUMENTATION_FOUNDATION.md) — authority order, deprecations, full `docs/` map, maintenance triggers
- **Sub-RQ1 threshold demo (2026-04-07):** Tightened `max_equalized_odds_difference` **0.70 → 0.55** → gate **failed** → archived `[metrics/fairness_gate_subrq1_threshold_demo_fail.json](metrics/fairness_gate_subrq1_threshold_demo_fail.json)`; threshold **reverted** to `0.70`; `python scripts/compare_profiles.py` → updated `[metrics/experiment_comparison.json](metrics/experiment_comparison.json)`
- **Thesis manuscript (2026-04-07):** [docs/thesis/MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — full draft (Intro–Conclusion, appendices); [docs/thesis/README.md](docs/thesis/README.md) — Pandoc → Word

---

## Next (priority order)

1. **Thesis writing (Word):** [docs/THESIS_WRITING_HUB.md](docs/THESIS_WRITING_HUB.md) → [docs/THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) + [docs/EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md); cite `experiment_comparison.json`, `fairness_gate_subrq1_threshold_demo_fail.json`, `human_oversight_latency.json` (Sub-RQ2 sample **7 s**, run [24081106560](https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560)); figures → [docs/figures/](docs/figures/).
2. **Git identity (optional):** `git config user.email "your@email"` if you still use a placeholder.
3. **After `params.yaml` changes:** Re-run `python scripts/compare_profiles.py` and commit `experiment_comparison.json`.

---

## Current focus

- **Agent lead:** Drive thesis completion in-repo—primarily [docs/thesis/MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) expansion (lit/theory/figures), doc alignment, evidence integrity; student handles faculty submission, supervisor, defence. See [AGENTS.md](AGENTS.md) lead mandate.

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

