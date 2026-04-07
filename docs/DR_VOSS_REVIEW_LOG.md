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
