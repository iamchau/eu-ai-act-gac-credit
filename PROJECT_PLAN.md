# Thesis project plan & status

**Last updated:** 2026-04-07 (P3 maintenance: `fix_manuscript_inline_md.py` on PROJECT_PLAN + MANUSCRIPT; `verify_thesis_metrics.py` OK)

This file is the **single overview** for scope, what is done, and what comes next. After each meaningful task, update **Last updated**, **Completed**, and **Next** (one minute).

**Detailed journey (tickable tracks A–F):** [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) — use for week-to-week visibility; keep this file as the executive summary.

---

## Phases (high level)


| Phase     | Goal                                                          | Status          |
| --------- | ------------------------------------------------------------- | --------------- |
| P0        | Repo + Python stack + MLflow + DVC baseline                   | **Done**        |
| P1        | Fairness gate (Fairlearn) + SHAP gate + metrics in CI         | **Done**        |
| P2        | Human-in-the-loop gate (GitHub Actions) + latency measurement | **Done** (CI)   |
| P3        | Standard vs governed experiment + thesis write-up             | **In progress** |
| **MLOps** | Serving API, Docker, CI image, **`/metrics`**, **GHCR push**  | **Done**        |


---

## MLOps serving — status

**In scope (not optional):** Train writes **`artifacts/model.joblib`** + **`artifacts/feature_schema.json`**. **`docker compose up --build`** mounts `./artifacts`. FastAPI [serving/app.py](serving/app.py): **`/health`**, **`/ready`**, **`/version`**, **`/predict`**; configurable via **`SERVING_API_KEY`**, **`MAX_BODY_BYTES`**, **`RATE_LIMIT_PREDICT`**, JSON access logs (**`LOG_JSON_ACCESS`**). **[scripts/smoke_serving.py](scripts/smoke_serving.py)** smoke test. **[.github/workflows/docker-build.yml](.github/workflows/docker-build.yml)** CI train → Docker image artefact; **[docs/deployment/RUNBOOK.md](docs/deployment/RUNBOOK.md)**. **[docs/deployment/TECHNICAL_EXTENSIONS.md](docs/deployment/TECHNICAL_EXTENSIONS.md)** = full catalog; **[docs/deployment/ML_OPS_SERVING_ANALYSIS.md](docs/deployment/ML_OPS_SERVING_ANALYSIS.md)** = analysis + **§8** career note; README **Serving**; manuscript §5.5.

