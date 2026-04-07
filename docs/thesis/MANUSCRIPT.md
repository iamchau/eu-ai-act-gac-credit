---

## title: "Implementing the EU AI Act: A Design Science Study on Governance-as-Code (GaC) for High-Risk Credit Scoring in Norway"

author: "[Author Name]"
date: "[Submission year]"

**Institution:** [University / Faculty]  
**Programme:** [Degree programme]  
**Supervisor:** [Name]  
**Repository:** `https://github.com/iamchau/eu-ai-act-gac-credit` (reference implementation)

*Draft manuscript — replace bracketed fields; expand literature where your programme requires; cite EUR-Lex for all Article quotations in the final PDF.*

---

# Abstract

The EU Artificial Intelligence Act (Regulation (EU) 2024/1689) imposes obligations on providers of high-risk AI systems, including credit scoring that evaluates natural persons. Translating legal and policy expectations into day-to-day machine learning operations remains challenging: performance-driven MLOps pipelines rarely encode fairness, explainability, and human oversight as **blocking** controls in continuous integration.

This thesis adopts **Design Science Research** (Hevner *et al.*) and instantiates **Governance-as-Code (GaC)**: selected Act-related expectations are mapped to executable **gates** (fairness, SHAP explainability, human approval before a release-style job) in a reproducible Python repository with MLflow, DVC, and GitHub Actions. The **standard** profile optimises predictive performance only; the **governed** profile adds automated checks. Using the public UCI South German Credit (UPDATE) dataset—not Norwegian bank data—the study compares both profiles under a fixed random seed and demonstrates that **stricter fairness policy** can cause the governed path to **block** when equalized-odds difference exceeds a tightened threshold. A second measurement records **human-oversight latency** in a GitHub Actions proxy (seconds from completion of automated gates to the start of an approval job, including Environment approval wait when configured).

The thesis does **not** claim full legal compliance or industry adoption. Contributions are: (1) a **GaC construct** and **reference instantiation**; (2) **controlled evaluation** evidence for Sub-RQ1 and Sub-RQ2; (3) **design principles** for regulated ML pipelines. Limitations include proxy sensitive attributes, CI-only oversight latency, and illustrative deployment.

**Keywords:** EU AI Act; governance-as-code; high-risk AI; credit scoring; MLOps; fairness; explainability; human oversight; design science research; Norway

---

# Table of contents

