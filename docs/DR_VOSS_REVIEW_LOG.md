# Dr. Ingrid Voss — implementation review log

*Concise, compliance-first notes. Update when the instantiation changes materially.*

---

## 2026-04-07 — Foundation + stress feature batch

**Approved**

- **Reproducibility:** `git_commit`, `params_yaml_sha16`, `dvc_lock_sha16` logged to MLflow tags and `train_metrics.json` — auditable without hand-waving.
- **MLflow store:** move to **SQLite** (`sqlite:///./mlflow.db`) — aligns with MLflow direction; file store deprecated.
- **Stress path:** training-only undersampling of rare sensitive level — **legitimate** for demonstrating gate **failure**; must be **disclosed** as synthetic harm injection, not “real bank bias.”
- **Compliance matrix:** single-page map from Act themes to controls — **required** for examiner navigation.

**Conditions**

- **COMPLIANCE_MATRIX** Article references: student must **swap in** faculty-cited EUR-Lex strings; my table is a **scaffold**.
- **Stress:** If gate does not fail at default `minority_keep_fraction`, **tighten threshold** or **lower fraction** until one clean fail — otherwise Sub-RQ1 story is weak.
- **SQLite:** Old `mlruns/` experiments are **not** migrated automatically; thesis runs should use **new** runs from SQLite unless you document migration.

**Verdict:** Proceed. Next review after first **documented** stress run with `gate_passed: false` captured in metrics.

---

## 2026-04-07 — Follow-up (threshold demo)

**Approved**

- **SUB_RQ1_DEMO.md** — Policy tightening (`max_equalized_odds_difference` **0.70 → 0.55**) is the **primary** demonstration that GaC **blocks** when rules tighten; stress modes are **secondary** (EOD did not move enough under undersample/remove_rare alone for this baseline).

**Action:** Student runs one **failing** fairness gate (threshold demo), exports JSON, then **reverts** threshold to 0.70 for the main baseline narrative.

---

## 2026-04-07 — Thesis foundation (document)

**Approved**

- **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md)** — **Operational** definitions for Primary RQ and Sub-RQs; **Hevner** mapping; **scope** table (Norway, `famges`, GitHub vs “digital signature”); **claim discipline** for EU AI Act; **chapter outline**; **evidence index**; **pre-flight checklist**.

**Conditions**

- **Legal:** Replace scaffold Article references in [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) with **EUR-Lex** citations your supervisor approves.  
- **Sub-RQ1:** Do not imply **sampled production approval rates** — use **defined** standard vs governed + **policy/threshold** demo.  
- **Sub-RQ2:** **One** latency number is **illustrative**; state **CI** limits in **one** explicit paragraph.

**Verdict:** Thesis **spine** is now **auditable**. Writing quality is yours; **structure** is no longer hand-waving.

---

## 2026-04-07 — Thesis draft improvements (paste-ready pack)

**Approved**

- **[THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md)** — Introduction **positioning**; methodology **operationalization** tables; **explicit answer sketches** for Primary RQ and Sub-RQs; **single consolidated** limitations block (avoid scattering).
- **[EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md)** — Primary **EUR-Lex** entry point for Regulation (EU) 2024/1689 (`CELEX:32024R1689`); citation discipline reminder.
- **[THESIS_CUT_LIST.md](THESIS_CUT_LIST.md)** — Editorial list: trim tool fluff, generic ethics, duplicate caveats; keep RQs and contributions sharp.
- **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §10** — Index of the above.

**Conditions**

- Replace bracketed placeholders and sample latency with **your** final run outputs.  
- **COMPLIANCE_MATRIX.md** remains a **scaffold** until Articles are verified against EUR-Lex in the thesis body.

**Verdict:** Dr. Voss structural feedback is **materialized** in-repo; drafting can proceed without re-deriving paragraphs from chat history.

---

## 2026-04-07 — RQ wording + Sub-RQ parity (doc pass)

**Approved**

- **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §2:** Thesis-ready **one-liners** for Introduction; **Sub-RQ2** answers vs does-not-answer table; **Sub-RQ parity** note (complementary, not symmetric).  
- **§8:** Minimum **evidence bundles** for Sub-RQ1 (comparison + blocking demo) and Sub-RQ2 (JSON + URL + **n**).  
- **[THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md):** §1b Norway/Annex III; §1c RQ one-liners; §2.4 Sub-RQ2 scope; §5 evidence checklist.

**Verdict:** Reduces examiner risk from **informal proposal phrasing** and **misread Sub-RQ2** as banking latency.

---

## 2026-04-07 — Sub-RQ2 alternatives + Discussion stubs

**Approved**

- **[SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md)** — Default **latency** Sub-RQ2 plus optional **traceability**, **oversight-as-design**, and **trade-offs** wordings; evidence notes; **do not** stack without faculty approval.  
- **[THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md)** — **Art. 14** functional-analogue one-liner; **§3b** Sub-RQ relationship; **§3c** velocity vs governance; evidence checklist points to alternatives doc.  
- **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md)** — Core-claim **note** if Sub-RQ2 is swapped; §2 link; §10 index.

**Verdict:** Supervisory choice on Sub-RQ2 is **documented**; default repo thesis remains **latency**-aligned.

---

## 2026-04-07 — Cross-audit: thesis ↔ code ↔ workflows

**Approved (doc corrections)**

