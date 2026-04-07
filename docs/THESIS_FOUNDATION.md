# Thesis foundation — air-tight narrative, RQs, and evidence

Use this as the **single spine** for writing. If a paragraph does not connect to an RQ, DSR cycle, or cited obligation, cut it or move it to an appendix.

---

## 1. Title and one-sentence claim

**Title (proposal):** *Implementing the EU AI Act: A Design Science Study on Governance-as-Code (GaC) for High-Risk Credit Scoring in Norway.*

**Core claim (defendable):** You **design and evaluate** a **GaC MLOps instantiation** (automated fairness + explainability + human-oversight **gates** in CI/CD) for **high-risk credit scoring**, and you **measure** (i) **policy effectiveness** vs a **standard** pipeline and (ii) **human-in-the-loop latency** in a **controlled CI proxy**.

**Note:** If you adopt an **alternative Sub-RQ2** (traceability, oversight-as-design, or trade-offs), replace clause **(ii)** consistently in the Introduction, Results, and evidence index—see [SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md).

**Do not claim:** That a Norwegian bank has adopted this system, that EU law is “fully implemented” in code, or that one dataset proves regulatory acceptance.

---

## 2. Research questions — operational definitions

### Primary RQ

**Proposal wording:** *How can we design a "Governance-as-Code" MLOps architecture that automatically enforces EU AI Act requirements (like fairness and oversight) within a CI/CD pipeline?*

**Tight formulation:**

| Phrase | Meaning in *this* thesis |
|--------|-------------------------|
| **Design** | A **construct** (GaC pipeline) + **instantiation** (working repo: MLflow, DVC, GitHub Actions, gate scripts) + **design principles** (discussion section). |
| **Automatically enforces** | **Executable checks**: if a gate fails, the pipeline **does not** proceed to “release” (or records failure); **not** that law is “fully automated.” |
| **EU AI Act requirements** | **Mapped** to concrete controls (fairness, transparency/explainability, human oversight, logging) — see [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md). **Legal completeness** is **not** claimed. |
| **CI/CD pipeline** | GitHub Actions + local `dvc repro`; **deployment** is **illustrative** (artifact + environment), not a production bank stack. |

### Sub-RQ 1

**Proposal:** *Does using automated GaC "gates" actually reduce the rate of non-compliant models being approved compared to the old way of doing things?*

**Tight formulation:**

| Term | Definition |
|------|------------|
| **Old way** | **Standard pipeline profile**: train for performance only; **no** fairness/SHAP gates in the comparison path. |
| **Non-compliant** | **Operationalized** as: failing **fairness threshold** (Equalized Odds) and/or **SHAP** sanity check **when those gates are enabled** — **not** a legal opinion. |
| **“Reduce the rate”** | In this thesis: **one controlled comparison** (same seed, same data lineage) + **at least one** demonstration where **stricter policy** or **stressed** training causes a **governed** path to **block** (see [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md)). **Do not** claim statistical sampling of “models in production.” |

### Sub-RQ 2

**Proposal:** *How much extra latency does it add to the process when we force a human-in-the-loop into an automated credit scoring workflow?*

**Tight formulation:**

