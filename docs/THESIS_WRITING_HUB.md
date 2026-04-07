# Thesis writing hub — anchor documentation for the full journey

Use this file as the **single map** between **project work** (code, runs, CI) and **thesis output** (Word, ≥ **50 pages**, tables, figures). Update the **checklists** as you progress; keep [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) aligned with your faculty’s chapter template.

**Rule:** Every thesis chapter should trace to **this repo** (paths, JSON, workflows) or to **primary sources** (EUR-Lex). If a paragraph has no anchor, cut it or move it to an appendix.

**Scope of this hub:** Page/figure **planning** and **workflow**—not a second copy of RQs or legal mapping (those stay in [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md)). If this file and the foundation **conflict**, **foundation wins**—then fix this hub.

**Canonical precedence & deprecations:** [DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md).

**Draft thesis file:** [thesis/MANUSCRIPT.md](thesis/MANUSCRIPT.md) (expand literature and figures to reach programme page count).

---

## Dr. Voss — compliance guardrails (length is not a substitute for rigor)

- **Do not** pad to 50 pages with tool tutorials or generic AI ethics; use [THESIS_CUT_LIST.md](THESIS_CUT_LIST.md).  
- **Do** bind every substantive claim to **evidence** ([THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8) or **cited** law—not to README enthusiasm.  
- **Confirm** whether **references / appendices** count toward the page rule; programs differ.  
- **Claim discipline** for the Act: same as foundation—**operationalizes selected controls**, not “full compliance in code.”

---

## 1. Thesis output specification (≥ 50 pages)

Your program may use **page** or **word** limits. **50 pages** in Word usually means **body text + figures/tables + references**, excluding optional appendices depending on rules—**confirm with your supervisor**.

| Indicative budget | Pages (guide) | Typical content |
|-------------------|---------------|-----------------|
| Front matter + abstract + TOC | 3–6 | Title, declaration, abstract, lists |
| Introduction | 8–12 | Problem, gap, RQs, contributions, structure |
| Background & literature | 10–16 | RAI, MLOps, EU AI Act high-risk credit, gap |
| Theory / DSR framework | 4–8 | Hevner, GaC definition, Norway/Annex III scope |
| Methodology | 8–14 | Data, standard vs governed, gates, metrics, ethics |
| Instantiation (design) | 8–14 | Architecture, tooling, Gate A/B/C, traceability |
| Results | 6–12 | Sub-RQ1 comparison + blocking demo; Sub-RQ2 latency |
| Discussion | 6–10 | Principles, trade-offs, limits, implications |
| Conclusion | 3–6 | RQ answers, future work |
| References | 4–8 | EUR-Lex + papers you actually cite |
| Appendices | optional | JSON excerpts, params, screenshots, compliance matrix |

**Rough word anchor (narrative only):** ~250–350 words per page of **continuous prose** (11–12 pt, normal margins) → **about 12,500–17,500 words** of main text if you had **no** large tables. In practice, **Word’s page count includes** tables and figures—so you will **not** need that much prose if you use the planned tables/figures below.

**Tables and figures:** They **occupy pages** and **carry evidence**—plan **8–15** numbered tables and **6–12** figures for a technical DSR thesis; do not duplicate the same numbers in prose **and** tables without purpose.

**Alignment:** The chapter **outline** in [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §7 maps to the rows above—merge or split chapters to match your faculty template, not the other way around unless they allow it.

---

## 2. Anchor at each project journey stage

| Stage | What you do | Documentation to update or cite |
|-------|----------------|----------------------------------|
| **Scoping** | Fix RQs, Norway scope | [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §1–2; snippets §1b–1c |
| **Data** | Freeze raw source | [DATA_PROVENANCE.md](DATA_PROVENANCE.md); MLflow `data_provenance` |
| **Implementation** | Change gates, params | [params.yaml](../params.yaml); [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) row for that control |
| **Runs** | Train / compare / demo | [metrics/](../metrics/) JSON; MLflow run; [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md) if threshold demo |
| **CI / Gate C** | Workflows, latency | [human_oversight.md](human_oversight.md); `human_oversight_latency.json` + run URL |
| **Writing** | Chapters in Word | [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md); [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md) |
| **Review** | Examiner-ready | [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §9 checklist; [DR_VOSS_REVIEW_LOG.md](DR_VOSS_REVIEW_LOG.md) |

**When code changes materially:** add one line to [PROJECT_PLAN.md](../PROJECT_PLAN.md) **Completed** and, if needed, a short entry in [DR_VOSS_REVIEW_LOG.md](DR_VOSS_REVIEW_LOG.md).

---

## 3. Documentation reading order (thesis author)

1. [DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md) — charter: precedence, deprecations, full doc map  
2. [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) — spine: RQs, DSR, scope, evidence index  
3. [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md) — **this file**: pages, figures, journey  
4. [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) — paste-ready paragraphs and tables  
5. [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) — Act ↔ controls (scaffold → EUR-Lex in thesis)  
6. [compare_pipelines.md](compare_pipelines.md) — standard vs governed  
7. [human_oversight.md](human_oversight.md) — Gate C / Sub-RQ2 definition  
8. [THESIS_EVAL_NOTES.md](THESIS_EVAL_NOTES.md) — evaluation checklist  
9. [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md) / [stress_experiment.md](stress_experiment.md) — demos  
10. [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md) — legal primary source  

---

## 4. Tables — reuse vs thesis-only

| Table topic | Source in repo | Thesis action |
|-------------|----------------|---------------|
| RQ operationalization | [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §2, [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) §2 | Copy; renumber; add caption “Source: author.” |
| Proposal vs implementation | [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §4 | Copy as-is; cite dataset name |
| Compliance map | [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) | Rebuild in Word; **replace** Article text with EUR-Lex citations |
| Standard vs governed | [compare_pipelines.md](compare_pipelines.md), [experiment_comparison.json](../metrics/experiment_comparison.json) | One summary table + key metrics |
| Fairness / SHAP gate | [fairness_gate.json](../metrics/fairness_gate.json), [shap_gate.json](../metrics/shap_gate.json) | Export values at time of writing |
| Sub-RQ2 latency | [human_oversight_latency.json](../metrics/human_oversight_latency.json) | One small table + workflow URL |

---

## 5. Figures & images — checklist

Place exports and drafts under [figures/](figures/) (see [figures/README.md](figures/README.md)). **Minimum set** to support length and clarity:

| # | Figure | Suggested source |
|---|--------|------------------|
| F1 | High-level GaC architecture (standard vs governed) | Draw (PowerPoint / draw.io / Mermaid export) |
| F2 | Data + train + gates + MLflow/DVC flow | Same |
| F3 | CI matrix (standard vs governed jobs) | Screenshot of [ci.yml](../.github/workflows/ci.yml) run or diagram |
| F4 | Gate A/B/C decision flow | Diagram + pointer to scripts |
| F5 | MLflow UI (run with tags: git, params digest) | Screenshot |
| F6 | Fairness metric vs threshold (optional) | Table or small plot from `fairness_gate.json` |
| F7 | SHAP summary excerpt | Export from `artifacts/shap_report.md` or notebook |
| F8 | Gate C: Environment + approval (concept) | Diagram + [human_oversight.md](human_oversight.md) |

**Captions:** Every figure: what it shows, **which chapter/RQ** it supports, and **limitation** if it is a proxy (e.g. CI not bank).

---

## 6. Word thesis workflow (practical)

1. Use your faculty **.dotx** / chapter styles (Heading 1–3, caption, equation).  
2. **Paste** RQs from [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) §1c; **lock** wording after supervisor approval.  
3. **Insert** tables from §4 above; **link** file paths in footnotes or appendix (“artifact at commit …”).  
4. **Export** figures to PNG/PDF; store originals in [figures/](figures/); version with thesis date.  
5. **Track** page count in Word using the **same rules** your program uses (body-only vs everything). Aim **≥ 50** per that definition.  
6. **References:** Zotero / EndNote; pin **EUR-Lex** snapshot date for the AI Act.  
7. **Figures in Word:** Add **alt text** (accessibility); keep a **list of figures/tables** updated for the examiner PDF.  
8. **Reproducibility line** in appendix: **git commit** (short SHA) matching the metrics you quote—see MLflow tags / `experiment_comparison.json`.

---

## 7. Before submission — one pass

- [ ] Page count meets program rule (**≥ 50** with tables/figures per their definition).  
- [ ] Every RQ has an **answer paragraph** (snippets §3 + your numbers).  
- [ ] [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8 evidence index matches **committed** JSON and run URLs.  
- [ ] [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §9 Dr. Voss checklist complete.  
- [ ] Appendices: `params.yaml` excerpt, gate JSON, optional MLflow screenshot.  
- [ ] **No** broken path references to repo files (use commit hash or tag in appendix if needed).  
- [ ] **Figures:** every image has caption + alt text; screenshots state **date** and **environment** (e.g. GitHub run id).

---

*Maintainer: bump [PROJECT_PLAN.md](../PROJECT_PLAN.md) when this hub’s checklists change materially.*
