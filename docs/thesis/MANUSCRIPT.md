---

## title: "Implementing the EU AI Act: A Design Science Study on Governance-as-Code (GaC) for High-Risk Credit Scoring in Norway"

author: "[Author Name]"
date: "[Submission year]"

**Institution:** [University / Faculty]  
**Programme:** [Degree programme]  
**Supervisor:** [Name]  
**Repository:** `https://github.com/iamchau/eu-ai-act-gac-credit` (reference implementation)

*Draft manuscript — replace bracketed fields; cite EUR-Lex for all Article quotations in the final PDF.*

**Length target (programme):** ≥ **20,000 words** main text (excluding references and appendices unless your faculty counts them—confirm). The draft below is **expanded** toward that target; run a word count on the exported body and add faculty-specific front matter as required.

---

# Abstract

The EU Artificial Intelligence Act (Regulation (EU) 2024/1689) imposes obligations on providers of high-risk AI systems, including credit scoring that evaluates natural persons. Translating legal and policy expectations into day-to-day machine learning operations remains challenging: performance-driven MLOps pipelines rarely encode fairness, explainability, and human oversight as blocking controls in continuous integration.

This thesis adopts Design Science Research (Hevner *et al.*) and instantiates Governance-as-Code (GaC): selected Act-related expectations are mapped to executable gates (fairness, SHAP explainability, human approval before a release-style job) in a reproducible Python repository with MLflow, DVC, and GitHub Actions. The standard profile optimises predictive performance only; the governed profile adds automated checks. Empirical work uses the public UCI South German Credit (UPDATE) dataset—not Norwegian bank data—under a fixed random seed. Under the baseline fairness budget, accuracy and ROC-AUC match between profiles on the fixed split; tightening the fairness threshold yields an archived fairness-gate failure; one cited GitHub Actions run records 7 seconds from completion of automated gates to start of the approval job (Sub-RQ2), including Environment approval wait when configured—not end-to-end bank or legal signing time.

The methodological stance is Design Science: build an artefact, evaluate it under controlled conditions, and bind empirical claims to versioned outputs. The thesis contributes a reference pattern for mapping high-level governance themes to CI/CD mechanics without asserting that executable checks replace legal analysis or organisational risk management. Norway is used as EEA and pedagogical context rather than as a source of proprietary domestic credit data.