| Term | Definition |
|------|------------|
| **Latency** | **Seconds** from **end of automated gates** to **start of the approval job** in GitHub Actions, recorded in `metrics/human_oversight_latency.json` (example: **7 s** for run [24081106560](https://github.com/iamchau/eu-ai-act-gac-credit/actions/runs/24081106560)). |
| **Limitation (must state)** | **CI proxy** only — not core banking latency, not auditor calendar time, not signing with a national eID. |

#### Thesis-ready one-liners (use in Introduction — replace proposal wording)

Use these **instead of** the informal proposal sentences so examiners do not quote over-broad claims.

| RQ | One sentence (adapt to faculty style) |
|----|----------------------------------------|
| **Primary** | *How can Governance-as-Code be **designed and instantiated** as a MLOps pipeline for high-risk credit scoring that **maps selected** EU AI Act obligations to **executable** fairness, explainability, and human-oversight controls in CI/CD—**without** claiming that the Act is fully automated or fully implemented in code?* |
| **Sub-RQ1** | *Under **controlled** comparison (same seed, same data lineage), does the **governed** profile (fairness + SHAP gates) **differ** from the **standard** profile—and can **stricter policy** or stress **demonstrate** that the governed path **blocks** when operational non-compliance is detected?* |
| **Sub-RQ2** | *What **automation-to-approval** latency does a human gate add in the **GitHub Actions** instantiation—measured as seconds from **end of automated gates** to **start** of the approval job—and **not** as end-to-end credit decision or legal signing time?* |

#### Sub-RQ2 — what it answers vs what it does not

**Must match** [human_oversight.md](human_oversight.md): the recorded interval **includes** time waiting for **GitHub Environment** approval (reviewer) and runner queue **before** the `human-approval-release` job starts — not “pure orchestration ms.”

| **Answers (in scope)** | **Does not answer (state explicitly)** |
|------------------------|----------------------------------------|
| Wall-clock seconds from **end of automated gates** to **start** of the approval job’s first step (`human_oversight_latency_seconds`) — **includes** Environment approval wait when reviewers are configured | End-to-end **bank** credit decision latency, **core banking** systems, **national eID** / qualified signature workflows |
| A **functional analogue** for “human oversight before release” in a DSR artifact | **Article 14** compliance as a **legal** conclusion |

#### Sub-RQ parity (for Discussion one paragraph)

Sub-RQ1 and Sub-RQ2 are **complementary**, not **symmetric**: Sub-RQ1 carries the main **evaluative** comparison (standard vs governed + blocking demo); Sub-RQ2 is a **narrow** measure of **GitHub-mediated** approval latency (gates done → approval job start), **not** banking science. **State that** so Sub-RQ2 is not read as weak evidence or as a claim about production credit SLAs.

**Optional Sub-RQ2 formulations** (latency default; traceability / design / trade-offs): [SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md).

---

## 3. Design Science Research (Hevner) — map to chapters

| Cycle | What it means here | Thesis chapter material |
|-------|---------------------|-------------------------|
| **Relevance** | EU AI Act **high-risk** credit scoring; Norway as **context**; gap between law and MLOps practice | Introduction, problem, scope |
| **Rigor** | MLflow, DVC, Fairlearn, SHAP, reproducibility (seed, digests, `dvc.lock`) | Methodology, evaluation setup |
| **Design** | Build GaC pipeline; measure; iterate; **design principles** | Methodology + implementation + results |

**Design as artifact:** *Construct* (GaC) + *instantiation* (repository) + *principles* (discussion).

---

## 4. Scope alignment (proposal vs implementation)

| Proposal | Implementation | Thesis wording |
|----------|----------------|----------------|
| **Norwegian banking sector** | No bank data; **simulation** | “Norwegian **context** and **Annex III** high-risk framing”; **not** an industry case study. |
| **Sensitive attributes** “age, gender” | UCI **South German UPDATE**; **`famges`** is a **combined** proxy (see UCI) | **Explicitly** name columns used; discuss **proxy** limits and **not** raw gender recovery. |
| **Digital signature** from auditor | GitHub **Environment** approval | **Functional analogue** for human gate; **limitation**: not a qualified eID or legal signature. |
| **Articles 10–14** | Mapped in [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) | **Cite EUR-Lex** for final text; table is a **scaffold**. |

---

## 5. EU AI Act — claim discipline

**Allowed:** “The **instantiation** **operationalizes** selected obligations (e.g. logging, fairness testing, explainability artifacts, human approval before release) **as implemented** in the artifact.”

**Avoid:** “This system **complies** with the EU AI Act” without qualification.

**Always:** Primary **legal** sources (EUR-Lex consolidated) + **your** mapping table; distinguish **legal obligation** vs **engineering control**.

---

## 6. Ethics (proposal §7)

- **Public anonymized data** — low risk to subjects; **still** discuss **fairness** and **proxy** use.
- **Art. 12 / 13** (transparency, information): **link** to SHAP + MLflow + DVC **traceability** in discussion.
- **DVC**: tie to **reproducibility** and **audit trail**; **not** “every decision in production” unless you scope it to **this** experiment.

---

## 7. Suggested chapter outline (expand to page targets with your faculty)

1. **Introduction** — Problem, gap, RQs, contributions, scope, structure of thesis.  
2. **Background and literature** — Responsible AI + fairness; MLOps; EU AI Act **high-risk** credit; **gap** (law ↔ code).  
3. **Theoretical framework** — DSR (Hevner); GaC definition; **Norway / Annex III** context (short).  
4. **Methodology** — DSR process; data; **standard vs governed**; gates; **evaluation metrics**; **limitations**.  
5. **Instantiation** — Architecture (reference repo); Gate A/B/C; **tooling** (MLflow, DVC, Actions).  
6. **Results** — **Sub-RQ1** (comparison + policy/threshold demo); **Sub-RQ2** (latency JSON + run URL); **stress** optional.  
7. **Discussion** — Design principles; trade-offs (velocity vs control); **what banks could adapt**; **limits**.  
8. **Conclusion** — Answers to RQs; future work; **transposition** of EU rules in Norway (if required by your program).  
9. **References** — **EUR-Lex** for Act; papers you actually cite.  
10. **Appendices** — Metrics JSON, compliance matrix, CI run screenshots, **parameters** (`params.yaml` excerpt).

---

## 8. Evidence index (bind text to repo)

| Thesis claim | File / artifact |
|--------------|-----------------|
| Standard vs governed | `metrics/experiment_comparison.json`
| Gate A | `metrics/fairness_gate.json`, `src/gate_fairness.py`
| Gate B | `metrics/shap_gate.json`, `artifacts/shap_report.md` (after run)
| Gate C (Sub-RQ2) | `metrics/human_oversight_latency.json` + workflow URL
| Reproducibility | MLflow tags (`git_commit`, `params_yaml_sha16`, `dvc_lock_sha16`); `dvc.lock`
| Policy demo (Sub-RQ1) | [SUB_RQ1_DEMO.md](SUB_RQ1_DEMO.md) + exported fairness JSON after threshold change (prefer **one** clean `gate_passed: false`) |

**Minimum Sub-RQ1 evidence bundle:** (1) `experiment_comparison.json` for standard vs governed under shared controls; (2) **either** exported failing `fairness_gate.json` from threshold demo **or** stress run with documented gate failure.

**Minimum Sub-RQ2 evidence bundle:** `human_oversight_latency.json` + **workflow run URL**; state **n** (e.g. one illustrative run vs several).

---

## 9. Dr. Voss — thesis pre-flight checklist

- [ ] Every **Article** number matches **EUR-Lex** or official consolidated text you were assigned.  
- [ ] **Sub-RQ1** uses **defined** “standard” vs “governed” and **operational** non-compliance — not vague “ethics.”  
- [ ] **Sub-RQ2** states **CI proxy** and **single** (or few) latency samples; **one** sentence that the metric **includes** GitHub Environment approval wait when configured, and **does not** measure **bank** credit pipelines or **eID** signing.  
- [ ] Introduction uses **thesis-ready one-liners** (§2), not informal proposal wording (“reduce the rate,” “credit scoring workflow” without scope).  
- [ ] **famges** / sensitive attributes: **honest** proxy discussion.  
- [ ] **GitHub approval** ≠ **digital signature** in law — **one** clear sentence.  
- [ ] **Contributions** = **artifact + evaluation + principles**, not “solved compliance.”  

---

## 10. Thesis draft materials (Dr. Voss improvements)

Paste-ready text and checklists live outside this spine so the foundation stays stable:

| Document | Use |
|----------|-----|
| [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) | **Thesis-ready RQ one-liners**; Norway/Annex III paragraph; **operationalization** tables; Sub-RQ2 **in/out of scope**; **evidence checklist**; answer sketches; **§3b–3c** Discussion (Sub-RQ relationship, velocity vs governance); **Art. 14** analogue sentence; **single** limitations block |
| [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md) | **EUR-Lex** link and citation discipline for Regulation (EU) 2024/1689 |
| [THESIS_CUT_LIST.md](THESIS_CUT_LIST.md) | What to **remove**, **tighten**, and **keep** in the main thesis text |
| [SUB_RQ2_ALTERNATIVES.md](SUB_RQ2_ALTERNATIVES.md) | Optional **Sub-RQ2** wordings (latency default; traceability; oversight design; trade-offs) |
| [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md) | **≥50 pages**, journey **anchors**, table/figure plan, Word workflow, pre-submission pass |
| [figures/README.md](figures/README.md) | Where to put thesis **PNG/PDF** exports and naming |

---

*Maintainer: align this file with your supervisor’s chapter template; trim or merge sections as required.*
