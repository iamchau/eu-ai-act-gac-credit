# Thesis draft snippets — paste-ready (Dr. Voss improvements)

Use these **verbatim or lightly adapted** in Word/LaTeX. They align with [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) and [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md). Replace bracketed placeholders with your faculty’s wording and your **final** numbers after runs.

---

## 1. Introduction — positioning paragraph

*Place after problem statement; before RQs.*

The gap addressed in this thesis is not merely abstract “ethics in AI,” but the **operational** distance between **high-risk** credit-scoring obligations under the EU regulatory framework for artificial intelligence (Regulation (EU) 2024/1689) and **day-to-day** machine-learning operations—versioning, testing, and release. **Governance-as-Code (GaC)** is treated here as a **design construct**: selected obligations are **mapped** to executable checks and traceability hooks in a continuous integration pipeline, so that “compliance-relevant” outcomes (fairness thresholds, explainability artifacts, human approval before release) are **observable and blocking** when policy is violated—not as a claim of full legal compliance in code, but as an **instantiation** amenable to design-science evaluation. The **Norwegian** context frames **Annex III** high-risk use and national implementation expectations, without implying an industry case study or production banking data.

---

## 2. Methodology — subsection: Operationalization

*Insert under DSR / evaluation; pull tables into thesis body as numbered tables.*

### 2.1 Primary RQ — terms

| Phrase | Meaning in this thesis |
|--------|-------------------------|
| **Design** | A construct (GaC pipeline) + instantiation (working repository) + design principles (discussion). |
| **Automatically enforces** | Executable checks: if a gate fails, the pipeline does not proceed to release (or records failure); not that law is fully automated. |
| **EU AI Act requirements** | Mapped to concrete controls (fairness, transparency/explainability, human oversight, logging)—see compliance matrix. Legal completeness is not claimed. |
| **CI/CD pipeline** | GitHub Actions + local `dvc repro`; deployment is illustrative (artifact + environment), not a production bank stack. |

### 2.2 Sub-RQ 1 — terms

| Term | Definition |
|------|------------|
| **Old way** | **Standard** pipeline profile: optimize for performance; no fairness/SHAP gates on the comparison path. |
| **Non-compliant** | **Operationalized** as failing the fairness threshold (Equalized Odds) and/or the SHAP sanity check when those gates are enabled—not a legal opinion. |
| **Reduce the rate** | One controlled comparison (same seed, same data lineage) plus at least one demonstration where stricter policy or stressed training causes the governed path to block (see project demo doc). Not a statistical sample of models in production. |

### 2.3 Sub-RQ 2 — terms

| Term | Definition |
|------|------------|
| **Latency** | Seconds from end of automated gates to start of the approval job in GitHub Actions, recorded in `metrics/human_oversight_latency.json`. |
| **Limitation** | CI proxy only—not core banking latency, auditor calendar time, or national eID signing. |

---

## 3. Results / Discussion — explicit answers to RQs

*One short paragraph per question; adjust numbers after your final runs.*

### Primary RQ — answer sketch

This work **designs and evaluates** a GaC MLOps **instantiation** for high-risk credit scoring: fairness and explainability **gates** integrated with experiment tracking and reproducible pipelines (MLflow, DVC, GitHub Actions). **Enforcement** is **operational**: failed gates **block** progression to a release-style job or record failure; obligations are **mapped** to controls in the compliance matrix, without asserting that the repository **fully implements** the EU AI Act. **Contributions** are the **artifact**, the **controlled evaluation** (standard vs governed), and **design principles** for adapting similar controls in regulated ML.

### Sub-RQ 1 — answer sketch

Compared to the **standard** profile, the **governed** profile adds automated fairness and SHAP checks. **Non-compliance** is **defined operationally** (e.g. Equalized Odds breach; SHAP gate failure). The governed path **can** prevent a “release” when thresholds are violated; a **policy demonstration** (e.g. tightened fairness threshold or stress mode—see project documentation) shows the gate **blocking** where the standard path would not. The thesis does **not** claim a measured reduction across many production approvals—only **controlled** evidence and a **blocking** demonstration under defined conditions.

### Sub-RQ 2 — answer sketch

Human-in-the-loop is modeled as a **required reviewer** on a protected GitHub **Environment** before a deploy-style job. **Latency** in this proxy is the **automation-to-approval-job** interval (on the order of **seconds** in sample runs—replace with your measured value and cite `human_oversight_latency.json` and workflow URL). This measures **CI orchestration delay**, not end-to-end credit decision time or legal signing workflows.

---

## 4. Limitations — single consolidated block

*Use once (e.g. Methodology + short pointer in Discussion). Avoid scattering the same caveats.*

1. **Data and domain:** The study uses the **UCI South German Credit (UPDATE)** dataset, not Norwegian bank data. **Sensitive attributes** are operationalized via dataset fields (including combined proxies such as `famges` per dataset documentation); findings do not transfer to production credit populations without re-validation.  
2. **Legal:** The compliance matrix is a **scaffold**; final thesis text must **cite EUR-Lex** (or assigned official sources) for Articles; the implementation **operationalizes selected controls**, not the Act in full.  
3. **Sub-RQ1:** Evidence is **controlled comparison** and **demonstrated blocking** under defined thresholds—not a statistical audit of model approval rates in industry.  
4. **Sub-RQ2:** Latency is a **CI/CD proxy** (GitHub Environments), not core banking systems, auditor calendars, or qualified electronic signatures.  
5. **Deployment:** The pipeline is a **research instantiation**; “release” and “environment” are **illustrative**, not a certified production deployment.

---

*Cross-reference: [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md), [THESIS_CUT_LIST.md](THESIS_CUT_LIST.md).*
