# Thesis figures (exports)

Store **thesis-bound** visuals here so they stay next to the narrative docs. **Do not** commit large binary churn without need—your faculty may prefer figures only in Word; this folder is the **working** location for drafts and PNG/PDF exports.

## Naming

`Fig01_gac_architecture.png`, `Fig02_pipeline_flow.png`, … matching [THESIS_WRITING_HUB.md](../THESIS_WRITING_HUB.md) §5.

## Suggested exports

| Asset | How |
|-------|-----|
| Architecture | draw.io, PowerPoint, or Mermaid → PNG/PDF |
| MLflow | Screenshot of run with `git_commit`, `params_yaml_sha16` tags |
| GitHub Actions | Screenshot of successful matrix workflow run |
| SHAP | Render from `artifacts/shap_report.md` or notebook |

## Git

Add patterns to `.gitignore` only if binaries become noisy, e.g. `*.pptx` — otherwise keep small PNGs for reproducibility.