The thesis does not claim full legal compliance or industry adoption. Contributions are: (1) a GaC construct and reference instantiation; (2) controlled evaluation evidence for Sub-RQ1 and Sub-RQ2; (3) design principles for regulated ML pipelines. **Limitation:** proxy sensitive attributes, CI-only oversight latency, single-sample Sub-RQ2 timing, and illustrative deployment—not generalisation to production banking systems.

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
10. [Appendices](#10-appendices) (A–H)

---

# 1. Introduction

## 1.1 Problem and motivation

Credit scoring systems that evaluate natural persons are listed among **high-risk** AI use cases in Annex III of Regulation (EU) 2024/1689 (*European Parliament and Council of the European Union*, 2024). Providers must meet requirements spanning data governance, transparency, fairness, logging, and human oversight—depending on the system’s role and risk management process. In parallel, machine learning practice has converged on **MLOps**: versioned data, automated training, and CI/CD for software-like release of models.

A persistent gap is **operational**: legal and policy language does not automatically appear as **tests** that fail a build when a model violates an internal fairness budget or lacks an explainability artifact. Organisations may adopt policies and principles, yet day-to-day ML work can still ship models that pass accuracy checks while failing internal fairness budgets—unless those budgets are wired into automation. **Governance-as-Code (GaC)** treats selected governance expectations as **code**: policies expressed as thresholds, scripts, and pipeline stages that can block progression when violated. The thesis **does not** claim that **all** Act duties can be reduced to tests; it claims that **some** expectations can be **mapped** to executable controls that support traceability and enforcement in engineering workflows.

## 1.2 Norwegian context (scope)

Norway, as part of the European Economic Area, participates in the **single market** alignment with EU product rules; AI system obligations must be read together with national financial supervision and consumer protection. This thesis uses **Norway** as **jurisdictional and pedagogical context** for high-risk credit scoring. It does **not** use proprietary Norwegian credit data or conduct an industry case study. The empirical work uses a **public** German credit dataset (Section 4.2) with explicit scope limits.

The rationale for naming Norway despite non-Norwegian data is disciplinary and career-oriented: graduates in Norwegian institutions are expected to situate EU product law in EEA context and to connect abstract rules to concrete systems they may encounter in finance. The thesis therefore frames obligations at EU level and signals national supervision as context, without simulating a bank case study.

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

Table 1a **signposts** where each chapter supports the RQs (see [THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md) for full operationalisation).

**Table 1a — Chapter map (RQ coverage)**


| Chapter | Primary RQ (design / instantiation) | Sub-RQ1 (controlled comparison + blocking demo) | Sub-RQ2 (automation-to-approval latency) |
| ------- | ----------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| 1–2     | Problem, scope, literature gap      | Motivation for gates and metrics                | Oversight as CI proxy (framed)           |
| 3–4     | DSR + GaC; data, profiles, ethics   | Method: standard vs governed; evidence binding  | Metric definition + limitations          |
| 5       | **Instantiation** (stack, gates)    | Fairness + SHAP scripts; CI matrix              | Gate C workflow + Environment            |
| 6       | —                                   | **Results:** Table 2–3, committed JSON          | **Results:** latency JSON + run URL      |
| 7–8     | Principles, limits, future work     | Interpretation of Sub-RQ1 demo                  | Interpretation of Sub-RQ2 sample         |


Narrative spine: Chapter 2 reviews responsible AI, MLOps, and the EU AI Act high-risk framing. Chapter 3 presents Design Science Research and GaC. Chapter 4 describes methodology, data, and limitations. Chapter 5 describes the instantiation. Chapter 6 reports results. Chapters 7–8 discuss and conclude. References and appendices follow.

## 1.6 Significance for practice and education

For students entering finance and IT roles in the EEA, the AI Act is not an abstract headline; it structures product obligations and internal governance expectations for high-risk systems. University training often separates law and ethics from MLOps labs. This thesis demonstrates a pedagogically useful integration: the same Git repository that trains a model also encodes fairness and explainability gates and a human approval path with measurable latency. That integration supports professional competence in traceable ML delivery without overstating legal effects.

## 1.7 Delimitations (summary)

The thesis does **not**: (i) evaluate a Norwegian bank system; (ii) provide legal advice; (iii) sample production approval workflows at scale; (iv) claim statistical representativeness for Sub-RQ2; (v) implement all Title III controls. It **does**: (i) instantiate GaC in code; (ii) bind empirical claims to committed JSON; (iii) demonstrate blocking under tightened fairness policy; (iv) report one CI latency observation with a clear definition. Full limitations are integrated in Section 7.5 (methods detail in Section 4.5). Proposal-versus-implementation alignment is tabulated in [THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md) (Section 4).

## 1.8 Empirical strategy in one page

The empirical work is controlled comparison plus demonstration. First, the thesis fixes the seed and data lineage so that standard and governed profiles are comparable. Second, it reports metrics from committed `experiment_comparison.json`. Third, it archives a fairness gate failure under a tightened threshold to show blocking behaviour. Fourth, it records one Sub-RQ2 latency sample with a workflow URL. These steps are designed for examiner verification and open replication, not for population-level statistical inference.

## 1.9 How to read this thesis with the repository

Read Chapters 1–4 for questions and methods. Chapter 5 maps to folders and workflows in the repository. Chapter 6 must match JSON files line-for-line for numbers. Chapters 7–8 interpret scope and limits. Appendices collect parameters, matrix scaffolds, metric excerpts, and evidence indices.

## 1.10 Terminology note

Governance-as-Code (GaC) means versioned executable checks mapped to selected policy expectations. Operational non-compliance means gate failure under the thesis definitions, not a legal finding. High-risk refers to Annex III framing under the Act where applicable, without claiming a concrete deployment context beyond the research instantiation.

---

# 2. Background and literature

This chapter situates the thesis in **algorithmic fairness**, **MLOps practice**, **post-hoc explainability**, and the **EU AI Act** framing for **high-risk** systems—including credit scoring in **Annex III**. The goal is not to reproduce legal commentary in full, but to show **why** an engineering artefact that encodes **gates** in CI/CD is a plausible response to an **operational** gap between abstract duties and day-to-day ML workflows. Throughout, the thesis distinguishes **legal** obligations (interpreted with faculty guidance and EUR-Lex) from **operational** proxies implemented in code.

## 2.1 Responsible AI and algorithmic fairness

### 2.1.1 Group metrics and trade-offs

Fairness in supervised classification is often discussed through **group** metrics that compare error rates or score distributions across groups defined by a **sensitive attribute** (Mehrabi *et al.*, 2021). Common formulations include **demographic parity** (equal positive prediction rates across groups), **equalized odds** (equal true/false positive rates across groups when sensitive attributes are binary or binarised), and related **calibration** notions. These metrics can **conflict** with one another and with **predictive utility** (accuracy, ROC-AUC) on fixed data; a large body of work documents **impossibility** and **trade-off** results under general conditions. For this thesis, the point is not to resolve philosophical debates about the “right” fairness definition, but to **operationalise** one chosen metric **transparently** in a pipeline gate so that **policy** is expressed as **executable** thresholds and **failures** are **observable**.

### 2.1.2 Equalized odds and this thesis

This thesis uses **equalized odds** (via **Fairlearn**) as implemented in **Gate A**, computed on **validation** predictions relative to a **sensitive column** (`famges`, with fallback described in Chapter 4). The **equalized odds difference** (EOD) is compared to a **maximum allowed** value in `params.yaml`. The **gate** is not a claim that the model is “fair” in a legal sense; it is a **repeatable** engineering check that **blocks** when the measured EOD exceeds the configured budget. **Legal** non-discrimination and **creditworthiness** assessments in EU/EEA law are **not** reducible to a single ML metric; Veale *et al.* (2021) emphasise that **legal** duties and **algorithmic** fairness tools must be **aligned** with care. This thesis therefore **does not** equate EOD compliance with **Regulation** compliance.

### 2.1.3 Proxy attributes and interpretation limits

The UCI dataset uses **coarse** demographic proxies; **protected characteristics** under national law may differ in definition and scope. Using `famges` as a sensitive column is a **methodological** choice for **demonstration** in a public dataset context, not a claim that the column maps cleanly to protected categories in Norway or the EU. **Proxy** use is a **limitation** (see Section 4.5) and affects **external validity**: any generalisation of the empirical findings to **Norwegian** credit practice is **indirect** and **contextual**, not statistical.

### 2.1.4 Mitigation and scope

The repository **does not** implement advanced **mitigation** (e.g. Fairlearn reductions, post-processing) as the default thesis path; the thesis instead focuses on **measurement** and **blocking** under tightened policy. **Mitigation** is noted as **future work** (Chapter 7) because it would introduce additional design choices and evaluation complexity beyond the stated **Sub-RQ1** scope.

### 2.1.5 Demographic parity and calibration (contrast)

Demographic parity requires equal positive prediction rates across groups (for binary classification). It can conflict with equalized odds when base rates differ. Calibration across groups is another notion often discussed in credit scoring because lenders care about probability estimates for pricing and limits. This thesis does not implement calibration gates; they could be added as future work if the programme requires multi-metric evaluation.

### 2.1.6 Individual fairness and distance metrics

Individual fairness asks that similar individuals receive similar outcomes under a defined metric on inputs. Operationalising individual fairness requires careful feature choice and can be computationally expensive. The UCI dataset’s row-level semantics are not rich enough to justify strong individual fairness claims here; the thesis remains at group fairness via EOD.

### 2.1.7 Fairness under distribution shift

Production credit systems experience covariate shift and concept drift. Fairness metrics computed on a static validation split do not guarantee fairness after drift. Industry practice often pairs fairness monitoring with drift detection on inputs and outputs. A natural extension to this thesis would add a drift gate or periodic batch checks post-deployment; that is out of scope for the instantiation as written.

### 2.1.8 Intersectionality and coarse groups

Real populations have intersectional structure; coarse binary splits can hide disadvantage within subgroups. The thesis uses a single sensitive column for demonstration and acknowledges that intersectional analysis would require more data and careful definition of groups.

## 2.2 MLOps, reproducibility, and “policy as code”

### 2.2.1 MLOps as an engineering baseline

MLOps combines **continuous integration** (testing, build) with **continuous delivery** of models and artefacts: versioned **datasets**, **features**, **training code**, **hyperparameters**, **metrics**, and **deployment** packages. Industry practice emphasises **reproducibility** (same seed, same data hash, same container), **observability** (logs, metrics), and **release discipline** (promotion gates). For credit scoring, this operational discipline is **compatible** with—but not identical to—**governance** expectations for **high-risk** AI under the Act.

### 2.2.2 From ethics principles to failing builds

Surveys of **AI ethics guidelines** (Jobin *et al.*, 2019) and of **bias and fairness** in machine learning (Mehrabi *et al.*, 2021) show convergence on abstract principles—**transparency**, **fairness**, **accountability**, **human oversight**—while leaving **implementation** open. **Governance-as-Code (GaC)** treats selected expectations as **machine-readable** artefacts: thresholds, scripts, and pipeline stages that can **fail** a pipeline run when violated. This is **not** “full automation of law”; it is a **controlled** way to make **policy breaches** visible in **engineering** workflows.

### 2.2.3 Supply-chain analogies and boundaries

Software **supply-chain** security emphasises **signed** artefacts, **dependency** scanning, and **policy** checks in CI. GaC borrows the **spirit** of **policy-as-code**—**express** rules in version control, **review** changes, **enforce** in automation—but applies it to **ML governance** choices (fairness, explainability artefacts, **human** approval before release). **Organisational** governance (committees, legal review, model risk management) remains **outside** the repository; the thesis **instantiation** is a **research** artefact, not a bank’s **SDLC**.

## 2.3 EU Artificial Intelligence Act—high-risk framing (non-exhaustive)

Regulation (EU) 2024/1689 establishes harmonised rules for AI systems placed on the **EU market** or **put into service** (*European Parliament and Council of the European Union*, 2024). **Annex III** lists **high-risk** use cases, including **creditworthiness** evaluation of **natural persons** (where applicable). **Providers** of high-risk systems must satisfy **Title III, Chapter 2** requirements, which include **risk management**, **data governance**, **technical documentation**, **record-keeping**, **transparency**, **human oversight**, **accuracy**, **robustness**, and **cybersecurity**—**as specified in the Articles** and in the official **consolidated text**.

**For the final thesis PDF**, the author must **quote** or **paraphrase** Articles with **EUR-Lex** references as required by the faculty; **Appendix B** and the **compliance matrix** (`docs/COMPLIANCE_MATRIX.md`) are **scaffolds** mapping **themes** to **controls**, not a substitute for **legal analysis** or **supervision**. This thesis **does not** claim that the **Gate A/B/C** implementation **fully satisfies** any Article; it claims **mapping** to **selected** **operational** controls.

### 2.3.1 Why “credit scoring” appears in the title and Norway in the scope

The **title** uses **high-risk credit scoring** to align with **Annex III** framing. The **empirical** work uses a **public German** credit dataset; **Norway** is **jurisdictional context** (EEA alignment with EU product rules; national financial supervision and consumer protection) as in Section 1.2. The thesis does **not** claim **national** representativeness of the dataset.

### 2.3.2 Thematic map from Title III, Chapter 2 (illustrative; cite EUR-Lex in PDF)

Commentary on high-risk providers under Title III, Chapter 2 typically groups expectations under recurring themes. The list below structures literature and the compliance matrix (`docs/COMPLIANCE_MATRIX.md`); precise duties depend on Article wording in the consolidated text.

**Risk management and quality.** Commentary often links this theme to systematic identification and mitigation of risks across the lifecycle. This thesis does not implement a full ISO-style risk management system; the repository supports traceability and repeatable evaluation as partial building blocks.

**Data and data governance.** Expectations concern training data, validation, representativeness, and documentation. The instantiation logs provenance strings (`data_provenance` in metrics) and uses fixed splits with a documented seed.

**Technical documentation and record-keeping.** Artefacts include metrics JSON, SHAP reports, MLflow run metadata, and git/DVC digests—supporting an audit-style trail at engineering level.

**Transparency and information to deployers.** SHAP summaries and `feature_schema.json` are engineering artefacts that support downstream communication; they do not replace mandatory disclosures under the Act where applicable.

**Human oversight.** Gate C models approval before a release-style job in CI as a functional analogue of “human oversight before release” in automation; it is not a legal conclusion of Article 14 compliance.

**Accuracy, robustness, and cybersecurity.** The baseline model reports accuracy and ROC-AUC; robustness and cybersecurity are only lightly illustrated (e.g. optional API limits on the serving demo). Readers must not infer that every theme is fully implemented—Appendix B remains a scaffold.

### 2.3.3 Why a thematic map is not legal analysis

Legal analysis requires close reading of Articles, recitals, and applicable harmonised standards as they apply to a concrete deployment context (provider vs deployer, credit bureau vs lender, etc.). This thesis stays at the level of engineering mapping and DSR evaluation. If a programme requires a dedicated law chapter, that should be supervised as legal research separate from the software artefact.

## 2.4 Explainability and post-hoc methods (SHAP)

**Transparency** obligations in the Act are often discussed alongside **explainability** in ML. **SHAP** (Lundberg & Lee, 2017) provides **feature attribution** explanations for predictions; in this thesis, **Gate B** requires **generation** of a SHAP summary (`artifacts/shap_report.md`) and metrics (`metrics/shap_gate.json`). The baseline threshold `min_top_mean_abs_shap: 0.0` in `params.yaml` makes **Gate B** primarily a **documentation** and **presence** check rather than a **strict** performance criterion; **raising** the threshold would make SHAP-driven **failure** more likely. **Post-hoc** explanations can be **misleading** under certain conditions; the thesis treats SHAP as **one** **audit-style** artefact in a **governed** path, not as proof of **meaningful** explanation to **data subjects**.

## 2.5 Norway, EEA alignment, and national context (brief)

Norway participates in the **EEA** through the **EEA Agreement**; **EU regulations** listed in **Annex** to the Agreement are **incorporated** into the **EEA** legal order with **national** procedures. **AI Act** obligations for **placing** systems on the market or **putting** them into service must be read **together** with **sector** rules (e.g. **financial** supervision, **consumer credit** and **marketing** rules). This thesis **does not** analyse **national transposition** in depth; **future work** may extend the **legal** chapter if the programme requires it.

## 2.6 Gap addressed

The gap addressed is **operational**: bridging high-level **policy** language and **executable** ML pipeline controls that can **fail** in CI/CD. **Prior** work in **AI ethics** and **fair ML** supplies **conceptual** foundations; **MLOps** supplies **engineering** practice; **EU AI Act** commentary supplies **legal** framing. This thesis contributes a **DSR artefact** (GaC instantiation) and **measurement** (Sub-RQ1/Sub-RQ2), **not** a **legal compliance certificate**.

## 2.7 Related work on ML governance tooling and enterprise practice

Beyond academic surveys, industry practice has produced model risk management (MRM) frameworks, model inventories, and governance platforms that track models across their lifecycle. Such systems often emphasise workflow, approvals, and documentation rather than executable gates in the same repository as training code. Open-source MLOps stacks (e.g. Kubeflow, MLflow, DVC) focus on reproducibility and deployment; fairness toolkits (Fairlearn, AIF360) focus on measurement and mitigation in notebooks or batch jobs. This thesis contributes a tight integration pattern: selected governance checks as first-class CI stages with the same versioning discipline as code, which is conceptually distinct from post-hoc documentation alone. Cite vendor and open-source documentation only as secondary sources if your faculty allows; peer-reviewed literature on MLOps and DSR remains the primary academic anchor.

## 2.8 Automated credit decisions: EU law context beyond the AI Act (non-exhaustive)

The EU AI Act is not the only legal frame relevant to credit scoring. The General Data Protection Regulation (GDPR) governs personal data processing and includes provisions on automated decision-making that must be read together with sector and product rules. This thesis does not perform a full GDPR analysis; it notes that engineering artefacts such as logs, explanations, and human review hooks are discussed in both privacy and AI governance debates. A dedicated GDPR compliance analysis may be added to the final PDF only where the faculty requires it, with supervisor-approved sources (see `docs/thesis/README.md`).

Consumer credit law at EU level has historically emphasised precontractual information, creditworthiness assessment, and responsible lending. National supervisors (for example Finanstilsynet in Norway) publish guidance on risk management and consumer protection that may interact with how institutions deploy models. That guidance is not “implemented” by this repository; Norway is used as context to motivate why traceable ML pipelines matter professionally.

From a methods standpoint, the important point is separation of concerns: (i) product law for high-risk AI systems (AI Act), (ii) data protection law (GDPR), (iii) sector rules for credit and markets, and (iv) internal organisational policies. Governance-as-Code in this thesis partially addresses (iv) at the level of engineering controls and does not substitute for (i)–(iii).

## 2.9 Synthesis of the literature gap

Prior work establishes that (a) fairness metrics and explainability tools exist, (b) MLOps practices exist, and (c) EU AI law commentary exists. The gap is integration: relatively few open reference implementations show how selected themes map to blocking CI gates with committed metrics and a human approval path measured end-to-end in automation. This thesis fills that gap at DSR artefact level with explicit limitations on legal and statistical generalisability.

## 2.10 Production ML, technical debt, and testability

Machine learning systems in production are more than training scripts: they include data pipelines, feature engineering, serving infrastructure, monitoring, and organisational processes. Sculley *et al.* (2015) argue that ML systems accumulate **hidden technical debt** when interfaces, data dependencies, and feedback loops are left implicit. Debt is not only “bad code”; it is **misalignment** between what teams assume about data and what actually happens in the wild. That framing is relevant for governance: if fairness and oversight are treated as **offline** analyses that never become **blocking** checks in the path to release, they can drift away from production behaviour.

Polyzotis *et al.* (2017) catalogue **data management** challenges in production ML, including **data cascades**—where upstream labelling or selection choices distort downstream models. A fairness gate on a fixed validation split does **not** solve data cascades; it **documents** one slice of behaviour under one policy. Acknowledging that limit is part of honest scope.

Breck *et al.* (2017) propose an **ML test score** rubric: structured checks for data, model, and production readiness. The thesis does **not** implement the full rubric; it **aligns** with the **spirit** of **tests-as-gates**—binary pass/fail criteria that can be automated. Where a bank might require dozens of checks, this thesis demonstrates a **minimal** **GaC** slice: fairness, SHAP artefacts, human approval, and traceability tags.

Continuous integration and delivery for ML mirror **site reliability engineering** (SRE) ideas: define service level objectives where meaningful, prefer automation over manual toil, and make failures **visible** early. GaC gates are **SRE-like** in the narrow sense that they turn “we should check fairness” into a **job** that either **passes** or **fails** with logs. They are **not** SRE for **customer-facing** **availability** of a **credit** **API** in this thesis—the serving stack is **illustrative**.

## 2.11 Explainability: interpretability, documentation, and limits

Interpretability in ML spans intrinsically interpretable models (e.g. small linear models with clear coefficients), post-hoc explanations (SHAP, LIME), and process documentation (how a model was trained). The EU AI Act’s transparency obligations for high-risk systems are legal constructs; they are not satisfied by publishing a SHAP plot alone. Rudin (2019) cautions against “explainable black box” culture as a substitute for domain-appropriate modelling when high-stakes decisions are involved. This thesis uses logistic regression for stability and baseline interpretability, yet still adds SHAP as a gate artefact because post-hoc summaries are common in MLOps practice and support audit-style review of feature attribution on the validation set.

Limitations of SHAP include approximation (depending on implementation), dependence on the background sample, and misleading attributions under correlation or leakage. Gate B with `min_top_mean_abs_shap: 0.0` does not claim that explanations are “correct” for every applicant; it claims that a standardised report was generated and archived as part of the governed path.

## 2.12 Research streams informing the thesis (synthesis)

Three streams converge. First, normative AI ethics and fair ML research supply definitions and criticisms of metrics (Section 2.1). Second, systems and software engineering research on ML operations (Sections 2.2 and 2.10) supplies language for tests, debt, and release discipline. Third, EU technology law and policy literature (Sections 2.3 and 2.8) frames obligations at a level that does not map one-to-one to shell commands. This thesis contributes a bridge artefact that is explicitly partial: it implements a subset of controls that can be automated in a student-scale repository without pretending to close every gap in Title III.

## 2.13 Harmonised standards and conformity assessment (context only)

The AI Act foresees harmonised standards and conformity assessment procedures for high-risk systems as the legal framework matures. Notified bodies and standardisation work will influence what “state of the art” means in practice for documentation, testing, and risk management. This thesis does not claim conformity with future harmonised standards; it positions GaC as a complementary engineering practice that could later be mapped to specific standard clauses when they are finalised and cited from official sources.

For the thesis as written, the relevant takeaway is processual: organisations will need repeatable evidence that models were trained, evaluated, and released under known policies. Versioned gates in CI contribute to that evidence base at the software layer.

## 2.14 Credit modelling practice and model risk (industry context)

Banks and credit institutions traditionally separate model development, validation, and approval under model risk management (MRM) frameworks inspired by supervisory guidance. In the United States, Federal Reserve SR 11-7 is a frequently cited reference for model risk management; it is not directly applicable in the EEA, but it illustrates how institutions structure independent validation, documentation, and approval. Validation often includes out-of-time and out-of-sample tests, stability analysis, and policy for override and appeal. Machine learning models introduce additional risks: data leakage, overfitting, and opacity relative to linear scorecards.

This thesis does not replicate a full three-lines-of-defence governance structure. It shows how two ingredients—automated metric gates and human approval before a release job—can be implemented in code with traceable outputs, which is compatible with MRM-style narratives even when organisational roles are not simulated.

## 2.15 Reproducibility in computational research

Computational reproducibility—re-running an analysis and obtaining the same outputs—is a baseline expectation in many scientific fields, yet ML work often falls short because data versions, random seeds, and library versions drift. Work on reproducible computational research emphasises containers, version pins, and open artefacts (see Stodden & Miguez, 2014, on best-practice reporting; see also broader surveys on reproducibility in science). This thesis adopts a pragmatic subset: fixed seed, committed metrics JSON, and git identifiers embedded in MLflow tags. That is not full bit-for-bit reproducibility across all platforms, but it is stronger than reporting only accuracy in prose.

## 2.16 Fair lending and non-discrimination: international parallels (non-exhaustive)

Scholarship and regulation on credit and discrimination differ by jurisdiction. In the United States, fair lending enforcement has a long history connected to disparate impact and disparate treatment concepts in civil rights law. In the EU/EEA, non-discrimination frameworks and consumer credit rules use different legal tests and institutions. This thesis does not map EOD to any specific legal test; it uses Fairlearn as an engineering construct for the DSR artefact. Readers with a law background should treat Chapter 2 as context, not as counsel.

## 2.17 CI/CD in research repositories versus bank SDLCs

Academic repositories often use GitHub Actions for continuous integration without full continuous deployment to regulated environments. Banks typically use private git hosts, artifact repositories with access controls, and change advisory boards. The pattern “train → test → gate → approve → release” is analogous even when tooling differs. The thesis instantiation is closer to open research practice than to a tiered bank network.

## 2.18 Observational fairness and causal reasoning (scope note)

Many fairness metrics are observational: they summarise joint distributions of inputs, predictions, and group labels in a dataset. Causal fairness research asks what would happen under interventions or counterfactual changes to data-generation processes (Pearl-style reasoning and related work). This thesis does not estimate causal effects; Gate A’s equalized odds difference is descriptive on the validation split under Fairlearn’s definitions. That scope limit is intentional: causal identification typically requires stronger assumptions and richer domain knowledge than a single public benchmark provides.

Researchers should not interpret observational fairness metrics as answering “what if we changed the world?” questions. They answer narrower engineering questions: “does this trained model exceed a stated disparity budget on this split, under this metric implementation?” Organisations may still use such gates as early warnings before deeper analysis.

## 2.19 Robustness and adversarial considerations (brief)

Robustness and cybersecurity are explicit themes in Title III, Chapter 2. The repository includes optional API limits for serving demos but does not run adversarial robustness evaluations or penetration tests on the scoring API. Extending GaC with robustness gates—input perturbation tests, distribution shift monitors, or security scans—would strengthen a production story but also multiply maintenance cost. The thesis notes the gap rather than filling every security dimension.

## 2.20 Human oversight beyond a single approval click

Human oversight in organisations includes training, competence management, escalation paths, and post-hoc audit. Gate C measures only automation-to-approval latency in CI: a thin slice of “oversight as workflow.” It does not measure whether the approver understood model risk, whether appeal processes exist for applicants, or whether oversight satisfies legal duties. Sub-RQ2 is therefore framed narrowly to avoid conflating CI mechanics with comprehensive human governance.

## 2.21 Synthesis: what Chapter 2 enables for Chapter 3

Chapter 2 supplies the vocabulary and boundaries for the construct in Chapter 3: GaC is an engineering response to an operational gap between abstract duties and executable checks, not a legal shortcut. The next chapter states evaluation criteria and the DSR mapping explicitly.

## 2.22 Chapter summary

Chapter 2 established: (i) fairness metrics and limits, including observational vs causal scope; (ii) MLOps and policy-as-code; (iii) EU AI Act high-risk framing without legal advice; (iv) explainability via SHAP as an engineering artefact; (v) Norway/EEA context; (vi) the operational gap; (vii) enterprise and open-source related work; (viii) GDPR/credit law sketches; (ix) technical debt and testing literature; (x) interpretability debates; (xi) synthesis; (xii) standards context; (xiii) MRM context; (xiv–xvii) reproducibility, fair-lending parallels, and CI/CD positioning; (xviii–xxi) causal scope note, robustness sketch, human oversight limits, and bridge to DSR. Chapter 3 formalises DSR and the GaC construct.

## 2.23 EU digital policy context (brief)

The AI Act sits alongside other EU initiatives on data, digital markets, and cybersecurity. A full policy synthesis is outside scope; the thesis nevertheless acknowledges that product rules for AI systems interact with sectoral regulation and consumer protection. Students are encouraged to read official Commission communications and supervisory guidance as directed by their supervisor.

## 2.24 Why UCI credit data is used despite limitations

Public UCI datasets are small and dated relative to modern banking features. They remain valuable for reproducible research because they are documented, licensed, and widely used as benchmarks. The thesis prioritises open replication over realism of features, explicitly trading external validity for evidence accessibility.

## 2.25 Explainability tools in credit scoring research

Industry and academia have experimented with explanation dashboards, reason codes, and post-hoc explanations for credit decisions. Regulatory expectations differ by jurisdiction. This thesis implements one narrow slice: SHAP-based reports as pipeline outputs, without claiming equivalence to mandatory disclosures to applicants.

## 2.26 Benchmarks and leaderboards versus governance science

Leaderboards reward accuracy. Governance science asks whether systems fail safely under policy constraints. The thesis does not optimise for leaderboard rank; it demonstrates a governed path that can block when policy tightens. That is a different scientific objective.

## 2.27 Learning outcomes alignment (illustrative)

Typical MSc learning outcomes include applying scientific methods, ethical reflection, and clear communication. This thesis addresses them by: (i) DSR methodology with explicit evaluation; (ii) careful scope statements on law and fairness; (iii) structured chapters and evidence binding. Where the programme publishes official outcome wording, that text should replace this subsection after supervisor review (`docs/thesis/README.md` author checklist).

## 2.28 Literature search strategy (replicable template)

A literature chapter can be strengthened by making the search **replicable** rather than impressionistic. A practical approach is to combine database queries with backward and forward citation tracing from anchor papers already central to the thesis (fairness tooling, MLOps debt, EU AI governance, and credit-risk modelling). Typical databases include Scopus, the ACM Digital Library, and IEEE Xplore; arXiv can supplement preprints where peer-reviewed coverage lags fast-moving tooling. Keyword bundles might combine *fair machine learning*, *algorithmic fairness*, *MLOps*, *continuous integration*, *model governance*, *EU AI Act*, *high-risk AI*, *credit scoring*, and *consumer credit*, with Boolean connectors adjusted per database syntax.

Inclusion criteria should be explicit: for example, English-language peer-reviewed articles and reputable grey literature (standards, regulator guidance) within a defined year window, unless a historical source is needed for legal evolution. Exclusion criteria might remove purely theoretical papers with no engineering implications if the thesis scope is applied, or conversely retain them if the programme expects philosophical depth—this is a supervisory decision. Document the number of records retrieved, duplicates removed, titles screened, abstracts read, and full texts assessed. Even a lightweight PRISMA-style paragraph signals methodological care.

Snowballing remains important because ML systems work spans venues (KDD, FAccT, NeurIPS workshops, industry blogs mirrored into proceedings). The present manuscript embeds a starter reference set aligned with the artefact; further reading should follow the programme’s required breadth and the consolidated EU law version in force at submission. Documenting queries, dates run, and PDF locations in a spreadsheet supports a defensible literature process (`docs/thesis/README.md`).

## 2.29 Debates in fair ML that gates cannot settle

Fair machine learning is not a single technical problem with a single technical solution. Researchers have shown impossibility-style results under certain conditions: multiple fairness criteria cannot always be satisfied simultaneously without trivialising the predictor or changing the base rates’ interpretation. Debates continue over observational versus causal fairness, over which groups should be protected and how group membership is inferred from data, and over whether fairness metrics should be computed on outcomes, decisions, or counterfactuals. Separately, practitioners argue about trade-offs between fairness and accuracy, stability under distribution shift, and the legitimacy of post-hoc adjustments.

Governance-as-code gates do **not** resolve these debates. A threshold in a YAML file or a fairness gate in CI encodes an organisation’s **temporary policy choice** and makes it testable and repeatable. Philosophical critique belongs at the layer of law, ethics, and organisational policy: what to measure, what to prioritise, and what to disclose. Engineering critique belongs at the layer of measurement validity, leakage, and robustness: whether the implemented test matches the policy intent. The thesis tries to keep those layers distinct so that reviewers do not mistake a pipeline check for a moral conclusion or a legal compliance certificate.

## 2.30 From draft AI Act commentary to consolidated law

Secondary sources written while the AI Act was a proposal remain valuable for conceptual history—for example, how scholars anticipated risk tiers, conformity logic, and fundamental rights framing—but they may cite Articles that were renumbered or amended. Veale and Zuiderveen Borgesius (2021) exemplify early commentary oriented toward fundamental rights and consumer-facing explanation expectations. For the submitted thesis PDF, direct quotations of obligations, definitions, and procedural requirements should come from the **consolidated** Regulation as published for the EU Official Journal and retrieved via EUR-Lex, with recital and Article numbers checked against that version.

Treat older blog posts, draft PDFs, and workshop slides as **historical** unless the authors explicitly updated them after adoption. Where national supervisors add sector guidance (for example, banking supervisors interpreting model risk management alongside AI Act duties), cite those documents with care and date them; they change faster than peer review cycles. This discipline reduces examiner objections about stale legal citations and signals professional care in a law-adjacent technical thesis.

## 2.31 Maturity models, CMMI-style thinking, and what GaC adds

Enterprises sometimes describe analytics capability with maturity scales: ad hoc experiments, managed projects, standardised production, then optimised continuous improvement. Academic analogues include capability maturity models borrowed from software engineering. Such models help allocate investment and set roadmaps, but they risk becoming label theatre if “level four” slides do not connect to verifiable controls.

Governance-as-code aligns naturally with **higher maturity** themes—automation, repeatability, evidence—but this thesis does **not** claim a maturity level for any organisation. Instead, it contributes a **concrete mechanism**: versioned gates that fail builds when policy thresholds are breached, plus logged artefacts suitable for audit trails. A maturity roadmap might still be necessary for budgeting and training; GaC can be one brick in that roadmap without replacing governance committees, second-line risk functions, or legal interpretation.

## 2.32 Ethics of benchmarking on historical credit data

Public credit datasets such as the German Credit Data (UCI) are convenient for reproducible methods research because rows and columns are stable and baselines are widely reported. Ethically, they encode past lending decisions that may reflect discrimination, incomplete records, or product designs that no longer exist. Benchmarking accuracy or fairness on such data does not validate real-world fairness for today’s applicants; at best it validates that an implementation matches prior papers under the same split assumptions.

This thesis uses the data strictly as a **reproducible demonstration substrate**: fixed splits, explicit proxy-variable warnings, no individual-level inference, and no claim that results transfer to a live portfolio. Where examiners ask “why not proprietary bank data,” the answer is triadic: confidentiality, scientific replicability for assessment, and alignment with open-science expectations for a student artefact. The ethical posture is conservative transparency about limits rather than over-claiming external validity.

## 2.33 Industry co-supervision and publication boundaries

When a workplace mentor co-supervises, clarify early what may appear in a public repository versus an appendix marked confidential or omitted entirely. Employment contracts, vendor evaluations, and incident post-mortems are typically off limits. This repository is structured so the thesis can be examined without exposing employer secrets: synthetic or public data, generic gate logic, and citations to law and standards rather than internal policy manuals.

If the student later adapts the artefact internally, a separate private fork may contain organisation-specific thresholds and integration hooks. The academic submission should describe that bifurcation abstractly so examiners understand how the public demo relates to a plausible deployment without breaching confidentiality.

## 2.34 Automation bias, green builds, and the limits of “pass”

Automation bias names the tendency to defer to machine-generated recommendations or green status indicators. In CI, a passing pipeline can psychologically signal “safe to ship” even when tests are narrow. A fairness gate might pass while data drift silently invalidates assumptions; an explainability artefact might render while omitting legally required narrative context; a documentation gate might check presence without checking accuracy.

The thesis mitigates automation bias in three ways: by stating limits explicitly in Chapters 1, 4, and 7; by binding claims to committed JSON metrics rather than hand-waved performance; and by treating human oversight latency as an empirical object rather than a checkbox. Checklist culture—ticking boxes without sensemaking—is a genuine organisational risk. Gates are presented as **necessary but insufficient** supports for responsible ML operations.

## 2.35 Bridge to Chapter 3

Chapter 2 established definitions, related work, and tensions between research practice and regulatory expectations. Chapter 3 turns to the Design Science Research framing: the GaC construct as an artefact, evaluation criteria aligned to the research questions, iteration and versioning, and explicit statements about what counts as evidence in this thesis. That sets up Chapter 4’s detailed method and traceability without duplicating the conceptual map.

---

# 3. Theoretical framework

## 3.1 Design Science Research (Hevner *et al.*)

Design Science Research (DSR) in information systems produces artifacts—constructs, models, methods, and instantiations—that address relevant problems and are evaluated with rigor (Hevner *et al.*, 2004). The knowledge contribution arises from building something novel within scope and showing how it behaves under controlled evaluation. Hevner *et al.* emphasise relevance (business or environmental problem), rigor (appropriate methods and prior knowledge), and design (iterative artefact construction and assessment).

### 3.1.1 Mapping this thesis to DSR cycles

This thesis maps to DSR as follows:

- **Relevance.** High-risk credit scoring under the EU AI Act framing intersects with MLOps practice; the gap is that governance expectations are not automatically enforced as blocking controls in ML pipelines unless encoded as tests.
- **Rigor.** The knowledge base draws on fairness tooling (Fairlearn), explainability (SHAP), reproducible evaluation (fixed seed, stratified split, committed JSON metrics), and CI workflows (GitHub Actions).
- **Design.** The artifact is a GaC instantiation—gates in code and CI—plus evaluation procedures for Sub-RQ1 and Sub-RQ2.

### 3.1.2 Artifact types in this thesis

Following Hevner’s taxonomy, this work primarily delivers an instantiation (working repository) and construct elucidation (Governance-as-Code as operationalised here). Method elements include the comparison protocol (`compare_profiles`) and the latency measurement approach for Sub-RQ2. Evaluation is functional (does the gate block when policy tightens?) and descriptive (what latency was observed in a cited CI run?), not a field trial of organisational adoption.

### 3.1.3 Relation to Peffers *et al.* (optional methodological naming)

Peffers *et al.* (2007) propose a DSR methodology with steps such as problem identification, objectives, design and development, demonstration, evaluation, and communication. This thesis implicitly follows that arc: problem (Section 1), objectives (RQs), development (Chapters 4–5), demonstration (Chapter 6), communication (thesis). The steps may be named explicitly in the final PDF if the faculty prefers a labelled DSR process.

## 3.2 Governance-as-Code (construct)

**Governance-as-Code** is defined in this thesis as mapping selected governance expectations to versioned, executable checks in the training and release path, such that violations are observable (logs, metrics, failed jobs) and can block progression to later stages. GaC is complementary to organisational governance: it does not replace legal review, model risk committees, or regulatory supervision.

### 3.2.1 Gates as policy instruments

Gates (A: fairness, B: SHAP, C: human approval) materialise selected policy choices as code: thresholds in `params.yaml`, scripts in `src/`, and workflow jobs in `.github/workflows/`. Changing policy is thus visible in version control (diffs, reviews), which supports traceability—a theme often associated with high-risk system documentation expectations, though traceability here is technical, not a claim of Article-level completeness.

### 3.2.2 What GaC does not claim

GaC does not fully automate legal interpretation. It does not certify conformity with all Title III requirements. It does provide a research reference for how selected duties can be linked to CI/CD mechanics for discussion and further institutional adaptation.

## 3.3 Evaluation criteria for this DSR artefact

DSR evaluation is not one-size-fits-all. For this thesis, the following criteria are explicit:

**Utility.** Does the instantiation make governance expectations observable and actionable for engineers (failed jobs, metrics JSON, artefacts)? The thesis argues yes, within scope.

**Feasibility.** Can a motivated MSc student reproduce the comparison and gates using the repository? The replication sections (4.7–4.9, Appendix F) exist to support yes, modulo machine and GitHub configuration.

**Rigour.** Are claims bound to committed files rather than informal memory? Evidence binding (Chapters 4 and 6) is the primary rigour mechanism.

**Honesty.** Are limitations stated (proxy attributes, *n* = 1 latency, non-Norwegian data)? A consolidated limitations discussion appears in Section 7.5 (with methods detail in Section 4.5); earlier chapters preview scope without replacing that discussion.

## 3.4 Iteration, versioning, and the DSR cycle

DSR is iterative in practice even when the thesis presents a linear chapter order. In this project, iteration occurred through git history: threshold changes, gate scripts, workflow tuning, and documentation updates. The submitted thesis should reference the commit embedded in `experiment_comparison.json` as the frozen evaluation snapshot for Chapter 6, even if the branch moves on afterwards. That convention makes the DSR evaluation auditable without claiming that every experimental branch was kept in the main line of development.

## 3.5 Knowledge contribution statement (DSR)

Following Hevner *et al.* (2004), this thesis contributes (i) a construct—Governance-as-Code as operationalised here—(ii) an instantiation—the public repository with gates and workflows—and (iii) methodological elements—the comparison protocol and Sub-RQ2 measurement definition. The evaluation produces design knowledge about when governed and standard profiles coincide on accuracy metrics under baseline policy and when a fairness gate blocks under tightened policy, plus a descriptive latency observation for human approval in CI.

## 3.6 Relationship to behavioural and organisational theories (light touch)

Some theses connect AI governance to organisational behaviour theories (e.g. routines, institutional isomorphism). This thesis does not develop a full organisational theory chapter; it provides an artefact that could later be studied qualitatively in banks. That boundary keeps the empirical work focused and testable.

## 3.7 Evaluation limitations inherent to DSR here

DSR evaluation in this thesis is functional and artefact-centric. It does not establish statistical generalisability to all credit models or causal effects of GaC on organisation-level outcomes. Those would require different methods (field studies, econometrics, etc.).

---

# 4. Methodology

## 4.1 Research design

The study follows a **Design Science Research** path: **build** the **GaC** **instantiation**, **evaluate** it under **controlled** conditions, and **demonstrate** **policy-as-code** behaviour when a **fairness** threshold is **tightened**. **Sub-RQ1** combines (i) a **standard vs governed** comparison with **fixed** seed and **documented** data lineage, and (ii) an **archived** **gate failure** JSON from a **threshold** demo. **Sub-RQ2** uses a **single** **illustrative** GitHub Actions workflow run with **committed** latency JSON and a **public** workflow URL—**not** a **sample** of production approvals.

### 4.1.1 Evaluation stance

The evaluation is **functional** and **reproducible** rather than **statistical** in the sense of **many** independent draws from a **production** population. **Generalisation** claims are **limited** to the **artifact** behaviour and the **dataset** used; **external validity** to **Norwegian** credit institutions is **not** asserted.

### 4.1.2 What counts as “success” for Sub-RQ1

**Success** for Sub-RQ1 is **not** “the governed model is better on accuracy”; it is **(a)** **transparent** comparison under **fixed** controls, and **(b)** a **demonstrated** **blocking** path when **policy** is **stricter** than observed **EOD** on the validation split. **Success** for **Sub-RQ2** is a **clear** **definition** of **latency** and a **citable** **observation** from **automation** to **approval job start**.

## 4.2 Data

**Primary source:** UCI Machine Learning Repository, **South German Credit (UPDATE)** (`SouthGermanCredit.asc`), dataset ID 573. **Provenance** string logged to MLflow: `uci-asc:SouthGermanCredit.asc`. If local raw files are missing, the training script may fall back to OpenML `credit-g`; the thesis reports the provenance recorded for the runs cited here.

**Binding for Chapter 6 (P3):** Tables and metrics for the **standard vs governed** comparison **must** match **`metrics/experiment_comparison.json`**—including its **`git_commit`**, **`data_provenance`**, and embedded metrics. For the committed file cited in Section 6.1, lineage is **`uci-asc:SouthGermanCredit.asc`** (aligned with CI and `scripts/compare_profiles.py`). A different local raw path does not override the cited JSON unless you regenerate and recommit that file.

**Split:** 75% train / 25% validation, `random_state=42`, stratified on the target. **Sensitive column** for fairness: `famges` (fallback `personal_status` if absent).

### 4.2.1 Preprocessing and model class

The **training** pipeline uses **scikit-learn** with **logistic regression** (details in repository `train.py` and `params.yaml`). The thesis **does not** tune **extensively** for maximum **Kaggle** performance; the **baseline** is **stable** and **reproducible** rather than **state-of-the-art** on this dataset. **Stability** supports **fair** comparison between **profiles** (same model family, same split).

### 4.2.2 Why not Norwegian bank data

Proprietary credit data is not used for ethical, access, and scope reasons. The public dataset limits claims about national practice but enables open replication and examiner access to the same metrics files.

### 4.2.3 Dataset description (South German Credit UPDATE)

The **South German Credit (UPDATE)** dataset (UCI ID 573; CC BY 4.0) contains **1000** rows; the target column is **`kredit`** (credit risk outcome). Features describe account behaviour, loan duration, savings, employment, and demographic-style fields. The variable **`famges`** encodes combined personal status and sex-related information; the UCI page documents coding—this thesis uses it **only** as a **sensitive** column for **Fairlearn** **group** metrics, with **proxy** limitations as in Sections 2.1.3 and 4.5.

**Task formulation.** The binary classification task is to predict **credit risk** from applicant and account attributes. **Logistic regression** is chosen for **stability** and **interpretability** baseline rather than maximum benchmark performance. **Preprocessing** (encoding, scaling) follows the repository’s `train.py` and is **held** **constant** across **standard** and **governed** **profiles** for **Sub-RQ1** **fairness**.

**Lineage and replication.** The thesis commits to **`uci-asc:SouthGermanCredit.asc`** (or equivalent) as recorded in `experiment_comparison.json`. OpenML fallback (`credit-g`) may differ slightly in schema handling; the authoritative lineage for Chapter 6 is whatever is embedded in the cited JSON after regeneration.

## 4.3 Profiles

- **Standard:** `PIPELINE_PROFILE=standard` — train only; performance metrics; **no** fairness or SHAP gates in the comparison script path.  
- **Governed:** `PIPELINE_PROFILE=governed` — train, then fairness gate, then SHAP gate.

**Note:** Local `dvc repro` runs all stages after train using `pipeline.profile` from `params.yaml` (default governed); the **standard** baseline for P3 uses the comparison script, not `dvc repro` alone (see project `docs/compare_pipelines.md`).

### 4.3.1 Comparison script vs CI matrix

The **authoritative** **tabular** comparison for the thesis is produced by **`scripts/compare_profiles.py`**, which runs **both** profiles with **consistent** inputs. **CI** (`.github/workflows/ci.yml`) runs **standard** and **governed** in a **matrix**; **either** path can be used to **sanity-check** behaviour, but **Chapter 6** **numbers** are **bound** to committed **`experiment_comparison.json`** (see Section 4.4).

## 4.4 Gate roles and evidence binding

For **Sub-RQ1**, the **fairness** gate (Gate A) carries the **demonstrated blocking** story: the archived threshold-tightening run (`metrics/fairness_gate_subrq1_threshold_demo_fail.json`) records **`gate_passed: false`** when the fairness budget is tighter than the observed equalized-odds difference on the validation split.

The **SHAP** gate (Gate B) **mandates** an explainability artefact (`artifacts/shap_report.md`) and metrics (`metrics/shap_gate.json`). With the baseline **`min_top_mean_abs_shap: 0.0`** in `params.yaml`, Gate B **documents** SHAP-based attribution for the validation set and **passes** under normal runs; it does **not** provide a second independent numeric failure mode in this baseline configuration (raising `min_top_mean_abs_shap` would be required to make SHAP-driven failure likely). Optional **stress** / bias-injection runs target **fairness** outcomes; see `docs/stress_experiment.md`.

**Evidence binding:** Claims in Chapter 6 that rest on the profile comparison **must** align with **`metrics/experiment_comparison.json`** (Sections 4.2 and 4.4). On-disk `metrics/fairness_gate.json` from a **later** local run may differ; the **thesis table** is tied to the embedded objects inside `experiment_comparison.json` unless you state otherwise.

### 4.4.1 Sub-RQ2: epoch fields and interpretation

`human_oversight_latency.json` stores Unix epoch timestamps for gates completed and approval job start; the difference in seconds is Sub-RQ2’s metric. Clock skew, runner queueing, and GitHub Environment approval wait are included in the wall-clock interval as observed—the thesis does not decompose these components for *n* = 1.

## 4.5 Ethics and limitations (methods)

- **Data:** Public anonymised records; **proxy** sensitive attributes—no claim of representing protected characteristics directly.  
- **Legal:** Appendix B maps themes to controls; **thesis must cite EUR-Lex** for Articles.  
- **Sub-RQ1:** Controlled comparison + blocking demo—not sampled production approval rates.  
- **Sub-RQ2:** CI proxy; latency includes GitHub Environment approval wait when enabled—not bank SLA or eID signing.  
- **Deployment:** Research instantiation; “release” is illustrative.

## 4.6 Validity, reliability, and threats

### 4.6.1 Internal validity

Fixed `random_state` and stratified splitting reduce random sources of variation between standard and governed for the same codebase. Gate order could affect wall time; the Sub-RQ1 accuracy comparison is not affected by gate timing because predictions come from the same trained model on the fixed split.

### 4.6.2 Construct validity

Operational non-compliance is defined as gate failure; that construct is not legal non-compliance. Human oversight is proxied by GitHub Environment approval before a job—not human review of each credit decision.

### 4.6.3 External validity

Findings do not generalise to all credit models or banks. Dataset country and era differ from contemporary Norwegian applications.

### 4.6.4 Reliability of evidence

Committed JSON and git hashes support reproducibility checks. Regenerating `experiment_comparison.json` after code changes is required before locking Chapter 6.

## 4.7 Replication and reproducibility

To replicate the P3 comparison, run `python scripts/compare_profiles.py` from the repository root with consistent `params.yaml` and data files. CI logs and MLflow tags provide additional audit trails. Docker serving is optional for Sub-RQ1/Sub-RQ2 evidence but supports instantiation claims (Chapter 5).

## 4.8 Replication procedure (step-by-step)

This section expands Section 4.7 into a **procedural** narrative examiners can follow without reading every script. It is **not** a substitute for repository `README.md` files; it explains **why** each step matters for **evidence binding**.

**Environment.** Use Python 3.12 to match CI unless you explicitly document a different interpreter. Create a virtual environment, install dependencies from the repository’s requirements files as described in the root `README.md`, and verify that raw data paths in `params.yaml` resolve (`data.raw_csv` / `data.raw_asc`). Missing data triggers fallback behaviour in training code; the thesis must report the **provenance** string embedded in the metrics JSON you cite, not an informal local path.

**Train and gates (governed path).** Running governed training executes model fitting followed by fairness and SHAP gates when invoked through the governed profile. The fairness gate writes `metrics/fairness_gate.json` for that run; SHAP writes `artifacts/shap_report.md` and `metrics/shap_gate.json`. These on-disk files can change when you repeat experiments; Chapter 6’s **comparison table** is tied to **`metrics/experiment_comparison.json`**, which embeds the metrics objects used for the thesis snapshot.

**Standard vs governed comparison.** Run `python scripts/compare_profiles.py` after ensuring a clean git state for the commit you want to cite. The script runs both profiles under the same controls and writes `metrics/experiment_comparison.json` with timestamps and embedded metrics. Open the JSON and confirm `git_commit`, `data_provenance`, wall times, accuracy, ROC-AUC, fairness gate summary, and SHAP gate summary. Paste or transcribe **only** from this file into Chapter 6 to avoid drift.

**Threshold demo.** To reproduce the archived failure, tighten `gates.fairness.max_equalized_odds_difference` below the observed absolute EOD (~0.617 for the cited configuration), run the fairness gate, and confirm `gate_passed: false`. Save outputs as a separate committed file (as in `metrics/fairness_gate_subrq1_threshold_demo_fail.json`) or document the run in an appendix. Restore the baseline threshold (0.70) for the main narrative.

**Sub-RQ2.** Trigger `governed_deploy.yml` under the same Environment protection rules you intend to describe. After the run completes, confirm `metrics/human_oversight_latency.json` contains coherent epoch fields and seconds, and capture the workflow URL. Update Chapter 6 and Appendix C together.

**Serving (optional).** Build the Docker image, run `scripts/smoke_serving.py` or manual checks against `/health` and `/predict`, and record versions. Serving supports instantiation claims but is not required for Sub-RQ1/Sub-RQ2 numbers.

**Verification gate.** Before thesis submission, run `python scripts/verify_thesis_metrics.py` and keep the console output or logs as an internal checklist. If verification fails, reconcile JSON and text before printing the PDF.

## 4.9 Ethics checklist (expanded)

Beyond Section 4.5, the author should explicitly confirm: (i) the public dataset licence permits thesis use (UCI CC BY 4.0 for dataset 573—cite per institution rules); (ii) sensitive-attribute proxy use is disclosed and interpreted cautiously; (iii) no attempt is made to re-identify individuals; (iv) repository URLs and workflow URLs are stable enough for examination (use tagged releases if required). If human subjects research is not conducted, state that clearly in the faculty declaration.

## 4.10 Methodological alternatives considered

A different thesis could have chosen (a) a purely legal analysis without code, (b) a field study with interviews in banks, or (c) a benchmark competition on accuracy alone. Option (a) was rejected because the programme and RQ call for an artefact and instantiation. Option (b) was rejected due to access and time constraints and because the stated RQs are engineering-centric. Option (c) was rejected because accuracy-only evaluation does not address governance gates or human oversight latency as defined here.

Within DSR, the chosen design emphasises reproducible artefacts over broad statistical sampling. That is a deliberate trade-off: strong internal validity for pipeline behaviour, weaker claims about industry populations.

## 4.11 Data protection note (public data; non-exhaustive)

Even public datasets can contain information about people at the row level. The GDPR may still apply when such data are processed in the EU/EEA depending on context and role. This thesis uses the data for research demonstration and does not ingest Norwegian customers’ data. A Data Protection Impact Assessment or faculty ethics form, if required, is completed outside this manuscript (`docs/thesis/README.md`).

## 4.12 Traceability matrix (method → chapter)

| Method element | Primary chapter |
| -------------- | ---------------- |
| Literature gap and fairness foundations | 2 |
| DSR + GaC construct | 3 |
| Data, profiles, validity, replication | 4 |
| Stack, gates, CI, serving | 5 |
| Committed metrics and demo | 6 |
| Interpretation, limits, future work | 7 |

## 4.13 Software engineering quality and the thesis artefact

Software quality attributes—maintainability, testability, security—matter for research code when that code is the evidence base for claims. The repository includes unit or integration tests as appropriate for the project (see `tests/` and CI configuration). The thesis does not evaluate test coverage percentages as a research outcome; it uses CI pass/fail as a sanity check that refactors do not silently break gates.

## 4.14 Threats to construct validity (expanded)

Construct validity asks whether the metrics measure what the RQs claim. “Operational non-compliance” is defined as gate failure; that is narrow by design. If a stakeholder equates it with legal non-compliance, the construct is misunderstood. The thesis mitigates this by defining terms in Chapters 1 and 4 and consolidating limitations in Section 7.5.

## 4.15 Role of the author and tool assistance (transparency)

The author implemented the repository and wrote the thesis text with editor and AI assistance as permitted by the faculty. Claims about metrics are grounded in committed JSON rather than generated prose alone. Front-matter disclosure wording, if required, follows examination rules (`docs/thesis/README.md`).

## 4.16 Measurement error and floating-point considerations

Metrics such as equalized odds difference are computed in floating-point arithmetic. Tiny differences can appear across machines or library versions. The thesis mitigates ambiguity by committing structured JSON outputs from the same code path used for the thesis tables. If a reviewer observes small numeric drift when re-running locally, the first step is to align library versions and data lineage with the cited commit.

## 4.17 Logging, audit trails, and non-repudiation (technical)

MLflow tags and git commit hashes support technical traceability between reported numbers and code state. They do not provide legal non-repudiation of human approvals in the sense of qualified electronic signatures. Gate C timestamps in JSON are workflow telemetry for research demonstration.

## 4.18 Scope of inference: what Sub-RQ1 does and does not prove

Sub-RQ1 supports controlled comparison and existence of a blocking path under tightened policy. It does not prove that the governed profile reduces harm in the real world, nor that the chosen EOD threshold is normatively correct. Those questions require domain and legal input beyond this thesis.

## 4.19 Pre-registration and hindsight bias (reflection)

This thesis was developed iteratively in a public repository. Full pre-registration of hypotheses was not the governing frame; DSR artefact construction was. Readers should still watch for hindsight bias in narrative: the final RQs and definitions must match what the evidence actually supports. The use of committed JSON reduces ambiguity about what was observed.

## 4.20 Ablation mindset: what each gate contributes

An ablation mindset asks what breaks if a component is removed. Without Gate A, the thesis loses the primary blocking story for fairness policy. Without Gate B, the governed path still exists but lacks a mandated SHAP report artefact under baseline settings. Without Gate C, Sub-RQ2 evidence disappears, though Sub-RQ1 can remain. This clarifies which parts of the instantiation support which sub-questions.

## 4.21 Data versioning and DVC in plain language

DVC tracks data dependencies as part of the pipeline definition. For this thesis, DVC supports the story that training and gates run against known inputs when stages are reproduced correctly. If DVC is not used for a given local workflow, the author must still ensure the thesis-cited JSON reflects the intended data state.

## 4.22 Ethics of stress experiments (pointer)

Optional stress experiments manipulate training data to induce gate failures. Use them only with clear documentation and supervisor agreement. The goal is to demonstrate gate sensitivity, not to simulate harm toward real groups.

---

# 5. Instantiation

This chapter describes how the GaC construct is realised in software: training and gates, experiment tracking, CI/CD, human approval, and an illustrative serving layer. Detail is sufficient for replication together with the repository; line-by-line code walkthrough is left to source files and linked docs where appropriate.

## 5.1 Stack

- **Python 3.12** (CI); scikit-learn logistic regression; **MLflow** tracking (`sqlite:///./mlflow.db`); **DVC** for pipeline stages; **Fairlearn** (equalized odds difference); **SHAP** (mean |SHAP| on validation).  
- **CI:** `.github/workflows/ci.yml` matrix **standard** vs **governed**.  
- **Gate C:** `.github/workflows/governed_deploy.yml`; Environment **`model-governance`**; latency written to `metrics/human_oversight_latency.json`.

### 5.1.1 MLflow and experiment tracking

MLflow stores run metadata, metrics, and tags—including short git commit hash, `params.yaml` digest, and `dvc.lock` digest—supporting traceability between reported numbers and code/data state. The SQLite backend is adequate for research-scale work; production deployments would typically use managed tracking and access controls.

### 5.1.2 DVC and pipeline stages

DVC orchestrates stages such as data fetch, train, and downstream steps according to `params.yaml`. Reproducibility relies on locked dependencies in `dvc.lock` and explicit parameters.

## 5.2 Gates


| Gate              | Script                       | Pass criterion (baseline)                                                                                                                                   |
| ----------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A Fairness        | `src/gate_fairness.py`       | `abs(equalized_odds_difference) ≤ max_equalized_odds_difference` (default **0.70**)                                                                         |
| B SHAP            | `src/gate_shap.py`           | Top feature mean |SHAP| ≥ `min_top_mean_abs_shap` from `params.yaml` (baseline **0.0**); writes `artifacts/shap_report.md`, `metrics/shap_gate.json` (§4.4) |
| C Human oversight | GitHub Actions + Environment | Manual approval before second job; latency JSON                                                                                                             |


Gate **A** is the primary **policy-as-code** lever for **blocking** demonstrations in this thesis (threshold demo; optional stress). Gate **B** enforces **presence** of a SHAP summary under the baseline threshold; Chapter 4.4 states how this relates to Sub-RQ1 evidence.

### 5.2.1 Gate A — fairness script interface

`src/gate_fairness.py` reads validation predictions and computes Fairlearn metrics relative to the sensitive column. On failure it writes or updates `metrics/fairness_gate.json` with `gate_passed: false` when the absolute EOD exceeds the configured maximum.

### 5.2.2 Gate B — SHAP artefact

`src/gate_shap.py` produces `artifacts/shap_report.md` and `metrics/shap_gate.json`. Chapter 6 reports the top feature’s mean SHAP where embedded in `metrics/experiment_comparison.json`.

### 5.2.3 Gate C — human approval workflow

`.github/workflows/governed_deploy.yml` models a release path where automated jobs finish before a manual approval gate (GitHub Environment `model-governance`) allows a subsequent job to run. Latency is written to `metrics/human_oversight_latency.json` for Sub-RQ2.

**Figure 1:** Standard vs governed GaC paths (schematic). **Source file:** `docs/figures/Fig01_gac_architecture.mmd` (export to PNG/SVG for Word). **Limitation:** diagram, not a bank network map.

## 5.3 Traceability

Each training run logs **git commit** (short), **params.yaml** SHA-16, and **dvc.lock** SHA-16 to MLflow tags and `metrics/train_metrics.json`, supporting audit-style replay.

### 5.3.1 Feature schema for inference

Training emits `artifacts/feature_schema.json` so the serving API can validate incoming feature vectors against the same contract as offline training—a minimal form of technical documentation aligned with transparency themes, without claiming full Article 13 compliance.

## 5.4 MLOps scoring API (illustrative)

The repository **includes** a **containerised** FastAPI service (`serving/`, Docker) exposing **`/health`** (liveness), **`/ready`** (readiness), **`/version`**, **`/metrics`** (minimal process stats), and **`/predict`** for the **same** sklearn pipeline as offline training; training also emits **`artifacts/feature_schema.json`** for a documented inference column contract. Continuous integration **builds** a Docker image after training, uploads a **tarball** artefact for every run, and **on** `push` **and** `workflow_dispatch` (not **`pull_request`**) also pushes the image to **GitHub Container Registry (GHCR)**—still **not** a production release or bank-grade operation. Optional controls (**API key** on predict, **request body limit**, **per-IP rate limit**, **structured access logs**) are **illustrative** operations hygiene—not bank security or compliance tooling. This supports **Primary RQ** “instantiation” and **Discussion** (traceable deployment-shaped artefact) but is **not** claimed as regulated production deployment: no service-level guarantees, no integration with core banking systems, and the model artefact remains **research-grade** on public data. Sub-RQ1 and Sub-RQ2 evidence remain tied to committed metrics and CI unless extended by explicit new experiments.

### 5.4.1 Relationship to Sub-RQ evidence

Sub-RQ1 and Sub-RQ2 do not require HTTP serving; they are grounded in training/gates and workflow latency JSON. Serving demonstrates end-to-end MLOps shape (train → artefact → container → inference) for the Primary RQ instantiation narrative.

## 5.5 Continuous integration and the governed release path

**CI training matrix.** The workflow `.github/workflows/ci.yml` runs standard and governed profiles so that regressions in gates surface as failed jobs on pull requests or main, depending on repository settings. This supports the Primary RQ claim that governance can live in the same automation surface as tests.

**Governed deploy and Gate C.** The workflow `.github/workflows/governed_deploy.yml` separates automated steps from a human-gated second phase. GitHub Environments can require named reviewers; until approval, the approval job does not start, and Sub-RQ2 measures elapsed time from completion of automated gates to the start of that job. This operationalises “human in the loop before release” for a DSR artefact; real banks typically use different tooling and controls.

**Docker and GHCR.** Training outputs feed a Docker build in CI; images may be pushed to GHCR on selected events. That demonstrates a traceable path from commit to runnable service, not a regulated production deployment.

## 5.6 Narrative walkthrough: one governed run (end-to-end)

The following walkthrough abstracts the repository layout into a single story from clone to optional HTTP inference. It is intended for readers who do not yet know where each script lives.

**Clone and environment.** A researcher clones the repository, creates a Python environment, and installs dependencies. Raw data are placed under `data/raw/` as documented in `params.yaml` (`south_german_credit.csv` or `SouthGermanCredit.asc`). The training entry point reads configuration, loads data, applies preprocessing consistent with the sklearn pipeline, and fits logistic regression.

**Training outputs.** The run writes `artifacts/model.joblib` (or equivalent path per repository), `metrics/train_metrics.json`, and MLflow records with tags for git commit and configuration digests. These outputs are the **foundation** **for** **both** **profiles.**

**Governed path only.** After training, `gate_fairness.py` evaluates validation predictions and writes `metrics/fairness_gate.json`. If EOD exceeds the configured maximum, the gate fails. Next, `gate_shap.py` computes SHAP values (with background sampling parameters from `params.yaml`), writes `artifacts/shap_report.md`, and writes `metrics/shap_gate.json`. If SHAP thresholds were raised above observed values, this gate could fail independently; under baseline `min_top_mean_abs_shap: 0.0`, it typically passes while still producing documentation.

**Comparison packaging.** `scripts/compare_profiles.py` runs standard and governed sequences and embeds the resulting metrics into `metrics/experiment_comparison.json`. That file becomes the single source of truth for Chapter 6 tables.

**CI analogue.** On GitHub, `ci.yml` runs the same logical profiles in a matrix. Failures appear as red checks, which is how policy breaches become visible to teams using pull requests.

**Gate C analogue.** A maintainer triggers `governed_deploy.yml`. Automated jobs complete; an Environment approval step may block a downstream job until a reviewer approves. The workflow writes latency JSON capturing seconds between gate completion and approval job start.

**Serving analogue.** Optionally, Docker builds an image; locally, `docker compose up` can expose `/predict`. This demonstrates inference contract enforcement via `feature_schema.json`, closing the loop from training to a deployment-shaped service.

## 5.7 Repository map (components and responsibilities)

The following inventory supports examiners and future maintainers. It is descriptive rather than a line-by-line manual.

**Root.** `params.yaml` centralises random seed, pipeline profile, gate thresholds, and MLflow settings. `dvc.yaml` and `dvc.lock` define pipeline stages and locked dependencies. `requirements*.txt` files split training, serving, and development dependencies. `Dockerfile` and `docker-compose.yml` support container builds for the scoring service.

**`src/`.** Training and gate logic live here: model training, fairness evaluation, SHAP generation, and utilities shared across stages. This separation keeps governance checks importable and testable independently of CLI entrypoints.

**`scripts/`.** Operational scripts include `compare_profiles.py` for the P3 comparison and `verify_thesis_metrics.py` for thesis/JSON consistency checks. Helper scripts may exist for smoke tests or maintenance; consult `README.md` for the authoritative list.

**`metrics/`.** Committed JSON outputs hold evidence for the thesis. `experiment_comparison.json` is the primary Sub-RQ1 table source. `fairness_gate_subrq1_threshold_demo_fail.json` archives the threshold demo. `human_oversight_latency.json` stores Sub-RQ2 timing. Other `fairness_gate.json` files may reflect local runs and should not override the committed comparison JSON unless regenerated intentionally.

**`artifacts/`.** Model binaries, SHAP reports, and schema files appear here after training. These files may be gitignored in part; the thesis emphasises **committed** metrics and reports referenced in Chapter 6.

**`.github/workflows/`.** YAML workflows define CI training matrices, governed deploy with Environment gates, and Docker build/push behaviour. Workflow design is part of the GaC instantiation: it determines when automation runs and who may approve.

**`docs/`.** Project documentation includes data provenance, stress experiment instructions, human oversight metric definitions, compliance matrix source, and thesis manuscript files. Treat `docs/` as the narrative complement to executable code.

**`serving/`.** FastAPI application code implements health endpoints and prediction for the trained sklearn pipeline. Optional security controls are documented in deployment docs.

**`tests/`.** Automated tests guard refactors. CI failure should block merges when tests are wired to required checks.

**`data/raw/`.** Placeholder paths for raw datasets; actual bytes may not ship in git for size reasons. The thesis binds to provenance strings recorded in metrics JSON.

This map completes the Primary RQ instantiation story at repository level: policy parameters, executable checks, automation, and traceable outputs coexist in one versioned workspace.

## 5.8 Troubleshooting and operational notes (technical)

Researchers often hit predictable issues when replicating ML repositories. Missing raw files may trigger OpenML fallback; always check `data_provenance` in the emitted metrics and align it with the thesis claim. Dependency conflicts can change metric values slightly; pin versions as in CI or use the same lock files where provided.

Fairness gate failures may reflect true policy breach or a bug in preprocessing (e.g. wrong sensitive column encoding). Inspect `metrics/fairness_gate.json` and validation prediction outputs as logged. SHAP gate failures under non-baseline thresholds should be expected if `min_top_mean_abs_shap` is set too high for the model and data.

GitHub Actions failures may stem from secrets missing for container registry push or from Environment protection not configured. For Sub-RQ2, ensure the workflow actually writes `human_oversight_latency.json` as implemented in the repository at the cited commit.

Docker issues often relate to port binding or missing `artifacts/` after training. Run training before serving or mount artefacts as documented.

These operational notes do not change the scientific claims; they help examiners and students reproduce the same evidence path that Chapter 6 relies on.

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

### 6.1.1 Interpretation

Numerical equality of accuracy and ROC-AUC under baseline policy does not imply that governance is costless in general. For this model family, split, and threshold configuration, the fairness constraint as implemented does not change the reported ranking metrics relative to the standard path. The governed path incurs additional wall time (Table 2) and produces additional artefacts (fairness and SHAP outputs) that support audit-style review. From a Sub-RQ1 standpoint, the controlled comparison shows how the profiles differ under fixed controls: they differ in runtime and in gate outputs, not in the reported accuracy metrics for this run.

## 6.2 Policy tightening — gate blocks (Sub-RQ1 demonstration)

When `max_equalized_odds_difference` was tightened from **0.70** to **0.55**, the same model class produced **abs EOD ≈ 0.617**, exceeding **0.55**. The fairness gate **failed** (`gate_passed: false`). The archived metric file is `metrics/fairness_gate_subrq1_threshold_demo_fail.json`. The threshold was **reverted** to **0.70** for the baseline narrative.

**Table 3 — Fairness gate: baseline vs tightened policy**


| Setting         | max EOD allowed | abs EOD (val) | gate_passed |
| --------------- | --------------- | ------------- | ----------- |
| Baseline        | 0.70            | 0.617         | true        |
| Demo (archived) | 0.55            | 0.617         | **false**   |


This demonstrates **executable** policy: **identical** code and data, **stricter** threshold, **blocked** governed path.

## 6.3 Human-oversight latency (Sub-RQ2)

From **`metrics/human_oversight_latency.json`** (workflow sample):

- **`human_oversight_latency_seconds`:** 7  
- **`gates_completed_epoch`** / **`approval_epoch`:** Unix epoch timestamps in the committed file (difference **7 s** for this run).  
- **Workflow run:** `https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560`

This measures **GitHub-mediated** delay (gates complete → approval job start), including Environment approval wait when protection is enabled—not end-to-end bank processing.

## 6.4 Synthesis: what the results jointly show

Read together, Tables 2–3 and the Sub-RQ2 bullet do not prove that GaC is always worth deploying in banks. They show a coherent story for this artefact: under fixed controls, governance can be added without changing the reported accuracy metrics for the baseline policy, while still enabling a hard stop when policy tightens. The 7 s latency sample shows that human gates in automation have measurable wall-clock cost even when the “work” of approval is a single click in a web UI. That triangulation supports the Primary RQ at engineering level and supports Sub-RQ1 and Sub-RQ2 within their definitions.

## 6.5 Interpreting the fairness numbers (without over-claiming)

The absolute EOD ≈ 0.617 on the validation split is a single scalar summary of group disparity under Fairlearn’s definition and the chosen sensitive column. It does not imply that 0.617 is “too high” or “acceptable” in a legal sense; it only shows that the baseline budget (0.70) permits the governed path to pass, while a stricter budget (0.55) fails for the same observed value. That contrast is the Sub-RQ1 policy-as-code demonstration in its minimal form.

## 6.6 Cost and latency: what the wall-time difference means

The governed profile wall time (~20.9 s) exceeds the standard profile (~6.7 s) in the cited JSON. The difference reflects additional computation (fairness and SHAP) and I/O for reports. This is not a claim about production serving latency or customer-facing response times; it is a developer pipeline measurement on one machine configuration. Readers should expect CI times to vary with hardware and caching.

## 6.7 Stability of predictions under baseline policy

Because accuracy and ROC-AUC match between profiles under the baseline fairness budget on the fixed split, the predictions on the validation set are consistent with identical model behaviour given the same trained coefficients. The thesis does not claim that gates never change training dynamics in general; it reports what the embedded metrics show for the cited run.

## 6.8 Reporting precision

Reported metrics use the precision present in `experiment_comparison.json`. Rounding in Word tables should not introduce drift relative to JSON. For examiners, the JSON file is authoritative.

## 6.9 Linking results back to Sub-RQ wording

Table 2 addresses whether the governed profile differs under fixed controls: it differs in runtime and gate outputs. Table 3 addresses whether stricter policy can block the governed path: yes, for the archived demo. Sub-RQ2 is addressed by the latency bullet and JSON fields. This mapping keeps Chapter 6 aligned with Chapter 1.

---

# 7. Discussion

This chapter moves from direct answers to the research questions, through practice-oriented implications and design principles, into a consolidated limitations statement (Section 7.5) and future work (Section 7.6). Subsequent sections extend the argument to adoption barriers, documentation-only governance, examiner concerns, publication ethics, model risk management, replication, and threats to validity—ending with a concise positioning statement (Sections 7.7–7.40).

## 7.1 Answers to research questions

The primary research question asked how Governance-as-Code can be designed and instantiated as executable controls in CI/CD; this thesis delivered a pipeline with fairness, SHAP, and human-approval gates. Enforcement is operational (gates block or fail the stage); the work does not claim full Act implementation in code.

For Sub-RQ1, under controlled comparison on the fixed split, the standard and governed profiles coincide on accuracy for the baseline configuration; the governed path adds runtime checks and wall-clock cost. The archived threshold demonstration shows the governed path blocks when fairness policy tightens—evidence for policy-as-code rather than principles-only governance.

For Sub-RQ2, the recorded 7 s latency is an illustrative CI sample (n = 1 cited run); it supports discussion of human gate overhead in automation, not banking production SLAs.

Sub-RQ1 and Sub-RQ2 are complementary, not symmetric: Sub-RQ1 carries the main evaluative evidence (controlled comparison plus executable blocking under tightened policy); Sub-RQ2 is a narrow GitHub-mediated operational metric (gates complete → approval job start). That distinction avoids reading Sub-RQ2 as weak evidence or as a claim about production credit SLAs.

## 7.2 Implications for practice (careful)

Organisations adopting high-risk ML for credit scoring face both legal expectations and engineering constraints. GaC does not replace legal counsel or model risk committees; it can narrow the gap between stated policy and what actually runs in pipelines. Teams should treat thresholds as organisational decisions with traceability (version control), not as neutral technical defaults. Where fairness metrics conflict with business objectives, leadership must resolve trade-offs explicitly—the thesis artefact only makes such conflicts visible when they are encoded as gates.

## 7.3 Velocity versus control

MLOps culture often prioritises deployment frequency and short feedback loops. Governance gates introduce latency and can block releases when policy is tightened. The empirical wall-time difference between profiles (Table 2) illustrates that control has a measurable engineering cost even when accuracy is unchanged. Organisations must decide where to place gates (pre-train, post-train, pre-deploy) and how strict to make them; this thesis does not prescribe a single organisation-wide policy.

## 7.4 Design principles

1. **Separation of profiles** — standard vs governed must be **defined** and reproducible.
2. **Evidence binding** — claims attach to JSON, workflows, and commit hashes.
3. **Honest scope** — proxy attributes, CI-only oversight, illustrative deployment.

## 7.5 Limitations

This section consolidates limitations for examination. Section 4.5 gives methods-level ethics and validity detail; Section 1.2–1.3 and Section 1.7 preview scope; Section 7.38 discusses threats to validity in a design-science sense. In short: **dataset** limits generalisation; **legal** claims require EUR-Lex and supervision; **Sub-RQ2** is a **narrow** CI proxy, not banking science.

### 7.5.1 Legal and normative limits

Examiners should not read Gates A/B/C as satisfying specific Articles without a dedicated legal analysis grounded in EUR-Lex. The compliance matrix is a thesis scaffold for traceability between themes and controls, not a regulatory sign-off.

### 7.5.2 Metric and data limits

Equalized odds is one fairness notion among many; the sensitive column is a proxy. Results on German public credit data do not transfer automatically to Norwegian portfolios or to production feature sets.

## 7.6 Future work

Mitigation algorithms (e.g. Fairlearn reductions), additional datasets, organisational study of GaC adoption, and national transposition details for Norway where required by the programme.

### 7.6.1 Extensions suggested by this artefact

Future work could: (i) run multi-seed studies to assess variance of EOD and gate pass rates; (ii) evaluate alternative gates (e.g. calibration, drift detection); (iii) integrate formal model cards or documentation generators in CI; (iv) conduct qualitative interviews with risk and compliance roles on adoption barriers for GaC in banks.

## 7.7 Adoption barriers (organisational, not technical)

Even when tooling exists, **adoption** of automated governance gates in large institutions faces **non-code** barriers. **Ownership** of thresholds (risk, compliance, modelling, IT) must be clear. **Change management** is required when a failing gate blocks a release on a deadline. **False positives** (gates failing for benign reasons such as data drift) can erode trust if not handled with runbooks. **Procurement** and **cloud** policies may restrict GitHub Actions patterns used here. This thesis does **not** evaluate organisational adoption; it provides a **reference** pattern that could inform **pilots**.

## 7.8 Comparison with “documentation-only” governance

Many organisations satisfy internal governance through documents and tick-box approvals outside the CI path. Documentation-only approaches can drift from what runs in production because manual steps decouple from versioned pipelines. GaC does not eliminate documentation; it aligns a subset of controls with automation so that policy changes are diffs and failed gates are visible events. The trade-off is engineering effort and possible friction against velocity.

## 7.9 What examiners might critique—and how this thesis responds

**Critique:** “The dataset is not Norwegian.” **Response:** Scope is explicit; external validity is limited by design. **Critique:** “*n* = 1 latency.” **Response:** Sub-RQ2 is defined as CI proxy measurement, not a statistical estimate of bank SLA. **Critique:** “SHAP is not legal transparency.” **Response:** Gate B is an engineering artefact supporting audit, not a claim about Article 13 compliance. **Critique:** “Equalized odds is not the law.” **Response:** Agreed; the metric is operational non-compliance within the thesis definition.

## 7.10 Transferability to Norwegian financial institutions

Transferability in qualitative research asks whether insights could apply elsewhere. Here, transferability is modest and conditional. The code pattern (gates in CI, MLflow tags, Environment approvals) could be adapted by an institution that uses Git-based MLOps and has defined internal fairness budgets. Tooling, risk culture, and legal interpretation differ by institution. This thesis does not provide a rollout plan or cost-benefit analysis for Norwegian banks.

## 7.11 Normative stance: governance in code without moralising

The thesis avoids claiming that more automation is always “ethical.” Automated gates can encode biased choices as easily as manual ones if thresholds and sensitive attributes are chosen poorly. Governance-as-Code is therefore a mechanism for visibility and enforcement, not a substitute for normative debate inside organisations. That stance aligns with critical literature that warns against “fairness washing” through metrics alone.

## 7.12 Communication of the DSR artefact (open science)

Design Science benefits when artefacts are communicated reproducibly. This repository is public as a reference implementation; the thesis cites a specific commit or release tag at submission so examiners can align text and code. If the repository later changes, a zip or institutional deposit may preserve the submission snapshot as required by the faculty.

## 7.13 Programme-specific extensions (checklist)

Before final submission, the author should confirm with the supervisor whether the programme expects: (i) a longer standalone literature review chapter; (ii) a formal problem formulation using Peffers steps explicitly in the introduction; (iii) a reflection chapter on learning outcomes; (iv) comparison with a commercial governance tool (vendor-neutral description). Those elements belong in the faculty template without breaking evidence binding for Chapter 6 (`docs/thesis/README.md`).

## 7.14 Reflection: what changed between proposal and final artefact

Design Science projects rarely end where they begin. In this work, early emphasis on “compliance” language was narrowed to operational gates and evidence binding to avoid over-claiming legal effects. Sub-RQ2 was specified as a CI latency metric rather than an unmeasurable end-to-end bank SLA. Such refinements are normal in DSR and should be described honestly in the faculty reflection chapter if required.

## 7.15 Pedagogical value for IT and business students

The artefact supports learning outcomes around version control, experiment tracking, fairness tooling, and workflow automation—skills that transfer to industry even when the specific dataset is not Norwegian. The thesis therefore has dual value: scientific (DSR instantiation and evaluation) and educational (professional competence).

## 7.16 Risk: over-automation and deskilling

A counterargument to GaC is that automating checks might deskill risk analysts or replace judgment with green dashboards. The thesis response is institutional: gates surface information and enforce policy thresholds chosen by people; they do not remove the need for credit judgment or legal interpretation outside the pipeline. Gate C explicitly keeps a human approval step in the release path.

## 7.17 Environmental and compute costs of governance gates

Running fairness and SHAP checks on every commit consumes CPU cycles and energy. For small datasets the overhead is modest, but at organisational scale the aggregate cost can be non-trivial. This is a real trade-off: more automated scrutiny implies more computation. The thesis does not perform a carbon accounting; it notes the trade-off so that institutions can weigh environmental cost against risk reduction when scaling GaC patterns.

## 7.18 Maintainability of policy thresholds in version control

Storing thresholds in `params.yaml` makes policy changes reviewable as pull requests. That is an organisational governance benefit: risk committees can participate in threshold changes with the same review culture as code changes. The thesis demonstrates the mechanism at small scale; large institutions would add approval routing and segregation of duties beyond what GitHub Environments show here.

## 7.19 Relationship to “responsible AI” programmes in industry

Many firms publish responsible AI principles. Without engineering hooks, those principles risk becoming static web pages. GaC is one way to connect principles to pipelines. The thesis does not evaluate corporate programmes; it provides a concrete pattern students can discuss in job interviews and case studies.

## 7.20 Failure modes: what happens when gates are wrong

Gates can fail for benign reasons (numerical instability, dependency upgrades) or for substantive reasons (true fairness breach). Operational teams need runbooks to distinguish them. The thesis includes JSON outputs and logs to support debugging, but it does not provide an incident response manual—that would be organisation-specific.

## 7.21 Open science and examiner access

Public repositories enable examiners to verify claims. This aligns with open science norms. If the author later makes the repository private, archive a zip or use institutional storage with access rules and document the snapshot in the thesis.

## 7.22 Mapping thesis chapters to learning outcomes (example)

If the programme lists learning outcomes such as “apply research methods,” “analyse ethical implications,” and “communicate technical results,” Chapters 1–4 map to methods and ethics framing; Chapter 5–6 map to technical results; Chapter 7–8 map to reflection and communication. Adjust the mapping table to your faculty’s exact wording.

## 7.23 Ethics of publication and dual-use concerns

Publishing open-source automation for governance can help students and small teams, but it can also be misread as “compliance in a box.” The thesis repeatedly warns against that misreading. Responsible publication includes clear limitations, honest scope statements, and pointers to legal supervision where organisations would need bespoke analysis.

## 7.24 Collaboration between legal, risk, and engineering roles

GaC only works organisationally when legal and risk stakeholders participate in threshold setting and gate design. Engineering teams should not “set fairness” in isolation. The thesis artefact is a conversation starter: it shows **where** controls can live, not **who** decides what is acceptable.

## 7.25 Sustainability and CI frequency

Running heavy gates on every push may be unnecessary for large training jobs. Organisations might use scheduled nightly runs for expensive checks and lighter checks on each commit. The thesis uses modest workloads; scaling up requires policy and cost decisions.

## 7.26 What a bank would add next (non-exhaustive)

A production bank would integrate identity management, secrets management, change records, penetration testing, and alignment with internal model inventory systems. The thesis provides a reference pattern, not a checklist for supervisory approval.

## 7.27 Examiner perspective: what to look for in the repository

Examiners should verify that Chapter 6 numbers match `metrics/experiment_comparison.json`, that the threshold demo JSON exists, and that workflow URLs resolve. They should also confirm that legal claims are carefully scoped and that EUR-Lex citations appear in the PDF for quoted Articles.

## 7.28 Final positioning statement

This thesis is best understood as a Design Science contribution in information systems and software engineering for regulated ML: a GaC instantiation with bounded evaluation evidence and explicit limitations on law and generalisation.

## 7.29 Synthesis of the programme reading list (illustrative)

Many MSc programmes publish a reading list spanning ethics, methods, and domain applications. This subsection cross-walks the present work to such a list without duplicating full book reviews. Mehrabi *et al.* (2021) survey bias and fairness definitions; this thesis operationalises one metric (equalized odds) in code and shows how a threshold change flips a gate outcome. Sculley *et al.* (2015) and follow-on work on production ML debt motivate why pipelines need tests beyond accuracy; the thesis adds gates as a specific class of tests tied to governance. Hevner *et al.* (2004) and Peffers *et al.* (2007) ground DSR; Chapters 3–4 map the artefact and evaluation to those expectations. Regulation (EU) 2024/1689 is the legal anchor; the thesis cites it for framing and does not substitute repository behaviour for legal analysis.

Required programme texts should appear with short notes each (what was taken from the source and where it appears in the thesis). Optional extensions—Nordic public-sector AI ethics relative to high-risk obligations, or business-ethics stakeholder duties—apply only where the programme demands them; guidance sits in `docs/thesis/README.md`.

## 7.30 GDPR, credit decisions, and what this thesis does not do

The General Data Protection Regulation (GDPR) and sector credit rules interact with algorithmic credit scoring in ways that depend on establishment, purpose, and lawful basis. Automated decision-making under Article 22, data subject rights, and profiling rules require legal analysis that varies by Member State implementation and product design. This thesis does **not** implement a GDPR compliance programme: it does not map each processing step to lawful bases, does not assess legitimate interest tests, and does not model data subject access flows.

The narrow engineering point is **separation of concerns**: GaC can enforce **internal** technical policy (fairness thresholds, explainability artefacts, human approval gates) while legal teams determine whether those policies meet regulatory obligations in a given deployment. Mentioning GDPR explicitly in the discussion section signals that the author knows the boundary between ML engineering and legal compliance—reducing examiner anxiety that the thesis conflates them. Any student required to include a **legal chapter** should expand this with supervisor-approved sources and national law; the present text stays intentionally short.

## 7.31 Model risk management (MRM) documents versus executable gates

Banks often maintain model inventories, validation reports, and committee approvals documented in PDFs and workflow tools. That is **documentation governance**: evidence exists, but it may drift from the code that runs in production. Governance-as-code pushes **executable** checks into CI so that certain policy breaches are **blocking** before merge or deploy. The two are complementary: MRM answers “who approved what and when” for supervisors; GaC answers “does this commit pass the same automated checks we defined.”

A bank might require both: a gate for SHAP artefacts **and** a quarterly validation report signed by an independent function. The thesis demonstrates the gate pattern on a public repository; it does not replace the bank’s MRM framework. Examiners from finance backgrounds may ask this question; the answer is that **no** single artefact is sufficient—this thesis contributes one **technical** layer.

## 7.32 Replication checklist for examiners (without running code)

Examiners who do not execute Python can still verify structure: open `params.yaml` and confirm the keys referenced in Chapter 4; open `metrics/experiment_comparison.json` and compare `git_commit` and numeric fields to Chapter 6 tables; open `.github/workflows` and confirm job names align with the narrative in Chapter 5; read `README.md` for the high-level map. That triangulation is enough to detect gross inconsistency. Running `python scripts/verify_thesis_metrics.py` is optional but recommended for authors before lock.

## 7.33 Positioning relative to “AI safety” and “alignment”

Research communities use “AI safety” and “alignment” for catastrophic risk and long-horizon control problems. Credit scoring governance is a **different** problem: near-term harm through discrimination, opacity, or poor oversight, within existing institutions. The thesis avoids importing alignment vocabulary that could confuse readers about scope. Responsible ML, fairness, and human oversight are the appropriate framing here.

## 7.34 Generative AI, drafting assistance, and academic integrity

Editorial and drafting tools may assist spelling, structure, or brainstorming; scientific claims, evaluation numbers, repository contents, and limitations remain the author’s responsibility. Tools cannot substitute for running experiments, committing results, or verifying EU law citations against primary sources. Disclosure requirements for the final PDF belong in front matter with faculty-specified wording (`docs/thesis/README.md`).

Generated text can mis-cite sources or misstate Article numbers. Every legal quotation and empirical figure should be checked against primary sources (`experiment_comparison.json`, EUR-Lex).

## 7.35 Credit risk modelling tradition versus fairness-first pipelines

Traditional credit modelling emphasises calibration, Basel-style capital implications, and long-run portfolio behaviour. Fairness-first ML pipelines emphasise group metrics, explanations, and human checkpoints. Real institutions must reconcile both: a well-calibrated score can still be unfair under a chosen definition; a fair-looking score can be unusable for capital or pricing if calibration fails. The thesis does not resolve that trade-off; it demonstrates **where** technical gates can sit in a CI story so that policy teams and modellers negotiate thresholds with visibility.

Students writing for finance-heavy committees may add one paragraph on **probability of default** calibration and note that the logistic baseline here is a teaching comparator, not a rating system. That signals awareness without expanding scope into banking regulation beyond the AI Act framing.

## 7.36 Reflexivity: positionality of the author

Reflexivity statements describe how the researcher’s background may shape problem framing. A student in Norway may be sensitised to EEA implementation debates and Nordic trust in public institutions; international readers may weigh Silicon Valley MLOps defaults differently. The thesis problem—making governance **legible** in software—reflects a conviction that **operational** artefacts matter for accountability, not only policy PDFs. Acknowledging that position helps examiners interpret why DSR and a public repository were chosen over a purely legal doctrinal thesis.

## 7.37 Closing synthesis: threads for viva discussion

Three threads often arise in vivas for IS/engineering theses: **contribution** (what is new), **evidence** (what was measured), and **limits** (what was not claimed). Contribution here is the GaC pattern instantiated with fairness, explainability, and human-approval gates. Evidence is the matched comparison, the archived gate-failure JSON under tightened policy, and the cited Sub-RQ2 latency sample. Limits include law, data, and production security. If the candidate can navigate those three threads with the repository open, the defence aligns with the manuscript’s own structure.

## 7.38 Threats to validity (design-science lens)

Section 7.5 states scope and limitations; this subsection names validity *types* so examiners see what each empirical claim can and cannot support.

Empirical software and design-science theses benefit from an explicit validity conversation adapted from Hevner *et al.* and from qualitative method traditions, without overstating quantitative rigour. **Construct validity** asks whether the operational measures match the intended concepts. Here, equalized odds approximates one notion of group fairness; SHAP magnitudes approximate “explainability depth” only in a narrow engineering sense; Sub-RQ2 latency approximates “human oversight friction” only as automation-to-approval seconds in one CI configuration. The thesis names those mappings honestly so critique can target the construct choices.

**Internal validity** concerns whether observed differences could stem from confounds. The governed and standard profiles share data, seed, and model family, which controls several confounds; remaining threats include library versions, runner contention, and undocumented environment differences. Committing `git_commit` and workflow URLs partially mitigates “runs that cannot be found again.” **External validity** is limited: German credit rows are not Norwegian applicants; public CI is not a bank data centre; a single latency sample is not a distribution.

**Conclusion validity** (whether statistical conclusions follow) is modest: the thesis does not claim significance tests across many seeds; it reports point estimates and a deliberate threshold manipulation to show gate behaviour. That is appropriate for a DSR demonstration but would be insufficient for a pure ML performance paper—another expected examiner question with a clear answer.

**Reliability** of the pipeline is supported by scripted verification and JSON artefacts; **objectivity** is supported by public code and fixed parameters. Together, the threats-to-validity subsection shows methodological maturity: the author knows what would be required to generalise claims and chose narrower, defensible statements instead.

## 7.39 Documentation debt and living artefacts

Production systems accumulate documentation debt when README files, architecture diagrams, and runbooks diverge from the behaviour of deployed services. Governance-as-code reduces **some** of that drift by binding policy to executable checks, but it introduces its own debt: thresholds linger in YAML while organisational policy moves in meetings; workflow comments rot when job graphs change; SHAP summaries become misleading if features change without regenerating reports. The thesis mitigates documentation debt rhetorically by versioning parameters, storing metrics as JSON with lineage, and recommending a tagged release for examination.

A practical takeaway for students is to schedule **periodic** regeneration of explainability artefacts and fairness reports as part of CI—not only on pull requests—so that “green” does not silently age into “wrong but passing.” That suggestion exceeds what the reference repository implements fully; it is future work aligned with MLOps maturity thinking. Examiners may ask whether GaC increases or decreases total documentation burden; the balanced answer is that it **shifts** effort from late manual review to upfront specification of tests and artefacts, which pays off when teams scale but requires discipline to maintain.

## 7.40 One-sentence takeaway for policy and engineering audiences

For **policymakers**, the thesis illustrates that high-level duties around risk management and oversight can be **reflected** in technical workflows—but only where legal concepts have been translated into measurable checks by accountable institutions. For **engineers**, it shows that such translation is feasible in CI without pretending that code exhausts compliance. That single bridge sentence often helps mixed examination committees align on what was demonstrated.

The same idea supports curriculum design: courses that separate “ethics week” from “deployment week” under-teach how values become parameters and tests. A module on governance-as-code does not replace law or philosophy, but it connects them to the artefacts graduates ship. This thesis is one worked example at MSc depth. Word-count rules for appendices and references are an examination-office matter (`docs/thesis/README.md`).

---

# 8. Conclusion

This thesis presented a Governance-as-Code (GaC) MLOps instantiation for high-risk credit scoring under the EU AI Act framing, with fairness, explainability, and human-oversight gates in CI/CD. The primary research question asked how GaC can be designed and instantiated as executable controls; the work does not claim full Act implementation in code. On Sub-RQ1, the standard and governed profiles matched on accuracy and ROC-AUC under the baseline fairness budget, while a tightened fairness threshold produced a documented gate failure in archived JSON. On Sub-RQ2, one cited GitHub Actions run recorded 7 seconds from completion of automated gates to start of the approval job. The contributions are the construct and reference repository, the bounded empirical evidence, and the design principles developed in the Discussion—not a claim that a single repository satisfies the Regulation as a legal matter.

## 8.1 Summary of contributions

The first contribution is construct and instantiation: a reference repository where governance expectations materialise as versioned gates and workflows. The second is empirical evidence within declared scope: a controlled comparison, a threshold demo with archived JSON, and a cited latency sample. The third is design knowledge: principles for separating profiles, binding claims to artefacts, and stating limits honestly.

## 8.2 Closing remark

Regulated machine learning will continue to require both law and engineering. This thesis shows one engineering pattern—Governance-as-Code in CI/CD—that can make policy visible and enforceable at the level of pipelines, without confusing that achievement with legal compliance or with industry adoption.

## 8.3 Recommendations for maintaining evidence alignment

After submission, any change to data, gates, or `params.yaml` should trigger regeneration of `metrics/experiment_comparison.json`, re-running `python scripts/verify_thesis_metrics.py`, and updating Chapter 6 before a new PDF is printed. Derivative projects that fork this repository should freeze a tag, write original introduction and reflection chapters, and expand the literature in their own voice; a checklist appears in `docs/thesis/README.md`.

## 8.4 Implications for supervisors and examination boards

This thesis is best evaluated as a Design Science artefact with bounded empirical claims. Strong assessment typically rewards clear evidence binding, honest limitations, and a coherent line from research questions to repository artefacts. Risk increases when legal compliance is overstated or when public benchmark results are read as evidence about Norwegian banking practice.

## 8.5 What success looks like for the author

Success is not “the model scores high.” Success is a defensible thesis that shows (i) a working GaC instantiation, (ii) reproducible metrics and a demonstrated gate failure under tightened policy, (iii) a clearly defined Sub-RQ2 measurement, and (iv) consistent scope language throughout.

## 8.6 Closing the loop: from thesis submission to future maintenance

After submission, the repository may continue to evolve. Archive the exact commit used for the PDF. If you extend the work, treat new experiments as new evidence: regenerate JSON, update Chapter 6, and avoid retroactive edits to locked results without documentation.

---

# 9. References

*Replace with your faculty’s citation style (APA, Harvard, OSCOLA, etc.). The Regulation must be cited from the official consolidated text.*

European Parliament and Council of the European Union. (2024). Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence and amending Regulations … *Official Journal of the European Union*. Retrieved from EUR-Lex: `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689`

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, 28(1), 75–105.

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, 24(3), 45–77.

Jobin, D., Ienca, M., & Vayena, E. (2019). The global landscape of AI ethics guidelines. *Nature Machine Intelligence*, 1(9), 389–399.

Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). A survey on bias and fairness in machine learning. *ACM Computing Surveys*, 54(6), 115:1–115:35.

