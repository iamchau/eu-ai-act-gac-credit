# Thesis draft snippets — paste-ready (Dr. Voss improvements)

Use these **verbatim or lightly adapted** in Word/LaTeX. They align with [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) and [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md). Replace bracketed placeholders with your faculty’s wording and your **final** numbers after runs.

---

## 1. Introduction — positioning paragraph

*Place after problem statement; before RQs.*

The gap addressed in this thesis is not merely abstract “ethics in AI,” but the **operational** distance between **high-risk** credit-scoring obligations under the EU regulatory framework for artificial intelligence (Regulation (EU) 2024/1689) and **day-to-day** machine-learning operations—versioning, testing, and release. **Governance-as-Code (GaC)** is treated here as a **design construct**: selected obligations are **mapped** to executable checks and traceability hooks in a continuous integration pipeline, so that “compliance-relevant” outcomes (fairness thresholds, explainability artifacts, human approval before release) are **observable and blocking** when policy is violated—not as a claim of full legal compliance in code, but as an **instantiation** amenable to design-science evaluation. The **Norwegian** context frames **Annex III** high-risk use and national implementation expectations, without implying an industry case study or production banking data.

---

## 1b. Norway and Annex III — standalone paragraph (optional second paragraph)

*Use if the title says “Norway” and you need one explicit scope sentence.*

Norway is relevant as **jurisdictional context** for how EU high-risk rules intersect with national financial supervision and EEA implementation—not as a source of proprietary credit data in this study. Credit scoring used to evaluate natural persons falls under **Annex III** high-risk AI in the Act’s taxonomy; this thesis **does not** empirically represent Norwegian banks or customers. The **artifact** is a **portable** GaC pattern; any **institutional** deployment would require data, policies, and sign-off processes beyond this repository.

---

## 1c. Final research questions — one sentence each (Introduction)

