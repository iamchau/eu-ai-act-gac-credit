# Thesis figures (exports)

**Documentation charter:** [../DOCUMENTATION_FOUNDATION.md](../DOCUMENTATION_FOUNDATION.md).

Store **thesis-bound** visuals here so they stay next to the narrative docs. **Do not** commit large binary churn without need—your faculty may prefer figures only in Word; this folder is the **working** location for drafts and PNG/PDF exports.

**Master checklist:** [THESIS_WRITING_HUB.md](../THESIS_WRITING_HUB.md) §5.

---

## Naming

`Fig01_gac_architecture.png`, `Fig02_pipeline_flow.png`, … matching the hub numbering.

---

## Caption template (use in Word)

Each figure in the thesis PDF should carry:

1. **Number + title** — e.g. *Figure 4.2 — Gate A/B/C control flow in the reference implementation.*  
2. **What it shows** — one sentence, factual.  
3. **Source** — *Author* (diagram), *Screenshot: GitHub Actions run …* (include **run id** or date), *MLflow UI*, etc.  
4. **Limitation** (if proxy) — e.g. *CI proxy; not a production bank deployment.*

**Accessibility:** Add **alt text** in Word for every figure (short description for screen readers / examiner PDFs).

---

## Technical

| Topic | Suggestion |
|-------|------------|
| **Resolution** | Prefer **vector** (PDF/SVG) for diagrams; raster **≥ 300 dpi** at print width if your program prints the thesis. |
| **Screenshots** | Crop to relevant UI; avoid full-desktop clutter; same **zoom** level across related figures. |
| **Third-party UIs** (GitHub, MLflow) | Academic use of screenshots is usually fine; follow your faculty’s policy on logos if strict. |

---

## Source files (Mermaid)

| File | Thesis figure | Export |
|------|----------------|--------|
| [Fig01_gac_architecture.mmd](Fig01_gac_architecture.mmd) | Figure 1 — standard vs governed + gates | `mmdc -i Fig01_gac_architecture.mmd -o Fig01_gac_architecture.png` (see header comment) |
| [Fig02_ci_matrix.mmd](Fig02_ci_matrix.mmd) | Figure 2 — conceptual CI matrix | same |

Same diagrams are duplicated for convenience in [thesis/MANUSCRIPT.md](../thesis/MANUSCRIPT.md) Appendix F (Figure 1).

## Suggested exports

| Asset | How |
|-------|-----|
| Architecture | `Fig01_gac_architecture.mmd` or draw.io, PowerPoint, or Mermaid → PNG/PDF |
| MLflow | Screenshot of run with `git_commit`, `params_yaml_sha16` tags |
| GitHub Actions | Screenshot of successful matrix workflow run **or** `Fig02_ci_matrix.mmd` |
| SHAP | Render from `artifacts/shap_report.md` or notebook |

---

## Git

Add patterns to `.gitignore` only if binaries become noisy, e.g. `*.pptx` — otherwise keep small PNGs for reproducibility.