Veale, M., & Zuiderveen Borgesius, F. (2021). Demystifying the Draft EU Artificial Intelligence Act. *Computer Law Review International*, 22(4), 97–112.

Bird, S., Dudík, M., Edgar, R., Horn, B., Lutz, R., Milan, V., … Wallach, H. (2020). Fairlearn: A toolkit for assessing and improving fairness in AI (Microsoft). Retrieved from `https://github.com/fairlearn/fairlearn`

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Proceedings of the 31st International Conference on Neural Information Processing Systems* (pp. 4765–4774).

Dua, D., & Graff, C. (2019). UCI Machine Learning Repository. University of California, Irvine, School of Information and Computer Sciences. `https://archive.ics.uci.edu/ml`

Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., … Dennison, D. (2015). Hidden technical debt in machine learning systems. In *Advances in Neural Information Processing Systems* (pp. 2503–2511).

Polyzotis, N., Roy, S., Whang, S. E., & Zinkevich, M. (2017). Data management challenges in production machine learning. In *Proceedings of the 2017 ACM International Conference on Management of Data (SIGMOD)* (pp. 1723–1726).

Breck, E., Cai, E., Nielsen, E., Salib, M., & Sculley, D. (2017). The ML test score: A rubric for ML production readiness and technical debt reduction. In *2017 IEEE International Conference on Big Data (Big Data)* (pp. 1123–1132).

Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence*, 1(5), 206–215.

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., … Gebru, T. (2019). Model cards for model reporting. In *Proceedings of the Conference on Fairness, Accountability, and Transparency* (pp. 220–229).

