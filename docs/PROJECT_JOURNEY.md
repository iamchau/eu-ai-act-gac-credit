# Project journey — detailed checklist

**Purpose:** A **granular**, **tickable** view of what is **done** vs **left to do** at any point.  
**Overview & phases:** [PROJECT_PLAN.md](../PROJECT_PLAN.md) (single page — update **Last updated** there after meaningful progress).  
**Authority:** RQs, claims, and evidence binding still follow [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md); this file does **not** override it.

**How to use**

1. Tick `- [x]` when an item is **truly** complete (not “draft exists”).
2. After a batch of ticks, bump **[PROJECT_PLAN.md](../PROJECT_PLAN.md)** — **Last updated**, **Completed**, **Next**, **Current focus**.
3. Weekly (or each sprint): skim **Blockers** in [PROJECT_PLAN.md](../PROJECT_PLAN.md) and **§E** below.

---

## At a glance


| Track              | Focus                                   | Typical stage                  |
| ------------------ | --------------------------------------- | ------------------------------ |
| **A — Evidence**   | Committed metrics ↔ thesis tables match | Before locking Results         |
| **B — Thesis**     | Manuscript → Word, figures, citations   | Main calendar effort           |
| **C — MLOps**      | Backlog: `/metrics`, registry push      | Parallel or pre-defence sprint |
| **D — Submission** | Faculty format, appendices, PDF         | Final weeks                    |
| **E — Hygiene**    | Git identity, lockfile, doc drift       | Ongoing                        |


---

## A. Evidence & reproducibility (freeze before final Results)

Tick when the **committed repo** matches what the **thesis cites**. A **submission checklist** table is in **Appendix E** of [thesis/MANUSCRIPT.md](thesis/MANUSCRIPT.md).

- `**params.yaml`** for the thesis run is **committed** and **stable** (or change is intentional with re-run below).
- `**metrics/experiment_comparison.json`** regenerated: `python scripts/compare_profiles.py` after last relevant `params.yaml` change; **committed**; `**git_commit`** inside file noted in thesis if required by faculty.
- **Gate metrics** cited in thesis match **committed** files: `metrics/fairness_gate.json`, `metrics/shap_gate.json` (or archived demo where cited).
- **Sub-RQ1 demo / threshold fail** (if cited): `metrics/fairness_gate_subrq1_threshold_demo_fail.json` present and referenced correctly.
- **Sub-RQ2** (if cited): `metrics/human_oversight_latency.json` + workflow URL; **n** and **limitation** (CI proxy) stated in thesis — see [human_oversight.md](human_oversight.md).
- **MLflow / digests** (if cited): `train_metrics.json` / tags align with narrative; no silent mismatch with `experiment_comparison.json` — see [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8.
- **DVC** (if you claim reproducibility via DVC): `dvc repro` or CI path documented; **Windows `dvc.yaml` paths** acknowledged if relevant.

---

## B. Thesis manuscript (`docs/thesis/MANUSCRIPT.md` → Word)

Use [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md) for page/figure budget. Tick **final** quality, not first draft.

### B.1 Structure & spine

- **Roadmap** — [EXCELLENCE_ROADMAP.md](EXCELLENCE_ROADMAP.md) (phases A–G); author meta + **evidence-freeze git tag** steps in [thesis/README.md](thesis/README.md), not in the main argument.
- **Abstract** — problem, method, findings, contribution, **one** limitation.
- **Introduction** — RQs with **thesis-ready one-liners** ([THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §2); chapter map; scope honest (no bank case study).
- **Conclusion** — **explicit answers** to Primary RQ + Sub-RQs tied to evidence paths.

### B.2 Chapters (align titles with faculty template if different)

- **Ch. 1 — Introduction** (final pass after Results stable).
- **Ch. 2 — Background / literature** (responsible AI, MLOps, EU AI Act high-risk framing).
- **Ch. 3 — Theory / DSR / GaC** (Hevner cycle, construct vs instantiation).
- **Ch. 4 — Methodology** — data, standard vs governed, gates, **limitations** block.
- **Ch. 5 — Instantiation** — repo architecture; **§5.4 CI / Gate C**, **§5.5 MLOps** aligned with [deployment/ML_OPS_SERVING_ANALYSIS.md](deployment/ML_OPS_SERVING_ANALYSIS.md) limits.
- **Ch. 6 — Results** — Sub-RQ1 (comparison + demo); Sub-RQ2 (latency); tables bound to **committed JSON**.
- **Ch. 7 — Discussion** — design principles, trade-offs, **what banks could adapt**, limits; Dr. Voss claim discipline.
- **Ch. 8 — Conclusion** — RQ answers; future work; Norway/transposition if required.

### B.3 Citations, figures, export

- **EUR-Lex / primary legal** for AI Act — [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md); no invented Article text.
- **Figures** — [figures/README.md](figures/README.md); captions state limits if proxy / not bank production.
- **Pandoc → Word** — [thesis/README.md](thesis/README.md); template per faculty.
- **THESIS_CUT_LIST.md** — final trim pass.
- **Supervisor review** — round(s) recorded per programme rules.

---

## C. MLOps (committed scope)

**Already in repo:** FastAPI serving, Docker/Compose, CI `docker-build` tarball, **`GET /metrics`**, GHCR push on **`push`** / **`workflow_dispatch`**, `/health`, `/ready`, `/version`, `/predict`, rate limit, RUNBOOK, extension catalog — see [PROJECT_PLAN.md](../PROJECT_PLAN.md).

- [x] **`GET /metrics`** (minimal process JSON) — [deployment/ML_OPS_SERVING_ANALYSIS.md](deployment/ML_OPS_SERVING_ANALYSIS.md) §7, [deployment/TECHNICAL_EXTENSIONS.md](deployment/TECHNICAL_EXTENSIONS.md) **C8**.
- [x] **Container registry push** (GHCR) — [`.github/workflows/docker-build.yml`](../.github/workflows/docker-build.yml); [RUNBOOK.md](deployment/RUNBOOK.md); [README.md](../README.md) **Serving**.

---

## D. Submission & defence prep

- **Faculty PDF/Word** — margins, front matter, page numbering per guide.
- **Appendices** — params excerpt, key JSON, compliance matrix, optional CI screenshots ([THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §7 outline).
- **Authorship / declarations** — programme forms.
- **Defence deck** (if required) — repo clone path, one-slide evidence map (`metrics/*.json`).
- **Archive** — tag release or zip snapshot if faculty requires fixed artefact.

---

## E. Ongoing hygiene (low friction)

- `**git config user.email`** — real address for commits (if not done).
- `**requirements.lock.txt**` — regenerate when `requirements.txt` meaningfully changes (`pip freeze` or tool you use).
- **DR_VOSS_REVIEW_LOG** — short entry after large thesis-facing doc batches ([DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md)).
- **Linux/macOS DVC** — if you use `dvc repro` off Windows, adjust `dvc.yaml` `cmd` ([PROJECT_PLAN.md](../PROJECT_PLAN.md) blockers).

---

## F. When to tick “project complete” (thesis + repo goals)

Minimum:

- Track **A** satisfied for all cited numbers.
- Track **B** manuscript submitted per faculty.
- Track **C** done **if** you committed to full MLOps scope in [PROJECT_PLAN.md](../PROJECT_PLAN.md); else document deferral in **Next** with reason.

---

*Maintainer: this is a **working** checklist — trim rows if your faculty drops a chapter; add rows for programme-specific forms.*