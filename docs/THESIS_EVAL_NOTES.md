# Thesis evaluation — ready-made points

**Start here:** [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) — RQs, DSR map, scope, and evidence chain.

Use with your supervisor’s style guide; cite primary sources for the EU AI Act.

## Limitations (methods)

- **Gate C latency** is measured in **GitHub Actions** (wall-clock from end of automated gates until the approval job starts; **includes** Environment approval wait when reviewers are configured — see [human_oversight.md](human_oversight.md)). It is a **CI proxy**, not production banking workflow latency.
- **Fairness threshold** `max_equalized_odds_difference: 0.70` is set so the **baseline** logistic model passes; report sensitivity when you tighten it or add mitigation (Fairlearn reductions, etc.).
- **`famges`** is a **proxy** for personal status / sex (UCI description); discuss proxy risk and Article 9 / GDPR where relevant.

## DSR artifacts to reference

| Artifact | Role |
|----------|------|
| `metrics/experiment_comparison.json` | Standard vs governed (same seed) |
| `metrics/fairness_gate.json` | Gate A outcome |
| `metrics/shap_gate.json` | Gate B outcome |
| `metrics/human_oversight_latency.json` | Gate C — **sample:** 7 s (`human_oversight_latency_seconds`), run `24081106560` |
| MLflow runs | `pipeline_profile`, `data_provenance` |
| `dvc.lock` + git commit | Reproducible pipeline state |

## Standard vs governed (P3)

Run locally:

```bash
python scripts/compare_profiles.py
```

Paste the table from `metrics/experiment_comparison.json` into the thesis and discuss **wall_time_seconds** vs **gate outcomes**.

**Which file to cite:** Use **`experiment_comparison.json`** for the **standard vs governed** side-by-side (it records `git_commit` at generation time). **`train_metrics.json`** on disk is only the **last** `train.py` run and may not match that comparison if you trained again without re-running `compare_profiles.py` — see [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §8.