Stodden, V., & Miguez, S. (2014). Best practices for computational science: Software development and reproducibility in science and statistics. *Journal of Open Research Software*, 2(1), Article e21.

[Add further MLOps or programme-required texts as needed.]

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
  "gates_completed_epoch": 1775564693,
  "approval_epoch": 1775564700,
  "workflow_run_url": "https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560"
}
```

## Appendix D — Reproducibility

Regenerate P3 comparison: `python scripts/compare_profiles.py` from repository root with the same `params.yaml` and data files.

## Appendix E — Submission checklist (Track A)

Tick **before** locking Results and PDF; **every row** must match the **committed** repository at `git commit` embedded in **`metrics/experiment_comparison.json`** (Sections 4.2, 4.4, Appendix C).


| Check                                                                             | Evidence                             |
| --------------------------------------------------------------------------------- | ------------------------------------ |
| `params.yaml` matches cited baseline (fairness threshold, seed, sensitive column) | `params.yaml` in repo                |
| `metrics/experiment_comparison.json` regenerated after any policy/data change     | File + timestamp in JSON             |
| `metrics/human_oversight_latency.json` + workflow URL match Chapter 6             | Same JSON + URL                      |
| Chapter 6 tables match JSON (no hand-typed drift)                                 | Diff vs `compare_profiles.py` output |
| EUR-Lex citations for quoted Articles                                             | Final PDF                            |


## Appendix F — Evidence index and reader’s guide to the repository

This appendix maps **where** evidence for each research question lives in the open repository. It is intended for examiners who clone the code and for the author when locking the final PDF. Word-count rules for appendices are an examination-office matter; if appendices do not count toward the minimum, move essential narrative into Chapters 4–6 and avoid duplicating tables (`docs/thesis/README.md`).

### F.1 Primary RQ (design and instantiation)

The Primary RQ asks how GaC can be designed and instantiated as a MLOps pipeline. Evidence is primarily **structural** rather than a single numeric table. Policy parameters live in `params.yaml` (seed, pipeline profile, `gates.fairness.max_equalized_odds_difference`, `gates.shap.min_top_mean_abs_shap`, sensitive column names). Pipeline stages and data dependencies are defined in `dvc.yaml` and locked in `dvc.lock`. Continuous integration is under `.github/workflows/` (`ci.yml` for the standard vs governed matrix; `governed_deploy.yml` and `docker-build.yml` for Gate C and container artefacts). Executable checks are implemented in `src/gate_fairness.py` and `src/gate_shap.py`; training entry points and metric emission are in the repository’s training modules as referenced in project documentation. The illustrative FastAPI service is under `serving/` with `Dockerfile` and `docker-compose.yml` at the repository root. When training locally, MLflow (`sqlite:///./mlflow.db` by default) records runs with tags linking git commit, `params.yaml` digest, and `dvc.lock` digest, supporting the traceability narrative in Chapter 5. Together, these artefacts demonstrate **instantiation**: a working path from data to metrics to optional deployment-shaped services.