- **Sub-RQ2 semantics:** [human_oversight.md](human_oversight.md) already stated latency **includes** Environment approval wait; [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) and [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) were updated to **match** (removed incorrect “excludes reviewer/queue” wording).  
- **README:** MLflow tracking is **`sqlite:///./mlflow.db`** — not `mlruns/` as primary UI path.  
- **compare_pipelines.md:** `dvc repro` vs `PIPELINE_PROFILE` / **standard** baseline clarified.  
- **SUB_RQ1_DEMO.md:** EOD range aligned with committed `experiment_comparison.json`.  
- **PROJECT_PLAN.md:** branch name typo (`main`).

**Verdict:** No code change required for Sub-RQ2 — **measurement** was already correct; **thesis** text had drifted.

---

## 2026-04-07 — Thesis writing hub (≥50 pages, journey anchors)

**Approved**

- **[THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md)** — Page/word **guide**, chapter budget, **stage→doc** anchor table, reading order, table/figure inventory, Word workflow, pre-submission checklist.  
- **[figures/README.md](figures/README.md)** — Naming and export guidance.  
- **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §10** — Links hub + figures.

**Verdict:** Documentation **foundation** is now **explicit** for the full thesis journey; student must still **confirm** page-count rules with faculty.

---

## 2026-04-07 — Thesis writing hub (follow-up review)

**Approved**

- **Scope clause** — Hub **does not** duplicate RQs/legal spine; **foundation wins** on conflict.  
- **Dr. Voss guardrails** — No padding; evidence binding; confirm what counts toward page total.  
- **Word count** — Clarified: prose estimate vs Word page count including tables/figures.  
- **Foundation §7** — Linked to hub page budget.  
- **Submission** — Alt text, git SHA in appendix, screenshot metadata.  
- **[figures/README.md](figures/README.md)** — Caption template, resolution, accessibility.

**Verdict:** Hub is **usable** for examiners; **length** is planned without inviting fluff.

---

## 2026-04-07 — Full-doc consistency pass

**Approved**

- **README:** `pipelines/` was misdescribed (folder empty); **`.github/workflows/`** added to layout table.  
- **PROJECT_PLAN:** `standard`/`governed` formatting; **`metrics/...`** path markup cleaned.  
- **THESIS_FOUNDATION §8:** Note on **`experiment_comparison.json`** `git_commit` vs last **`train_metrics.json`**.  
- **THESIS_EVAL_NOTES:** Gate C wording aligned with **human_oversight.md**; which metric file to cite for P3.  
- **params.yaml:** `gates.human_oversight.enabled_in_ci` clarified as **documentation-only** (Gate C is workflow-driven).

**Verdict:** Reduces silent **thesis↔metrics** mismatch when students re-train without re-running **`compare_profiles.py`**.

---

## 2026-04-07 — Documentation foundation (charter)

**Approved**

- **[DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md)** — Single **precedence** table (code → thesis spine → hub); **deprecations** (MLflow, Gate C flag, metrics/git); **full doc map**; **maintenance triggers**; reader entry points.  
- **Wired** into [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §10, [README.md](../README.md), [AGENTS.md](../AGENTS.md), [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md), [THESIS_EVAL_NOTES.md](THESIS_EVAL_NOTES.md), [figures/README.md](figures/README.md), [PROJECT_PLAN.md](../PROJECT_PLAN.md).

**Verdict:** Thesis documentation has an explicit **foundation**; conflicts resolve by **procedure**, not guesswork.

---

## 2026-04-07 — Documentation charter (micro-edit)

**Approved**

- **Precedence row 1:** Clarified **code vs params** — code is what runs; mismatch = **bug**, not narrative workaround.  
- **COMPLIANCE_MATRIX:** Explicit that scaffold **never** overrides **EUR-Lex** / approved legal text.  
- **§4 Thesis author path** aligned with hub: **charter → foundation → hub → …**  
- **§3 map:** Self-row for this file.

**Verdict:** Charter is **examiner-safe** on legal hierarchy and **implementation** truth.

---

## 2026-04-07 — Sub-RQ1 threshold demo executed + P3 JSON refreshed

**Approved**

- **`max_equalized_odds_difference` 0.70 → 0.55** → fairness gate **failed** (EOD ~0.617 > 0.55); archived **[`metrics/fairness_gate_subrq1_threshold_demo_fail.json`](../metrics/fairness_gate_subrq1_threshold_demo_fail.json)**.  
- **Reverted** to **0.70**; **`scripts/compare_profiles.py`** re-run — **`experiment_comparison.json`** updated (git commit at generation time recorded in file).  
- **[THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8**, **[SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md)**, **[DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md)** — pointers to archived fail JSON.

**Verdict:** Sub-RQ1 **blocking** demonstration is now **artifact-backed** in-repo, not chat-only.

---

## 2026-04-07 — Thesis manuscript (`MANUSCRIPT.md`)

**Approved**

- **[thesis/MANUSCRIPT.md](thesis/MANUSCRIPT.md)** — Full draft: abstract, Ch.1–8, references scaffold, appendices (params, compliance pointer, metric JSON); numbers aligned to **`metrics/experiment_comparison.json`**, **`fairness_gate_subrq1_threshold_demo_fail.json`**, **`human_oversight_latency.json`**.  
- **[thesis/README.md](thesis/README.md)** — Pandoc export to `.docx`.

**Conditions**

- Student **expands** Chapter 2–3 and references to meet **faculty** page and citation rules; **replace** bracketed metadata; **add** figures from [figures/README.md](figures/README.md).

**Verdict:** Thesis is **writable** from the repo; **length** and **legal** citations remain student/supervisor work.