1. [Introduction](#1-introduction)
2. [Background and literature](#2-background-and-literature)
3. [Theoretical framework](#3-theoretical-framework)
4. [Methodology](#4-methodology)
5. [Instantiation](#5-instantiation)
6. [Results](#6-results)
7. [Discussion](#7-discussion)
8. [Conclusion](#8-conclusion)
9. [References](#9-references)
10. [Appendices](#10-appendices)

---

# 1. Introduction

## 1.1 Problem and motivation

Credit scoring systems that evaluate natural persons are listed among **high-risk** AI use cases in Annex III of Regulation (EU) 2024/1689 (*European Parliament and Council of the European Union*, 2024). Providers must meet requirements spanning data governance, transparency, fairness, logging, and human oversight—depending on the system’s role and risk management process. In parallel, machine learning practice has converged on **MLOps**: versioned data, automated training, and CI/CD for software-like release of models.

A persistent gap is **operational**: legal and policy language does not automatically appear as **tests** that fail a build when a model violates an internal fairness budget or lacks an explainability artifact. **Governance-as-Code (GaC)** treats governance expectations as **code**: policies expressed as thresholds, scripts, and pipeline stages that can block progression when violated.

## 1.2 Norwegian context (scope)

Norway, as part of the European Economic Area, participates in the **single market** alignment with EU product rules; AI system obligations must be read together with national financial supervision and consumer protection. This thesis uses **Norway** as **jurisdictional and pedagogical context** for high-risk credit scoring. It does **not** use proprietary Norwegian credit data or conduct an industry case study. The empirical work uses a **public** German credit dataset (Section 4.2) with explicit scope limits.

## 1.3 Research questions

The **primary research question** is:

> *How can Governance-as-Code be designed and instantiated as a MLOps pipeline for high-risk credit scoring that maps selected EU AI Act obligations to executable fairness, explainability, and human-oversight controls in CI/CD—without claiming that the Act is fully automated or fully implemented in code?*

**Sub-RQ1** addresses policy effectiveness under controlled conditions:

> *Under controlled comparison (same seed, same data lineage), does the governed profile (fairness + SHAP gates) differ from the standard profile—and can stricter policy or stress demonstrate that the governed path blocks when operational non-compliance is detected?*

**Non-compliance** is **operational**, not legal: failure of the fairness gate (Fairlearn equalized odds difference above threshold) and/or the SHAP sanity gate when enabled.

**Sub-RQ2** addresses human-in-the-loop delay in the **CI proxy**:

> *What automation-to-approval latency does a human gate add in the GitHub Actions instantiation—measured as seconds from end of automated gates to start of the approval job—and not as end-to-end credit decision or legal signing time?*

The metric **includes** waiting for GitHub Environment approval when reviewers are configured; it does **not** measure core banking systems or qualified electronic signatures.

Table 1 summarises operational terms for the primary RQ (see also Chapter 4).

**Table 1 — Operational terms for the primary RQ**


| Phrase                 | Meaning in this thesis                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------- |
| Design                 | Construct (GaC pipeline) + instantiation (repository) + design principles (Chapter 7).  |
| Automatically enforces | Executable checks: failed gates block or record failure—not full automation of law.     |
| EU AI Act requirements | Mapped to engineering controls (Chapter 5, Appendix B); legal completeness not claimed. |
| CI/CD pipeline         | GitHub Actions + local DVC; deployment is illustrative, not a production bank stack.    |


## 1.4 Contributions

1. **Artifact:** A reference **GaC MLOps** repository with Gates A (fairness), B (SHAP), C (human approval), experiment tracking, and reproducibility digests.
2. **Evaluation:** Controlled **standard vs governed** comparison and a **policy tightening** demonstration with archived gate failure JSON; **Sub-RQ2** latency from a documented workflow run.
3. **Principles:** Discussion of trade-offs (velocity vs control) and boundaries of CI-based oversight.

## 1.5 Structure of the thesis

Chapter 2 reviews responsible AI, MLOps, and the EU AI Act high-risk framing. Chapter 3 presents Design Science Research and GaC. Chapter 4 describes methodology, data, and limitations. Chapter 5 describes the instantiation. Chapter 6 reports results. Chapters 7–8 discuss and conclude. References and appendices follow.

---

# 2. Background and literature

## 2.1 Responsible AI and algorithmic fairness

Fairness in classification is operationalised through **group** and **individual** notions. This thesis uses **equalized odds** (Fairlearn) on validation predictions relative to a **sensitive attribute** column. The UCI dataset exposes a combined demographic proxy (`famges`); interpretation limits are discussed in Section 4.5.

## 2.2 MLOps and compliance

MLOps emphasises reproducibility, monitoring, and automation. **Governance-as-Code** extends that idea by encoding policy as **pipeline gates**—a theme aligned with software supply-chain and policy-as-code literature [expand with your supervisor’s required citations].

## 2.3 EU AI Act and high-risk credit scoring

Regulation (EU) 2024/1689 establishes harmonised rules for AI systems placed on the EU market or put into service. High-risk systems must comply with **Title III, Chapter 2** requirements (e.g. risk management, data governance, transparency, human oversight, accuracy, robustness, cybersecurity)—**cite the official consolidated text from EUR-Lex** for precise Article duties in your final PDF; Appendix B is a **scaffold**, not a substitute for legal analysis.

## 2.4 Gap addressed

The gap addressed is **operational**: bridging high-level obligations and **executable** ML pipeline controls. This thesis contributes an **instantiation** and **measures**, not a legal compliance certificate.

---

# 3. Theoretical framework

## 3.1 Design Science Research (Hevner *et al.*)

Design Science Research produces **artifacts** (constructs, models, methods, instantiations) that solve relevant problems and are evaluated rigorously. Cycles include **relevance** (problem in context), **rigor** (methods and knowledge base), and **design** (build and evaluate). This thesis maps to: **relevance**—EU high-risk credit and MLOps practice; **rigor**—Fairlearn, SHAP, reproducible splits, committed metrics; **design**—GaC pipeline and evaluation.

## 3.2 Governance-as-Code

GaC is defined here as: **mapping** selected governance expectations to **versioned** checks in the training and release path, such that violations are **observable** and can **block** downstream stages. It is complementary to organisational process; it does not replace legal review.

---

# 4. Methodology

## 4.1 Research design

The study follows a **DSR** path: build the instantiation, compare **standard** vs **governed** profiles under fixed controls, and demonstrate **blocking** under tightened policy. **Sub-RQ2** uses a **single** illustrative GitHub Actions workflow run with archived latency JSON.

## 4.2 Data

**Primary source:** UCI Machine Learning Repository, **South German Credit (UPDATE)** (`SouthGermanCredit.asc`), dataset ID 573. **Provenance** string logged to MLflow: `uci-asc:SouthGermanCredit.asc`. If local raw files are missing, the training script may fall back to OpenML `credit-g`; the thesis reports the provenance recorded for the runs cited here.

**Binding for Chapter 6 (P3):** Tables and metrics for the **standard vs governed** comparison **must** match `**metrics/experiment_comparison.json`**—including its `**git_commit**`, `**data_provenance**`, and embedded metrics. For the committed file cited in Section 6.1, lineage is `**uci-asc:SouthGermanCredit.asc**` (aligned with CI and `scripts/compare_profiles.py`). A different local raw path does not override the cited JSON unless you regenerate and recommit that file.

**Split:** 75% train / 25% validation, `random_state=42`, stratified on the target. **Sensitive column** for fairness: `famges` (fallback `personal_status` if absent).

## 4.3 Profiles

- **Standard:** `PIPELINE_PROFILE=standard` — train only; performance metrics; **no** fairness or SHAP gates in the comparison script path.  
- **Governed:** `PIPELINE_PROFILE=governed` — train, then fairness gate, then SHAP gate.

**Note:** Local `dvc repro` runs all stages after train using `pipeline.profile` from `params.yaml` (default governed); the **standard** baseline for P3 uses the comparison script, not `dvc repro` alone (see project `docs/compare_pipelines.md`).

## 4.4 Gate roles and evidence binding

For **Sub-RQ1**, the **fairness** gate (Gate A) carries the **demonstrated blocking** story: the archived threshold-tightening run (`metrics/fairness_gate_subrq1_threshold_demo_fail.json`) records `**gate_passed: false`** when the fairness budget is tighter than the observed equalized-odds difference on the validation split.

The **SHAP** gate (Gate B) **mandates** an explainability artefact (`artifacts/shap_report.md`) and metrics (`metrics/shap_gate.json`). With the baseline `**min_top_mean_abs_shap: 0.0`** in `params.yaml`, Gate B **documents** SHAP-based attribution for the validation set and **passes** under normal runs; it does **not** provide a second independent numeric failure mode in this baseline configuration (raising `min_top_mean_abs_shap` would be required to make SHAP-driven failure likely). Optional **stress** / bias-injection runs target **fairness** outcomes; see `docs/stress_experiment.md`.

**Evidence binding:** Claims in Chapter 6 that rest on the profile comparison **must** align with `**metrics/experiment_comparison.json`** (Sections 4.2 and 4.4). On-disk `metrics/fairness_gate.json` from a **later** local run may differ; the **thesis table** is tied to the embedded objects inside `experiment_comparison.json` unless you state otherwise.

## 4.5 Ethics and limitations (methods)

- **Data:** Public anonymised records; **proxy** sensitive attributes—no claim of representing protected characteristics directly.  
- **Legal:** Appendix B maps themes to controls; **thesis must cite EUR-Lex** for Articles.  
- **Sub-RQ1:** Controlled comparison + blocking demo—not sampled production approval rates.  
- **Sub-RQ2:** CI proxy; latency includes GitHub Environment approval wait when enabled—not bank SLA or eID signing.  
- **Deployment:** Research instantiation; “release” is illustrative.

---

# 5. Instantiation

## 5.1 Stack

- **Python 3.12** (CI); scikit-learn logistic regression; **MLflow** tracking (`sqlite:///./mlflow.db`); **DVC** for pipeline stages; **Fairlearn** (equalized odds difference); **SHAP** (mean |SHAP| on validation).  
- **CI:** `.github/workflows/ci.yml` matrix **standard** vs **governed**.  
- **Gate C:** `.github/workflows/governed_deploy.yml`; Environment `**model-governance`**; latency written to `metrics/human_oversight_latency.json`.

## 5.2 Gates


| Gate              | Script                       | Pass criterion (baseline)                                                               |
| ----------------- | ---------------------------- | --------------------------------------------------------------------------------------- |
| A Fairness        | `src/gate_fairness.py`       | `abs(equalized_odds_difference) ≤ max_equalized_odds_difference` (default **0.70**)     |
| B SHAP            | `src/gate_shap.py`           | Top feature mean |SHAP| ≥ `min_top_mean_abs_shap` (**0.0** — artefact + pass; see §4.4) |
| C Human oversight | GitHub Actions + Environment | Manual approval before second job; latency JSON                                         |


Gate **A** is the primary **policy-as-code** lever for **blocking** demonstrations in this thesis (threshold demo; optional stress). Gate **B** enforces **presence** of a SHAP summary under the baseline threshold; Chapter 4.4 states how this relates to Sub-RQ1 evidence.

**Figure 1 (placeholder):** High-level architecture — standard vs governed paths and Gate A/B/C.

## 5.3 Traceability

Each training run logs **git commit** (short), **params.yaml** SHA-16, and **dvc.lock** SHA-16 to MLflow tags and `metrics/train_metrics.json`, supporting audit-style replay.

## 5.4 MLOps scoring API (illustrative)

The repository **includes** a **containerised** FastAPI service (`serving/`, Docker) exposing **`/health`** (liveness), **`/ready`** (readiness), **`/version`**, **`/metrics`** (minimal process stats), and **`/predict`** for the **same** sklearn pipeline as offline training; training also emits **`artifacts/feature_schema.json`** for a documented inference column contract. Continuous integration **builds** a Docker image after training, uploads a **tarball** artefact for every run, and **on `push` and `workflow_dispatch`** (not **`pull_request`**) also pushes the image to **GitHub Container Registry (GHCR)**—still **not** a production release or bank-grade operation. Optional controls (**API key** on predict, **request body limit**, **per-IP rate limit**, **structured access logs**) are **illustrative** operations hygiene—not bank security or compliance tooling. This supports **Primary RQ** “instantiation” and **Discussion** (traceable deployment-shaped artefact) but is **not** claimed as regulated production deployment: no service-level guarantees, no integration with core banking systems, and the model artefact remains **research-grade** on public data. Sub-RQ1 and Sub-RQ2 evidence remain tied to committed metrics and CI unless extended by explicit new experiments.

---

# 6. Results

## 6.1 Standard vs governed (Sub-RQ1, controlled comparison)

Table 2 summarises `metrics/experiment_comparison.json` generated at **2026-04-07T13:21:17Z** (repository commit embedded in file: `456289c57a504a2b532d5edbb601a04fd2e953e3`).

**Table 2 — Standard vs governed profiles (same seed, same lineage)**


| Metric        | Standard | Governed                      |
| ------------- | -------- | ----------------------------- |
| Exit code     | 0        | 0                             |
| Wall time (s) | 6.726    | 20.912                        |
| Accuracy      | 0.776    | 0.776                         |
| ROC-AUC       | 0.796    | 0.796                         |
| Fairness gate | not run  | pass (EOD 0.617, max 0.70)    |
| SHAP gate     | not run  | pass (top feature `laufkont`) |


Under the **baseline** threshold (**0.70**), both profiles achieve identical accuracy and ROC-AUC; the governed path adds **gate latency** (wall time) and **policy enforcement** without changing point predictions for this split.

## 6.2 Policy tightening — gate blocks (Sub-RQ1 demonstration)

When `max_equalized_odds_difference` was tightened from **0.70** to **0.55**, the same model class produced **abs EOD ≈ 0.617**, exceeding **0.55**. The fairness gate **failed** (`gate_passed: false`). The archived metric file is `metrics/fairness_gate_subrq1_threshold_demo_fail.json`. The threshold was **reverted** to **0.70** for the baseline narrative.

**Table 3 — Fairness gate: baseline vs tightened policy**


| Setting         | max EOD allowed | abs EOD (val) | gate_passed |
| --------------- | --------------- | ------------- | ----------- |
| Baseline        | 0.70            | 0.617         | true        |
| Demo (archived) | 0.55            | 0.617         | **false**   |


This demonstrates **executable** policy: **identical** code and data, **stricter** threshold, **blocked** governed path.

## 6.3 Human-oversight latency (Sub-RQ2)

From `metrics/human_oversight_latency.json` (workflow sample):

- `**human_oversight_latency_seconds`:** 7  
- **Workflow run:** `https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560`

This measures **GitHub-mediated** delay (gates complete → approval job start), including Environment approval wait when protection is enabled—not end-to-end bank processing.

---

# 7. Discussion

## 7.1 Answers to research questions

**Primary RQ.** The thesis **designed and instantiated** a GaC pipeline mapping selected obligations to **fairness**, **SHAP**, and **human approval** controls. **Enforcement** is operational (gates block or fail the stage); the work does **not** claim full Act implementation in code.

**Sub-RQ1.** Under controlled comparison, **standard** and **governed** coincide on accuracy for this baseline; the governed path adds **checks** and **cost** (time). The **threshold demo** shows the governed path **blocks** when policy tightens—evidence for **policy-as-code** beyond hand-waving.

**Sub-RQ2.** The recorded **7 s** latency is an **illustrative** CI sample (**n = 1** run cited); it supports discussion of **human gate overhead** in automation, not banking production SLAs.

## 7.2 Design principles

1. **Separation of profiles** — standard vs governed must be **defined** and reproducible.
2. **Evidence binding** — claims attach to JSON, workflows, and commit hashes.
3. **Honest scope** — proxy attributes, CI-only oversight, illustrative deployment.

## 7.3 Limitations

See Section 4.5 and Chapter 1. In short: **dataset** limits generalisation; **legal** claims require EUR-Lex and supervision; **Sub-RQ2** is a **narrow** operational metric.

## 7.4 Future work

Mitigation algorithms (e.g. Fairlearn reductions), additional datasets, organisational study of GaC adoption, and national transposition details for Norway where required by the programme.

---

# 8. Conclusion

This thesis presented a **Governance-as-Code** MLOps **instantiation** for high-risk credit scoring under the EU AI Act **framing**, with **fairness**, **explainability**, and **human oversight** gates in CI/CD. **Controlled** evaluation and a **policy tightening** demonstration support Sub-RQ1; **Sub-RQ2** reports **GitHub Actions** latency for a **functional analogue** of human oversight before release. Contributions are the **artifact**, **evidence**, and **principles**—not a claim that a single repository **satisfies** the Regulation as a legal matter.

---

# 9. References

*Replace with your faculty’s citation style (APA, Harvard, OSCOLA, etc.). The Regulation must be cited from the official consolidated text.*

European Parliament and Council of the European Union. (2024). Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence and amending Regulations … *Official Journal of the European Union*. Retrieved from EUR-Lex: `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689`

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, 28(1), 75–105.

[Add: Fairlearn, SHAP, UCI dataset, MLOps, RAI surveys as required by your programme.]

---

# 10. Appendices

## Appendix A — Parameters excerpt (`params.yaml`)

Relevant keys: `seed: 42`; `pipeline.profile`; `gates.fairness.max_equalized_odds_difference: 0.70` (baseline); `gates.fairness.sensitive_column: famges`; `mlflow.tracking_uri: sqlite:///./mlflow.db`. Full file in repository root.

## Appendix B — Compliance matrix (scaffold)

Use `docs/COMPLIANCE_MATRIX.md` in the repository; **replace** Article citations with your **EUR-Lex** references in the final thesis.

## Appendix C — Metric excerpts

**C.1** `experiment_comparison.json` — see `metrics/experiment_comparison.json` at commit cited in Chapter 6.

**C.2** `fairness_gate_subrq1_threshold_demo_fail.json`:

```json
{
  "equalized_odds_difference": 0.6169354838709677,
  "abs_equalized_odds_difference": 0.6169354838709677,
  "max_allowed": 0.55,
  "gate_passed": false
}
```

**C.3** `human_oversight_latency.json` (sample run):

```json
{
  "human_oversight_latency_seconds": 7,
  "workflow_run_url": "https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560"
}
```

## Appendix D — Reproducibility

Regenerate P3 comparison: `python scripts/compare_profiles.py` from repository root with the same `params.yaml` and data files.

---

*End of manuscript draft.*