### F.2 Sub-RQ1 (controlled comparison and blocking)

Sub-RQ1 is supported by **committed JSON** and a **fixed** comparison protocol. The authoritative tabulated metrics for the thesis body are in `metrics/experiment_comparison.json`.

Before locking the PDF, run `python scripts/verify_thesis_metrics.py` from the repository root; it prints canonical values and confirms that embedded JSON files parse consistently. If you change `params.yaml`, training code, gates, or raw data handling, regenerate the comparison with `python scripts/compare_profiles.py` and recommit `experiment_comparison.json`; then update Chapter 6 (timestamp, git commit) and Appendix C so they match.

The **threshold tightening** demonstration that shows Gate A failing is archived in `metrics/fairness_gate_subrq1_threshold_demo_fail.json`. The baseline narrative in Chapter 6 uses `max_equalized_odds_difference: 0.70`; the demo used `0.55` against the same observed EOD (~0.617). Do not hand-edit the thesis tables: diff the JSON against the script output.

Optional stress experiments (undersampling minority sensitive levels in training only) are documented in `docs/stress_experiment.md` and can extend Sub-RQ1 discussion when additional robustness checks are required—they are **not** required for the core claim that the governed path can **block** under stricter policy.

### F.3 Sub-RQ2 (automation-to-approval latency)

