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
