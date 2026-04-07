# Standard vs governed pipelines (thesis experiment)

| Profile | Command (local) | CI job (`ci.yml`) |
|--------|-------------------|-------------------|
| **Standard** | `PIPELINE_PROFILE=standard` … `python src/train.py` or set `pipeline.profile: standard` in `params.yaml` | `matrix.profile == standard` — **train only** |
| **Governed** | `dvc repro` (train + fairness + SHAP) **or** `PIPELINE_PROFILE=governed` + `python src/train.py` then gate scripts | `matrix.profile == governed` — train + gates |

**DVC note:** `dvc repro` does **not** set `PIPELINE_PROFILE`; the train stage uses `pipeline.profile` from `params.yaml` (default **governed**). It always runs fairness + SHAP after train. A **standard** baseline is **not** produced by `dvc repro` alone — use `PIPELINE_PROFILE=standard` and **train only** (as in CI **standard** and `scripts/compare_profiles.py`).

**MLflow** logs `pipeline_profile` on each run.

**Thesis use:** Compare **velocity** (time to green CI / number of steps) and **outcomes** (metrics + gate pass/fail) between profiles on the **same data split** (fixed `seed` in `params.yaml`).
