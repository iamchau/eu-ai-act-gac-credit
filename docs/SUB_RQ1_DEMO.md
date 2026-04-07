# Sub-RQ1 demo — gate blocks deployment when policy tightens

**Dr. Voss:** The cleanest **non-hand-waving** demonstration is **policy-as-code**: **identical** code and data, **only the threshold** changes.

## Steps

1. Note current fairness: `metrics/fairness_gate.json` — `abs_equalized_odds_difference` is often **~0.58–0.62** on this baseline (exact value depends on data split and run; e.g. [experiment_comparison.json](../metrics/experiment_comparison.json) shows **~0.617**).
2. In `params.yaml`, set `gates.fairness.max_equalized_odds_difference` from **0.70** to **0.55** (stricter).
3. Run:

```powershell
cd C:\Users\Chau_\Projects\eu-ai-act-gac-credit
.\.venv\Scripts\python.exe src\train.py
.\.venv\Scripts\python.exe src\gate_fairness.py
```

4. **Expected:** `gate_passed: false`, non-zero exit code — the **governed** path **blocks** the same model class that previously passed under looser policy.

5. **Thesis:** Table “policy v1 vs v2” + one paragraph on **GaC** = **executable** compliance thresholds.

6. **Revert** `max_equalized_odds_difference` to **0.70** for your default baseline runs.

## Optional: stress modes (`STRESS_BIAS`)

See [stress_experiment.md](stress_experiment.md). Use **`STRESS_MODE=remove_rare`** for a **biased training** narrative; if EOD does not move enough for your story, prefer the **threshold** demo above.