Sub-RQ2 evidence is `metrics/human_oversight_latency.json` plus the workflow run URL cited in Chapter 6. The metric definition (what “start of approval job” means) is specified in `docs/human_oversight.md`. The sample is **n = 1**; treat it as a **plausible order-of-magnitude** for GitHub-mediated approval wait, not as a statistically representative estimate.

### F.4 Compliance mapping and legal sources

The thematic mapping of Act expectations to **engineering** controls appears in `docs/COMPLIANCE_MATRIX.md` and is referenced as Appendix B. Replace placeholder Article citations with **EUR-Lex** references in the final PDF. The matrix is an **audit-style** scaffold for the thesis, not a legal opinion.

### F.5 What the repository does not contain

The repository does **not** include proprietary Norwegian credit data, core banking integrations, or signed legal advice. It does **not** prove adoption by any financial institution. Examiners should evaluate the thesis as a **Design Science** artefact plus **controlled** metrics, bounded by the limitations in Chapters 4 and 7.

## Appendix G — Supplementary literature synthesis (optional move to Chapter 2)

**Note:** If your faculty **does not** count appendices toward the **20,000-word** minimum, **relocate** this appendix into Chapter 2 as new subsections rather than maintaining two versions.

### G.1 Model documentation and “model cards”

Mitchell *et al.* (2019) propose model cards as structured documentation accompanying trained models: intended use, factors, metrics, and ethical considerations. The goal is to make limitations and evaluation context legible to downstream teams and affected stakeholders. Model cards are not automatically generated by this thesis repository, but the same impulse—bind claims to artefacts—appears in `metrics/*.json`, `artifacts/shap_report.md`, and MLflow tags.

