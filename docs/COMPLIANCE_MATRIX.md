# Compliance matrix — EU AI Act ↔ GaC implementation

**Purpose:** One-page audit trail: legal expectation → engineering control → metric → artifact.  
**Rule:** Cite **EUR-Lex** or official consolidated text for examiners; this table is a **thesis map**, not legal advice.


| Theme (Act)                                                     | Your control (repo)                                                            | Metric / evidence                                   | Artifact / path                                          |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------- | -------------------------------------------------------- |
| Data governance (Art. 10)                                       | Fixed seed, UCI data, `data_provenance` in MLflow                              | Same splits via `seed`; source documented           | `docs/DATA_PROVENANCE.md`, MLflow tags                   |
| Transparency / info to deployers (Art. 13)                      | SHAP gate, logged model                                                        | Top features, mean |SHAP|                           | `artifacts/shap_report.md`, `metrics/shap_gate.json`     |
| Human oversight (Art. 14)                                       | GitHub Environment `model-governance`, `governed_deploy`                       | `human_oversight_latency_seconds`                   | `metrics/human_oversight_latency.json`, workflow run URL |
| Fairness / discrimination risk (Annex III + Art. 10–11 context) | Fairlearn EOD gate on `famges` (proxy)                                         | `equalized_odds_difference` vs threshold            | `metrics/fairness_gate.json`, `src/gate_fairness.py`     |
| Traceability / logging                                          | MLflow + git/DVC digests on each run                                           | `git_commit`, `params_yaml_sha16`, `dvc_lock_sha16` | MLflow tags, `metrics/train_metrics.json`                |
| **Stress (research)**                                           | Optional `stress` / `STRESS_BIAS` undersamples minority sensitive in **train** | EOD on **unchanged val** worsens; gate may **fail** | Same gates; document in `docs/stress_experiment.md`      |


**Dr. Voss note:** Replace row citations with your faculty’s preferred Article numbering once the final consolidated text for your submission year is fixed.