**Completed (2026-04-07):** **`GET /metrics`** (minimal JSON process stats) — [serving/app.py](serving/app.py); **GHCR** (`docker-build.yml` pushes on **`push`** / **`workflow_dispatch`**) — [RUNBOOK.md](docs/deployment/RUNBOOK.md).

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
- **Project journey (2026-04-07):** [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) — tickable tracks (evidence, thesis, MLOps, submission, hygiene); pairs with this file
- **Sub-RQ1 threshold demo (2026-04-07):** Tightened `max_equalized_odds_difference` **0.70 → 0.55** → gate **failed** → archived `[metrics/fairness_gate_subrq1_threshold_demo_fail.json](metrics/fairness_gate_subrq1_threshold_demo_fail.json)`; threshold **reverted** to `0.70`; `python scripts/compare_profiles.py` → updated `[metrics/experiment_comparison.json](metrics/experiment_comparison.json)`
- **Thesis manuscript (2026-04-07):** [docs/thesis/MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — full draft (Intro–Conclusion, appendices); [docs/thesis/README.md](docs/thesis/README.md) — Pandoc → Word
- **MLOps serving (2026-04-07):** [serving/](serving/) FastAPI, [Dockerfile](Dockerfile), [docker-compose.yml](docker-compose.yml), [requirements-serving.txt](requirements-serving.txt); [docs/deployment/ML_OPS_SERVING_ANALYSIS.md](docs/deployment/ML_OPS_SERVING_ANALYSIS.md); README **Serving**; manuscript §5.5
- **Serving extensions (2026-04-07):** `train.py` → `artifacts/feature_schema.json`; serving: API key, max body, JSON access logs; [scripts/smoke_serving.py](scripts/smoke_serving.py); [docs/deployment/TECHNICAL_EXTENSIONS.md](docs/deployment/TECHNICAL_EXTENSIONS.md)
- **Serving CI + ops (2026-04-07):** [docker-build.yml](.github/workflows/docker-build.yml); `/ready`; `slowapi` rate limit; [RUNBOOK.md](docs/deployment/RUNBOOK.md)
- **Thesis alignment (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) §4.4 gate roles + P3 evidence binding; §4.5 ethics (renumbered); §5.2 Gate B row; [THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md) §8 serving row + Gate B note + Dr. Voss checklist item
- **MLOps backlog (2026-04-07):** **`GET /metrics`** (minimal JSON: uptime, PID, **`predict_success_total`**, etc.); **`docker-build.yml`** **GHCR** push (`:serving-<sha>`, `:latest`) on **`push`** / **`workflow_dispatch`**; [smoke_serving.py](scripts/smoke_serving.py) updated; [README.md](README.md), [RUNBOOK.md](docs/deployment/RUNBOOK.md), [TECHNICAL_EXTENSIONS.md](docs/deployment/TECHNICAL_EXTENSIONS.md), [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) §5.5
- **Manuscript excellence pass (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — **Table 1a** chapter map (RQ signposting); §2.2 MLOps/compliance prose (placeholder removed); Discussion **Sub-RQ relation** + **contribution triad** §7.2; Conclusion explicit RQ answers; **Appendix E** Track A binding checklist; [PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) §A pointer
- **Manuscript depth pass (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — expanded **Ch. 2** (fairness metrics, MLOps, Act, Norway/EEA); **Ch. 3** (Hevner/Peffers, construct vs instantiation); **§4.1** evaluation stance; **Discussion** §7.4–7.6 (practice, velocity, future work); **§9 References** (APA-style core list); **Appendix F** Mermaid Figure 1 + optional figures; [AGENTS.md](AGENTS.md) — agent owns thesis writing, human manual-only steps
- **Manuscript continuation (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — **§4.6–4.7** (`compare_profiles` vs CI matrix; Sub-RQ2 epochs); **§5.4** CI / Gate C / `governed_deploy` / docker-build pointer; **§5.5** serving API (former §5.4); **Appendix B** Table B1 compliance mapping; **§6.3** epoch fields; references alphabetised; cross-refs **§5.5** in [PROJECT_PLAN.md](PROJECT_PLAN.md), [PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md), [ML_OPS_SERVING_ANALYSIS.md](docs/deployment/ML_OPS_SERVING_ANALYSIS.md), [DR_VOSS_REVIEW_LOG.md](docs/DR_VOSS_REVIEW_LOG.md)
- **Manuscript continuation 2 (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — **Abstract** aligned with JSON binding + Sub-RQ2 epochs; **§2.6–2.7** (Jobin *et al.*, Mehrabi *et al.*); **Chapter 8** split **§8.1 / §8.2**; references **Jobin**, **Mehrabi**; [figures/Fig01_gac_architecture.mmd](docs/figures/Fig01_gac_architecture.mmd), [figures/Fig02_ci_matrix.mmd](docs/figures/Fig02_ci_matrix.mmd); [figures/README.md](docs/figures/README.md) export hints
- **Manuscript continuation 3 (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — **§3.4** evaluation (functional / comparative / demonstrative / Sub-RQ2); **§6.4** integrated reading of Tables 2–3 + §6.3; **§2.3** secondary commentary (Veale & Zuiderveen Borgesius, 2021); reference **Veale**; **§3.1** pointer to §3.4; Table 1a rows Ch.3/6
- **Manuscript continuation 4 (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — **§1.4.1** signposting (§3.4, §6.4, Appendix E, §4.8); **§4.8** reliability (validation-only gates, n=1 Sub-RQ2, no bootstrap); **§7.3** cross-ref **§4.8**; Chapter 4 narrative in **§1.5**
- **Manuscript continuation 5 (2026-04-07):** [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — **Chapter 6** opening reader note (committed JSON only; interpretation in Ch.7); **§4.5** trimmed to ethics + deployment + pointers to **§4.7–4.8** (removed duplicate Sub-RQ bullets)
- **Foundation alignment (2026-04-07):** [THESIS_FOUNDATION.md](docs/THESIS_FOUNDATION.md) — **§7** Results bullet (reader note, §6.4); **§8** “Chapter 6 rule” + evidence table **MLOps** row (`/metrics`, GHCR); [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) **§6.4** ties to Chapter 6 lead-in
- **Documentation charter (2026-04-07):** [DOCUMENTATION_FOUNDATION.md](docs/DOCUMENTATION_FOUNDATION.md) — **§1** paragraph + **§2** table row (Results discipline); **§5** maintenance row; [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) **§6.3** list formatting fix
- **Repo hygiene (2026-04-07):** [.gitignore](.gitignore) — `thesis-draft.docx`, `~$*.docx`; [scripts/verify_thesis_metrics.py](scripts/verify_thesis_metrics.py) — JSON sanity check for thesis; [scripts/fix_manuscript_inline_md.py](scripts/fix_manuscript_inline_md.py) — optional path args; [PROJECT_PLAN.md](PROJECT_PLAN.md) — **`…`** inline-code normalization
- **Markdown hygiene (maintenance):** [PROJECT_PLAN.md](PROJECT_PLAN.md) + [MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) — rerun automated **`…`** normalization; thesis metrics JSON verify pass

---

## Next (priority order)

1. **Thesis writing (Word):** [docs/THESIS_WRITING_HUB.md](docs/THESIS_WRITING_HUB.md) → [docs/THESIS_DRAFT_SNIPPETS.md](docs/THESIS_DRAFT_SNIPPETS.md) + [docs/EU_AI_ACT_CITATIONS.md](docs/EU_AI_ACT_CITATIONS.md); cite `experiment_comparison.json`, `fairness_gate_subrq1_threshold_demo_fail.json`, `human_oversight_latency.json` (Sub-RQ2 sample **7 s**, run [24081106560](https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560)); figures → [docs/figures/](docs/figures/).
2. **Git identity (optional):** `git config user.email "your@email"` if you still use a placeholder.
3. **After `params.yaml` changes:** Re-run `python scripts/compare_profiles.py` and commit `experiment_comparison.json`.
4. **Evidence lock (Track A):** Walk **Appendix E** in [docs/thesis/MANUSCRIPT.md](docs/thesis/MANUSCRIPT.md) before final PDF; full list — [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) §A.

---

## Current focus

- **Agent lead:** Word export + literature depth + figures ([THESIS_WRITING_HUB.md](docs/THESIS_WRITING_HUB.md)); execute **Track A** checks via Appendix E + journey §A. Student: supervisor, faculty format, submission. See [AGENTS.md](AGENTS.md) lead mandate.

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

