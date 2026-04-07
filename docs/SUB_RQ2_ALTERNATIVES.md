# Sub-RQ2 — alternative formulations (Dr. Voss)

The **default** thesis design uses **Sub-RQ2 = CI orchestration latency** (`human_oversight_latency.json`). That is **measurable** and **honest**, but **narrow**. If your supervisor wants Sub-RQ2 to stress **traceability** or **human oversight design** instead (or in addition), use **one** of the alternatives below—**do not** stack multiple Sub-RQ2s without faculty approval.

**Repository default:** Latency-focused Sub-RQ2 (aligned with Gate C and [human_oversight.md](human_oversight.md)).

---

## A — Default (keep): automation-to-approval latency

**Thesis-ready one-liner:**  
*What **automation-to-approval** latency does a human gate add in the **GitHub Actions** instantiation—measured as seconds from **end of automated gates** to **start** of the approval job—and **not** as end-to-end credit decision or legal signing time?*

| Pros | Cons |
|------|------|
| Crisp metric; matches `metrics/human_oversight_latency.json` + workflow URL | Easy to **misread** as “banking latency” without scope text |

**Evidence:** `human_oversight_latency.json` + run URL; state **n**.

---

## B — Traceability / audit trail

**Thesis-ready one-liner:**  
*To what extent does the GaC instantiation produce **reproducible, inspectable** evidence for fairness and explainability decisions (experiment tracking, data lineage, gate outputs, configuration digests)—as an operational analogue to documentation and record-keeping expectations under the EU AI Act framework?*

| Pros | Cons |
|------|------|
| Aligns with MLflow, DVC, `run_context` digests, gate JSON | More **descriptive**; you need **evaluation criteria** (e.g. checklist: what must exist for an audit replay—not just “we logged it”) |

**Evidence (examples):** MLflow tags (`git_commit`, `params_yaml_sha16`, `dvc_lock_sha16`); `dvc.lock`; `metrics/fairness_gate.json`, `metrics/shap_gate.json`; `artifacts/shap_report.md`; CI run logs.

**If you switch to B:** Either **drop** latency as a formal Sub-RQ (move to Results as supporting) **or** combine in one Sub-RQ2 with **two** explicit parts (latency + traceability)—get supervisor approval; avoid scope creep.

---

## C — Human oversight as technical control

**Thesis-ready one-liner:**  
*How is **human oversight before release** realized as a **technical control** in CI/CD (protected environment, required reviewers), and what are the **boundary conditions** relative to production banking workflows and qualified electronic signatures?*

| Pros | Cons |
|------|------|
| Direct **design** narrative; fits Art. 14 **analogue** without legal conclusion | Less **quantitative**; latency becomes **illustrative** |

**Evidence:** Workflow design ([governed_deploy.yml](../.github/workflows/governed_deploy.yml)); [GITHUB_SETUP.md](GITHUB_SETUP.md); one latency number as **example**; explicit limitation paragraph.

---

## D — Engineering trade-offs (velocity vs governance)

**Thesis-ready one-liner:**  
*What **engineering trade-offs** emerge between a **standard** (performance-only) path and a **governed** path with automated gates and a human approval step—in **this** instantiation (e.g. CI duration, gate failures, orchestration delay)?*

| Pros | Cons |
|------|------|
| Unifies Sub-RQ1 “difference” with operational **cost** | Risk of **vague** prose unless every trade-off is **operationalized** (table: metric, standard, governed) |

**Evidence:** `experiment_comparison.json`; CI matrix run times if recorded; `human_oversight_latency.json`; optional gate-failure counts from documented runs.

---

## Recommendation (Dr. Voss)

- **Default thesis:** Keep **A** unless faculty pushes toward **B** or **C**.  
- **B** is strong if examiners want **Act alignment** beyond stopwatch metrics—budget **extra** methodology text for **criteria**.  
- **Do not** silently swap Sub-RQ2 in the Introduction without updating **§1 core claim**, **Results**, and **evidence index** in [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md).
