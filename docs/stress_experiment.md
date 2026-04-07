# Stress experiment — Sub-RQ1 “bad model” path

**Intent:** Show that the **governed** pipeline can **block or flag** a model that a **standard** (performance-only) path might still ship.

**Mechanism:** After the usual train/val split, **training rows** are undersampled for the **rarest** `famges` (sensitive) level. Validation data is unchanged. The model overfits majority-sensitive patterns; **equalized odds** on validation typically **worsens**.

**Run locally (PowerShell):**

```powershell
cd C:\Users\Chau_\Projects\eu-ai-act-gac-credit
$env:STRESS_BIAS="1"
.\.venv\Scripts\python.exe src\train.py
.\.venv\Scripts\python.exe src\gate_fairness.py
```

**Modes:** `STRESS_MODE=undersample` (default) or `STRESS_MODE=remove_rare` (drops all training rows with the rarest sensitive level). **If EOD barely moves**, use [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md) (threshold-only demo) instead — it always “fails” when the policy is stricter than the metric.

**Expected:** `gate_passed: false` only if EOD exceeds `max_equalized_odds_difference` (often easier via **threshold** demo than via stress).

**Reset:** `Remove-Item Env:STRESS_BIAS` and run `dvc repro` with `stress.enabled: false` (default).

**Thesis:** One paragraph + table: standard metrics vs governed **gate failure** under stress.
