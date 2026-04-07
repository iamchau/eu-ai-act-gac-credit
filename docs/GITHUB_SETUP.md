# GitHub: remote, CI, and Gate C

Do these once so **CI runs on push** and you can collect **`human_oversight_latency.json`**.

## 1. Create the repo and add `origin`

On GitHub: **New repository** (empty, no README). Then locally:

```bash
cd /path/to/eu-ai-act-gac-credit
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin master
```

(Use `main` instead of `master` if that is your default branch.)

## 2. Environment for Gate C

**Settings** → **Environments** → **New environment** → name: **`model-governance`**.

- Enable **Required reviewers** and add at least one reviewer (yourself is fine for a pilot).

## 3. Run governed deploy (latency sample)

**Actions** → **governed-deploy** → **Run workflow** → approve the Environment when prompted.

Download artifacts:

- **`human-oversight-latency-<run_id>`** → contains `metrics/human_oversight_latency.json`.

Keep that JSON for Sub-RQ2 in the thesis.

## 4. CI matrix

Every push/PR runs **standard** and **governed** jobs (see `.github/workflows/ci.yml`). Use run URLs and job durations from the Actions UI for the “velocity / overhead” discussion.