*Replace informal proposal wording. Aligns with [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §2.*

| RQ | Thesis-ready sentence |
|----|------------------------|
| **Primary** | *How can Governance-as-Code be **designed and instantiated** as a MLOps pipeline for high-risk credit scoring that **maps selected** EU AI Act obligations to **executable** fairness, explainability, and human-oversight controls in CI/CD—**without** claiming that the Act is fully automated or fully implemented in code?* |
| **Sub-RQ1** | *Under **controlled** comparison (same seed, same data lineage), does the **governed** profile (fairness + SHAP gates) **differ** from the **standard** profile—and can **stricter policy** or stress **demonstrate** that the governed path **blocks** when operational non-compliance is detected?* |
| **Sub-RQ2** | *What **automation-to-approval** latency does a human gate add in the **GitHub Actions** instantiation—measured as seconds from **end of automated gates** to **start** of the approval job—and **not** as end-to-end credit decision or legal signing time?* |

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

### 2.4 Sub-RQ 2 — answers vs does not answer

| **In scope** | **Out of scope (state in Methodology or Discussion)** |
|--------------|--------------------------------------------------------|
| Seconds from end of automated gates to **start** of approval job (CI orchestration) | End-to-end latency of a **real** credit decision in a bank |
| One **instantiation** (GitHub Environment + reviewer) | Reviewer **cognitive** time, calendar wait, SLA |
| Illustrative sample(s) with JSON + run URL | Statistical model of “oversight cost” across organizations |

---

## 3. Results / Discussion — explicit answers to RQs

*One short paragraph per question; adjust numbers after your final runs.*

### Primary RQ — answer sketch

This work **designs and evaluates** a GaC MLOps **instantiation** for high-risk credit scoring: fairness and explainability **gates** integrated with experiment tracking and reproducible pipelines (MLflow, DVC, GitHub Actions). **Enforcement** is **operational**: failed gates **block** progression to a release-style job or record failure; obligations are **mapped** to controls in the compliance matrix, without asserting that the repository **fully implements** the EU AI Act. **Contributions** are the **artifact**, the **controlled evaluation** (standard vs governed), and **design principles** for adapting similar controls in regulated ML.

### Sub-RQ 1 — answer sketch

Compared to the **standard** profile, the **governed** profile adds automated fairness and SHAP checks. **Non-compliance** is **defined operationally** (e.g. Equalized Odds breach; SHAP gate failure). The governed path **can** prevent a “release” when thresholds are violated; a **policy demonstration** (e.g. tightened fairness threshold or stress mode—see project documentation) shows the gate **blocking** where the standard path would not. The thesis does **not** claim a measured reduction across many production approvals—only **controlled** evidence and a **blocking** demonstration under defined conditions.

### Sub-RQ 2 — answer sketch

Human-in-the-loop is modeled as a **required reviewer** on a protected GitHub **Environment** before a deploy-style job. **Latency** in this proxy is the **automation-to-approval-job** interval (on the order of **seconds** in sample runs—replace with your measured value and cite `human_oversight_latency.json` and workflow URL). This measures **CI orchestration delay**, not end-to-end credit decision time or legal signing workflows.

**Art. 14 (functional analogue — one sentence, Methodology or Sub-RQ2):**  
The GitHub Environment approval is a **technical analogue** for “human oversight before release” in this DSR artifact; it is **not** a claim that the setup satisfies Article 14 of Regulation (EU) 2024/1689 as a legal matter—verify wording against [EUR-Lex](EU_AI_ACT_CITATIONS.md) and your supervisor.

---

### 3b. Discussion — how the Sub-RQs relate (paste paragraph)

Sub-RQ1 and Sub-RQ2 answer **different** questions and are **not** equally general. Sub-RQ1 addresses whether the **governed** pipeline **differs** from the **standard** path under controlled conditions and whether policy can **block** release when operational criteria fail. Sub-RQ2 addresses **orchestration overhead** for inserting a **human gate** in **this** CI design—not the latency of a real credit decision in a bank, reviewer judgment time, or legal signing. Together they support a **complementary** reading: **effectiveness** of automated gates (Sub-RQ1) and **cost** of the human handoff in the proxy (Sub-RQ2).

---

### 3c. Discussion — velocity vs governance trade-off (optional paragraph)

The **standard** profile optimizes for **training and release velocity** under a performance-only objective. The **governed** profile adds **fairness and SHAP** checks and a **mandatory** human step before a deploy-style job, trading **some** automation speed and **some** CI orchestration delay for **observable** policy enforcement. This trade-off is **instantiation-specific**; production systems would add organizational review time not captured here.

---

## 4. Limitations — single consolidated block

*Use once (e.g. Methodology + short pointer in Discussion). Avoid scattering the same caveats.*

1. **Data and domain:** The study uses the **UCI South German Credit (UPDATE)** dataset, not Norwegian bank data. **Sensitive attributes** are operationalized via dataset fields (including combined proxies such as `famges` per dataset documentation); findings do not transfer to production credit populations without re-validation.  
2. **Legal:** The compliance matrix is a **scaffold**; final thesis text must **cite EUR-Lex** (or assigned official sources) for Articles; the implementation **operationalizes selected controls**, not the Act in full.  
3. **Sub-RQ1:** Evidence is **controlled comparison** and **demonstrated blocking** under defined thresholds—not a statistical audit of model approval rates in industry.  
4. **Sub-RQ2:** Latency is a **CI/CD proxy** (GitHub Environments), not core banking systems, auditor calendars, or qualified electronic signatures.  
5. **Deployment:** The pipeline is a **research instantiation**; “release” and “environment” are **illustrative**, not a certified production deployment.

---

## 5. Evidence checklist (Sub-RQ parity in the binder)

**Sub-RQ1 (evaluative thread — expect more pages):**

- [ ] `metrics/experiment_comparison.json` — standard vs governed under shared controls  
- [ ] **Blocking demo:** exported `fairness_gate.json` with `gate_passed: false` after threshold tightening (see [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md)), **or** documented stress failure  
- [ ] One short paragraph: **not** a sampled “approval rate” from industry  

**Sub-RQ2 (narrow operational thread — do not oversell):**

- [ ] `metrics/human_oversight_latency.json` + **workflow run URL**  
- [ ] State **n** (one run vs several) and that the measure is **automation → approval job**, not banking workflow  
- [ ] **Optional:** One sentence that Sub-RQ1 and Sub-RQ2 are **complementary** (effectiveness vs handoff delay), not equally general claims  
- [ ] If changing Sub-RQ2 focus (traceability, design, trade-offs): see [SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md) and update Introduction + [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §1 / §8  

---

*Cross-reference: [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md), [THESIS_CUT_LIST.md](THESIS_CUT_LIST.md), [SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md).*
