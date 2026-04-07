# Thesis writing — what to cut or tighten (Dr. Voss)

Use this as an **editorial checklist** alongside [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md). Goal: fewer tool names, sharper compliance story.

---

## Remove or move to appendix

- **Long tool tutorials** (MLflow UI clicks, DVC command cheat sheets) — keep **one** architecture or workflow figure if needed; cite the repo for commands.  
- **Generic AI ethics manifestos** not tied to **your** RQs or **your** artifact.  
- **Repeated** limitations — use the **single block** in [THESIS_DRAFT_SNIPPETS.md](THESIS_DRAFT_SNIPPETS.md) §4 once, then cross-reference.  
- **Marketing language** (“fully compliant,” “ensures trust,” “solves governance”) — replace with **operational** verbs: *maps, blocks, records, measures*.

---

## Tighten in main text

| Instead of | Prefer |
|------------|--------|
| Listing every Python package | **Role** of each layer (tracking, lineage, gates) + pointer to repository |
| “The EU AI Act requires…” without citation | **Article + EUR-Lex** (see [EU_AI_ACT_CITATIONS.md](EU_AI_ACT_CITATIONS.md)) |
| Vague “non-compliant model” | **Definition**: fairness/SHAP gate outcomes as in Sub-RQ1 |
| “Human oversight” as buzzword | **Sub-RQ2 definition**: what was measured (CI latency proxy) and what was not (banking SLA, eID) |

---

## Keep prominent

- **Primary RQ** — design + evaluation of GaC **instantiation**.  
- **Sub-RQ1** — standard vs governed + **blocking** demonstration.  
- **Sub-RQ2** — latency **definition** + **limitation**.  
- **Scope table** (proposal vs implementation) — one honest paragraph on dataset and Norway.  
- **Contributions**: artifact + evidence + principles — **not** “solved compliance.”

---

*Aligned with Dr. Voss checklist in [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §9.*