A natural extension of this work would emit a Markdown or PDF model card in CI from the same inputs as the gates, so that documentation is regenerated whenever training or policy parameters change. That would strengthen the “transparency artefact” story while keeping the thesis scope bounded in the main chapters.

### G.2 Contestability and explanation in administrative law (sketch)

Scholarship on automation in public administration often asks whether citizens can contest decisions and access meaningful explanations. Credit decisions in private banking are typically contractual rather than administrative acts, yet parallel questions arise around fair process, explanation, and appeal in consumer relationships. EU consumer protection and data protection frameworks interact with product rules for high-risk AI systems in ways that depend on the actor and processing context.

This thesis does not analyse appeal pathways or draft consumer-facing disclosures. It provides engineering hooks—logs, SHAP reports, human approval before release—that could support wider process design when combined with legal advice and organisational policy.

### G.3 Open-source governance patterns

Open-source communities rely on CODEOWNERS, branch protection, required reviews, and signed commits for trust and safety. Gate C borrows the review concept for ML artefacts: certain jobs cannot proceed without human approval recorded in the platform. The parallel is instructive: governance is partly social (who may approve) and partly technical (what must pass before approval).

### G.4 Where to read next (programme-dependent)

The author follows the supervisor’s reading list. Typical clusters include: (i) EU digital law and AI policy; (ii) fair ML and causal inference; (iii) MLOps and reliability engineering; (iv) financial regulation and consumer credit in Norway. This appendix is a bridge, not a substitute for faculty requirements. If appendices do not count toward the minimum word count, merge G.1–G.3 into Chapter 2 and remove duplicate prose (`docs/thesis/README.md`).

