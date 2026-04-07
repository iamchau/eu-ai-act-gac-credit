# GitHub: remote, CI, and Gate C

## 1. Repo and remote (done if you followed the push)

**Repo:** [iamchau/eu-ai-act-gac-credit](https://github.com/iamchau/eu-ai-act-gac-credit)

Local (already applied in this project):

```bash
git remote add origin https://github.com/iamchau/eu-ai-act-gac-credit.git
git branch -M main
git push -u origin main
```

## 2. Environment for Gate C

**Settings** → **Environments** → **New environment** → name: `**model-governance`**.

- Enable **Required reviewers** and add at least one reviewer (yourself is fine for a pilot).

Without reviewers, the approval job may still run immediately; latency is smaller but still recorded.

**Important:** Under **Deployment branches**, allow `**main`** (or “All branches”). If only `production` is allowed, the `human-approval-release` job will not run on `main`.

## 3. Run governed deploy (latency sample)

**Actions** → **governed-deploy** → **Run workflow** → approve the Environment when prompted.

Download artifacts:

- `**human-oversight-latency-<run_id>`** (ZIP) → contains `metrics/human_oversight_latency.json`.

Keep that JSON for Sub-RQ2 in the thesis.

**If Run workflow, approval, or download fails:** see **[GATE_C_RUNBOOK.md](GATE_C_RUNBOOK.md)** (direct links, branch rules, troubleshooting).

## 4. CI matrix

Every push/PR runs **standard** and **governed** jobs (see `.github/workflows/ci.yml`). Use run URLs and job durations from the Actions UI for the “velocity / overhead” discussion.

## 5. Optional: GitHub CLI

If you install the [GitHub CLI](https://cli.github.com/), you can trigger workflows from the terminal after `gh auth login`:

```bash
gh workflow run governed-deploy.yml
```

