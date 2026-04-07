# Documentation foundation — project & thesis

This file is the **charter** for documentation quality: **what is authoritative**, **what is deprecated**, and **how to keep thesis docs aligned** with code. Read it **once** when joining the project; skim it before major thesis edits.

---

## 1. Authority & precedence (resolve conflicts here)

When two documents disagree, apply this order **from top (strongest) to bottom**:

| Priority | Source | Governs |
|----------|--------|---------|
| 1 | **`params.yaml` + `src/*.py` + `.github/workflows/*.yml`** | Actual runtime behavior (if **code** and **params** disagree, **code is what runs**—fix the mismatch; do not “document around” a bug) |
| 2 | **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md)** | Research questions, DSR mapping, scope, evidence index (§8), claim discipline |
| 3 | **[human_oversight.md](human_oversight.md)** | Gate C latency **definition** (includes Environment approval wait when configured) |
| 4 | **[compare_pipelines.md](compare_pipelines.md)** | **Standard** vs **governed** profiles and DVC vs `PIPELINE_PROFILE` |
| 5 | **[COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md)** | Act ↔ controls **scaffold** — **never** overrides **EUR-Lex** or supervisor-approved legal text in the thesis body |
| 6 | **README.md** (repo root) | Quick start; must stay consistent with **1**—fix README if it drifts |
| 7 | **[THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md)** | Page/figure **planning** only—never overrides **2** |

If **7** or **6** conflicts with **2**, **update the hub/README** after changing the foundation, not the other way around.

---

## 2. Deprecations & technical facts (avoid stale narratives)

| Topic | Canonical fact | Do not assume |
|-------|----------------|----------------|
| **MLflow store** | `mlflow.tracking_uri: sqlite:///./mlflow.db` in `params.yaml` | That the UI “lives in `mlruns/`” as the **primary** backend (legacy file store); use `--backend-store-uri` for SQLite |
| **`mlruns/`** | Gitignored; may appear if you switch tracking URI | That old runs are auto-migrated to SQLite |
| **Gate C** | Implemented by **workflows** + Environment, **not** by reading `gates.human_oversight.enabled_in_ci` in Python | That `enabled_in_ci` changes runtime (it is a **documentation flag**) |
| **P3 comparison metrics** | `metrics/experiment_comparison.json` has its own **`git_commit`** | That `metrics/train_metrics.json` always matches without re-running `scripts/compare_profiles.py` — see [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8 |
| **Sub-RQ1 demo (archived fail)** | `metrics/fairness_gate_subrq1_threshold_demo_fail.json` — threshold demo with `gate_passed: false` | That `metrics/fairness_gate.json` is always the failing snapshot (it reflects **last** run at 0.70 baseline after revert) |
| **`dvc.yaml`** | Uses **Windows** `.venv\Scripts\python.exe` in `cmd` | Same path on Linux/macOS — adjust to `.venv/bin/python` per [PROJECT_PLAN.md](../PROJECT_PLAN.md) blockers |

---

## 3. Thesis documentation map (all `docs/*.md`)

| Document | Role |
|----------|------|
| [DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md) | **This file** — precedence, deprecations, maintenance |
| [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) | **Spine:** RQs, DSR, scope, chapter outline, evidence §8, Voss checklist §9 |
| [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md) | ≥50 pages, journey anchors, tables/figures, Word workflow |
| [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) | Paste-ready paragraphs, operationalization tables, limitations |
| [THESIS_EVAL_NOTES.md](THESIS_EVAL_NOTES.md) | Evaluation angles + limitations bullets; defers RQs to foundation |
| [THESIS_CUT_LIST.md](THESIS_CUT_LIST.md) | Editorial: what to cut from the thesis draft |
| [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md) | EUR-Lex entry point for Regulation (EU) 2024/1689 |
| [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) | Obligation ↔ control scaffold |
| [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md) | Threshold demo for gate failure |
| [SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md) | Optional Sub-RQ2 wordings |
| [compare_pipelines.md](compare_pipelines.md) | Profiles, CI vs local, DVC note |
| [human_oversight.md](human_oversight.md) | Gate C setup + latency semantics |
| [DATA_PROVENANCE.md](DATA_PROVENANCE.md) | Dataset sources |
| [stress_experiment.md](stress_experiment.md) | Stress / bias training path |
| [GITHUB_SETUP.md](GITHUB_SETUP.md), [GATE_C_RUNBOOK.md](GATE_C_RUNBOOK.md) | GitHub / Gate C operations |
| [DR_VOSS_REVIEW_LOG.md](DR_VOSS_REVIEW_LOG.md) | Implementation & doc review trail |
| [figures/README.md](figures/README.md) | Thesis figure exports |
| [thesis/MANUSCRIPT.md](thesis/MANUSCRIPT.md) | **Thesis draft** (chapters 1–8 + appendices); export via [thesis/README.md](thesis/README.md) |

---

## 4. Who starts where?

| Reader | Start |
|--------|--------|
| **Thesis author (writing)** | [DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md) (this charter) → [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) → [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md) → [thesis/MANUSCRIPT.md](thesis/MANUSCRIPT.md) (draft) → snippets & citations |
| **Engineer (running code)** | [README.md](../README.md) → [compare_pipelines.md](compare_pipelines.md) |
| **Examiner traceability** | [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8 + committed `metrics/*.json` |

---

## 5. Maintenance triggers (keep docs excellent)

| Event | Update |
|-------|--------|
| Change **gates, thresholds, or profiles** | `params.yaml`; row in [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) if mapping changes; [PROJECT_PLAN.md](../PROJECT_PLAN.md) |
| Change **workflows or Gate C** | [human_oversight.md](human_oversight.md), [GATE_C_RUNBOOK.md](GATE_C_RUNBOOK.md) if behavior changes |
| New **thesis-facing batch** | [DR_VOSS_REVIEW_LOG.md](DR_VOSS_REVIEW_LOG.md) (short entry) |
| **Regenerate** P3 evidence for final thesis | Run `python scripts/compare_profiles.py`; commit `experiment_comparison.json`; note commit in appendix |

---

*This charter is the **documentation foundation**; it changes rarely. Bump [PROJECT_PLAN.md](../PROJECT_PLAN.md) when it does.*
