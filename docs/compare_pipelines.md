# Standard vs governed pipelines (thesis experiment)

| Profile | Command (local) | CI job (`ci.yml`) |
|--------|-------------------|-------------------|
| **Standard** | `PIPELINE_PROFILE=standard` … `python src/train.py` or set `pipeline.profile: standard` in `params.yaml` | `matrix.profile == standard` — **train only** |
| **Governed** | `dvc repro` (train + fairness + SHAP) | `matrix.profile == governed` — train + gates |

**MLflow** logs `pipeline_profile` on each run.

**Thesis use:** Compare **velocity** (time to green CI / number of steps) and **outcomes** (metrics + gate pass/fail) between profiles on the **same data split** (fixed `seed` in `params.yaml`).