### G.5 SHAP variants and practical choices

SHAP implementations differ in explainer choice (TreeExplainer, KernelExplainer), background sampling size, and feature preprocessing. The thesis repository fixes parameters in `params.yaml` (e.g. `gates.shap.background_samples`) so that SHAP outputs are reproducible for a given commit. Changing these parameters changes explanations; that is not “cheating,” but it is a reason to document settings in the thesis and to treat SHAP as an audit artefact tied to a specific configuration.

### G.6 Fairlearn: metric definitions and validation scope

Fairlearn’s equalized odds difference is computed on the validation predictions produced by the training pipeline. The metric is only defined relative to the chosen sensitive feature and the classifier’s behaviour on the held-out split. It does not account for selection into the dataset, marketing channels, or post-decision outcomes. Readers should treat Gate A as a **pipeline** **check**, not a full fair lending audit.

### G.7 GitHub Actions as a research platform

GitHub Actions provides runners, secrets, environments, and workflow logs. It is convenient for open reproducibility but creates dependencies on a vendor platform. A bank might replicate the same pattern in GitLab CI, Azure DevOps, or internal Jenkins with equivalent gates. The thesis uses GitHub because it matches typical student workflows and public artefact sharing.

### G.8 DVC: when it helps and when it is overhead

DVC tracks data and pipeline stages. For small public datasets, DVC is sometimes more machinery than strictly necessary, but it supports the narrative that data and code evolve together with locked stages. If examiners question complexity, the author can justify DVC as part of reproducibility discipline rather than as a requirement for the core metrics.

### G.9 Stress experiments and ethics of synthetic harm

The repository supports optional stress modes that manipulate training data to worsen fairness outcomes on validation. Such experiments must be described carefully: the goal is to demonstrate gate behaviour, not to simulate real-world discrimination against a protected group. Use `docs/stress_experiment.md` and supervisor guidance.

### G.10 Serving security: threat sketch

The FastAPI service includes optional API keys and rate limits as teaching examples. A production credit API would require authentication integration, fraud controls, encryption, and operational monitoring beyond this thesis. Do not present the demo service as security-hardened.

### G.11 Writing style: precision vs buzzwords

Examiners respond well to precise terms: “gate failure,” “committed JSON,” “Environment approval,” “equalized odds difference.” They respond poorly to vague claims that “AI ethics is embedded” without pointing to an artefact. Prefer evidence binding over adjectives.

### G.12 Checklist before printing the PDF

Confirm: title page fields; table of contents page numbers; figure and table captions; consistent heading levels; references complete; EUR-Lex citations for quoted Articles; Chapter 6 matches JSON; `verify_thesis_metrics.py` passes; repository URL and commit or tag cited.

### G.13 MLflow: what is logged and what is not

MLflow runs store parameters, metrics, tags, and artefact paths depending on training code. They do **not** automatically store a full legal rationale for threshold choices. Organisations must still record **why** a fairness budget is 0.70 rather than 0.55 in meeting minutes or policy documents. The thesis uses MLflow to connect engineering outputs to code state, not to replace governance records.

### G.14 GitHub Environments and separation of duties

Environment protection rules can require reviewers from a specific team. That mirrors separation-of-duties ideas in operational risk: the person who commits model code might not be the person who approves release. The thesis uses a single maintainer scenario in places; production would separate identities and use stronger authentication.

### G.15 Container images and supply chain

Pushing Docker images to GHCR creates an artefact chain from commit to image digest. Supply-chain attacks target build systems; this thesis does not analyse SBOM signing or image scanning policies. Mentioning the limitation signals awareness for examiners in security-oriented programmes.

### G.16 Logistic regression as a baseline

Logistic regression is not state-of-the-art for every tabular dataset, but it is stable, fast, and relatively interpretable. For Sub-RQ1, the point is comparison between profiles under identical model family and split, not winning a leaderboard.

### G.17 Random seed and stochasticity

`seed: 42` controls sklearn and numpy randomness where used. Some libraries may still exhibit non-determinism on GPU or across BLAS threads; this CPU-focused sklearn pipeline aims for reproducibility on a typical laptop and CI runner.

### G.18 OpenML fallback

If the UCI file is absent, OpenML `credit-g` may load. Schema differences could affect metrics slightly. The thesis binds results to the **committed** `experiment_comparison.json` lineage string to avoid ambiguity.

### G.19 Feature schema and inference contract

`feature_schema.json` documents expected columns for `/predict`. It reduces silent shape errors during demos. Production systems would add contract tests against real-time feature stores.

### G.20 Rate limiting and abuse scenarios

Optional rate limits mitigate naive flooding of `/predict` in demos. They do not stop authenticated insider abuse or adversarial examples; those are out of scope.

### G.21 Latency metric and queueing

Sub-RQ2 includes queueing and approval wait. Decomposing those components would require more runs and platform access logs. The thesis reports the aggregate seconds field as defined.

### G.22 Academic integrity and repository history

Public git history may include experimental commits. Examiners should evaluate the thesis against a **tagged** snapshot, not an arbitrary moving branch.

### G.23 Translations and language

If the final thesis is in Norwegian, translate technical terms consistently (e.g. “gate,” “pipeline,” “fairness”) and align with faculty terminology lists.

### G.24 Accessibility of figures

Export Figure 1 from Mermaid with sufficient contrast for colour-blind readers; add alt text in Word/PDF per accessibility guidelines if required.

### G.25 Archiving for long-term access

Consider Zenodo or institutional repository deposit of the exact commit hash, data snapshot references, and PDF together for long-term reproducibility.

### G.26–G.40 Quick reference notes (exam preparation)

The following short notes are **mnemonics** for oral defence preparation; they are not independent claims beyond the main chapters.

**G.26** Primary RQ asks *how* to design and instantiate GaC, not whether GaC is legally sufficient.

**G.27** Sub-RQ1 is about controlled difference and demonstrable blocking, not production approval rates.

**G.28** Sub-RQ2 measures CI automation-to-approval seconds, not bank processing time.

**G.29** Gate A uses Fairlearn EOD vs a threshold; Gate B mandates SHAP artefacts; Gate C is human approval in workflow.

**G.30** `experiment_comparison.json` is the authoritative table source for Chapter 6.

**G.31** Threshold demo JSON proves `gate_passed: false` under tighter max EOD.

**G.32** Norway is jurisdictional context; data are German public UCI.

**G.33** DSR contribution is artefact + evaluation + principles, not legal compliance.

**G.34** SHAP is an audit artefact; not necessarily legal transparency to data subjects.

**G.35** Serving API is illustrative; not production security.

**G.36** `verify_thesis_metrics.py` is a sanity preflight before PDF lock.

**G.37** EUR-Lex citations belong in the final PDF for quoted Articles.

**G.38** Stress experiments are optional and must be ethically framed.

**G.39** If appendices do not count toward word minimum, merge appendix prose into Chapter 2 or 4.

**G.40** Freeze a git tag for the examiner snapshot.

## Appendix H — Oral defence preparation: anticipated questions and answers (draft)

**Note:** Polish with your supervisor; answers must stay consistent with Chapters 1–8 and committed JSON.

**Q1: Does your repository comply with the EU AI Act?**  
A: No full compliance is claimed. The thesis maps selected themes to engineering controls and evaluates a DSR artefact. Legal compliance requires institutional processes and EUR-Lex-grounded analysis beyond this work.

**Q2: Why not use Norwegian data?**  
A: Access and ethics constraints; the thesis prioritises open replication with a documented public dataset.

**Q3: Why equalized odds?**  
A: It is a standard group fairness metric with a clear implementation in Fairlearn and a direct threshold interpretation for gates. Other metrics could be added as future work.

**Q4: Why SHAP if you use logistic regression?**  
A: To align with common MLOps explainability artefacts and to exercise a gate that produces documentation even when coefficients exist. It also supports comparison with non-linear extensions later.

**Q5: What does 7 s latency prove?**  
A: Only the defined Sub-RQ2 metric for one cited CI run: seconds from gates complete to approval job start, including Environment wait when configured.

**Q6: Could this be used in a bank?**  
A: As a pattern for pilots, possibly, after legal review and integration with bank controls. This thesis does not evaluate a bank deployment.

**Q7: What is your main scientific contribution?**  
A: A GaC instantiation with bounded evaluation evidence and explicit limitations on law and generalisation.

**Q8: What would you do differently with more time?**  
A: Multi-seed studies, additional datasets, mitigation methods, drift gates, and a supervised legal chapter if required by the programme.

**Q9: How do you address fairness washing?**  
A: By explicit scope limits, proxy warnings, and by treating gates as policy enforcement mechanisms that require human choices about thresholds and sensitive attributes.

**Q10: What is the role of Norway in the thesis?**  
A: EEA and pedagogical context for high-risk credit scoring; not empirical data from Norwegian banks.

**Q11: Why GitHub Actions rather than Jenkins or Azure DevOps?**  
A: Public reproducibility and typical student tooling; the pattern transfers to other CI systems.

**Q12: Is logistic regression outdated?**  
A: It is a stable baseline for controlled comparison; the thesis is about governance mechanics, not leaderboard accuracy.

**Q13: Could Gate B fail in baseline configuration?**  
A: Yes, if `min_top_mean_abs_shap` is raised; baseline 0.0 makes failure unlikely for SHAP magnitude.

**Q14: What about data drift after deployment?**  
A: Out of scope; future work could add monitoring gates.

**Q15: How do you know the JSON was not edited by hand?**  
A: Regenerate with `compare_profiles.py` and diff; verification script checks parseability and key fields.

**Q16: What ethical review was required?**  
A: Depends on faculty rules; public UCI data with proxy attributes still deserves careful disclosure.

**Q17: What is the main limitation?**  
A: External validity: German public benchmark, not Norwegian production credit.

**Q18: How does this relate to your career goals?**  
A: Prepares for roles bridging ML engineering with risk/compliance awareness in EEA context.

**Q19: What would regulators ask that this thesis does not answer?**  
A: Whether a specific deployment satisfies Articles, data rights, and sector rules—legal analysis outside scope.

**Q20: Final one-sentence takeaway?**  
A: GaC can make selected governance expectations executable in CI/CD with traceable evidence, without replacing law or organisational governance.

---

*End of manuscript draft.*