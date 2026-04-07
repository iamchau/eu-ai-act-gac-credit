# Gate C — Human oversight (GitHub Actions)

This implements **Art. 14-style** “human in the loop” as an **executable gate**: deployment (or “release”) does not proceed until a **protected GitHub Environment** is approved.

## Workflows

| Workflow | Purpose |
|----------|---------|
| [`ci.yml`](../.github/workflows/ci.yml) | Matrix **standard** (train only) vs **governed** (train + fairness + SHAP). |
| [`governed_deploy.yml`](../.github/workflows/governed_deploy.yml) | **Manual** run: automated gates → **wait** on Environment **`model-governance`** → write **`metrics/human_oversight_latency.json`**. |

## Configure the Environment (required for real oversight)

1. Repo **Settings** → **Environments** → **New environment** → name: **`model-governance`**.  
2. Enable **Required reviewers** and add at least one account (you or a supervisor test account).  
3. Save.

Until reviewers are set, the second job may still run immediately; the thesis should report whether protection was enabled.

## Measuring latency (Sub-RQ2)

`human_oversight_latency.json` contains:

- **`human_oversight_latency_seconds`** — wall-clock seconds from **end of automated gates** (`gates_completed_epoch`) until the **approval job starts** (`approval_epoch`). This includes queue time and the time waiting for a human to approve the Environment.

**Limitation:** This is a **CI proxy** for “approval latency,” not bank-grade signing. Discuss in methods / limitations.

## Local development

Gate C is **CI-native**. Locally, run `dvc repro` for Gates A–B only; record human-oversight latency from a **workflow run** after pushing to GitHub.
