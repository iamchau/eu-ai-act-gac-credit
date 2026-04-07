# Gate C runbook — governed-deploy, approval, artifact

Use this if **Actions → Run workflow** or **approval / download** did not work.

## Direct links (replace if your repo URL differs)

- **All workflows:** [Actions tab](https://github.com/iamchau/eu-ai-act-gac-credit/actions)
- **This workflow only:** [governed_deploy.yml](https://github.com/iamchau/eu-ai-act-gac-credit/actions/workflows/governed_deploy.yml)

## A. Enable Actions (if the Actions tab is empty or disabled)

1. Repo **Settings** → **Actions** → **General**.
2. Under **Actions permissions**, choose **Allow all actions and reusable workflows** (or your org’s equivalent).
3. Save.

## B. Run the workflow manually

1. Open the **governed_deploy** workflow page (link above).
2. On the **right**, you should see **Run workflow** (dropdown).
3. Branch: **`main`** → green **Run workflow**.

If **Run workflow** is missing:

- The workflow file must exist on the **default branch** (`main`). Confirm: [`.github/workflows/governed_deploy.yml`](https://github.com/iamchau/eu-ai-act-gac-credit/blob/main/.github/workflows/governed_deploy.yml) on GitHub.
- Some organization accounts restrict who can run workflows; try as **repo owner** or ask an admin.

## C. Environment `model-governance` must allow `main`

If the second job never starts or stays “Pending”:

1. Repo **Settings** → **Environments** → **`model-governance`**.
2. **Deployment branches** — set to **All branches** *or* explicitly allow **`main`** (not only `production` / protected names).
3. **Required reviewers** — optional; if listed, only those users can approve.

## D. Where to click “Approve”

1. Open the **workflow run** (click the latest run under **governed-deploy**).
2. You should see two jobs: **`build-and-gates`** then **`human-approval-release`**.
3. If the second waits for you:
   - In the run page, look for **“Review deployments”** / **“Waiting for approval”** (yellow / pending).
   - Or **Settings** → **Environments** → **`model-governance`** → pending deployment reviews.
4. Approve so **`human-approval-release`** runs.

If there are **no** reviewers configured, the second job often runs **without** a button (latency will be small).

## E. Download `human_oversight_latency.json`

1. After the run finishes (green), scroll to the bottom of the run page.
2. Section **Artifacts**.
3. Download **`human-oversight-latency-<run_id>`** (ZIP).
4. Unzip → **`metrics/human_oversight_latency.json`** — keep this for Sub-RQ2.

If **Artifacts** is empty:

- Open the **`human-approval-release`** job log — check for errors.
- Confirm the step **Upload latency metric** ran.

## F. Still stuck?

- Paste the **failing job log** (or a screenshot of the run page) into your thesis notes or ask your supervisor — the log text is enough to debug.
- As a **fallback for the thesis**, you can still report **local** wall-clock from `scripts/compare_profiles.py` (standard vs governed) and state that **Gate C latency** was collected from CI once the workflow runs successfully.
