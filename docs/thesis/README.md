# Thesis manuscript (`MANUSCRIPT.md`)

This folder holds the **thesis draft** in Markdown (`MANUSCRIPT.md`). The **repository copy** is the working **full draft**; replace **only** bracketed title-page placeholders (`[Author Name]`, `[Supervisor]`, …) and align the exported Word file with the **faculty template** (manual step).

**Excellence roadmap (phases, checklists):** [../EXCELLENCE_ROADMAP.md](../EXCELLENCE_ROADMAP.md).  
**Spine (RQs, evidence):** [../THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md).

---

## Export to Word (optional)

From the repository root, with [Pandoc](https://pandoc.org/) installed:

```bash
pandoc docs/thesis/MANUSCRIPT.md -o thesis-draft.docx --from markdown --toc --number-sections
```

**Using a faculty reference document** (styles from a `.docx` saved from your `.dotx`): save a one-page Word file that uses your template styles as `reference.docx`, then:

```bash
pandoc docs/thesis/MANUSCRIPT.md -o thesis-draft.docx --from markdown --toc --number-sections --reference-doc=reference.docx
```

Open `thesis-draft.docx` in Word, **review Heading 1–3**, table formatting, and **Table of Contents** (Update field). Paste into a **new document** created from your faculty `.dotx` if you prefer to attach the template after the fact.

---

## Check metrics before locking PDF

```bash
python scripts/verify_thesis_metrics.py
```

---

## Evidence freeze (Phase C — examiner snapshot)

Before declaring Results final:

1. Commit all thesis and metrics changes so the working tree is clean.
2. Regenerate comparison JSON if needed: `python scripts/compare_profiles.py`, then commit `metrics/experiment_comparison.json`.
3. Run `python scripts/verify_thesis_metrics.py` and fix any failures.
4. Ensure Chapter 6 and Appendix C cite the `git_commit` inside `experiment_comparison.json` (not a stale hash).
5. Create an **annotated tag** on that commit (example name; adjust date):

```bash
git tag -a thesis-examiner-YYYY-MM-DD -m "Thesis evidence freeze; see experiment_comparison.json git_commit"
git push origin thesis-examiner-YYYY-MM-DD
```

Mention the tag or commit hash in the thesis front matter or methods if your faculty requires a frozen artefact. For a full deposit (Zenodo, institutional), use the **same** commit as the tag.

To align inline Markdown code/bold in the manuscript after bulk edits:

```bash
python scripts/fix_manuscript_inline_md.py
```

---

## Source of truth

Narrative and claims follow [../THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md). Bind numbers to **`metrics/experiment_comparison.json`** (P3 comparison; includes **`git_commit`**) and regenerate with `python scripts/compare_profiles.py` after changing `params.yaml`, gates, or data—do not rely on a hand-pasted commit hash here.

---

## Word count and faculty rules

Many programmes require **≥ 20,000 words** of main text. From the repo root, approximate count of `MANUSCRIPT.md` after the YAML block:

```bash
python -c "import re; p=open('docs/thesis/MANUSCRIPT.md',encoding='utf-8').read(); body=re.sub(r'^---.*?---','',p,flags=re.S); print(len(re.findall(r'\S+', body)))"
```

**Confirm with your supervisor or examination office:** whether **references**, **appendices**, and **front matter** count toward the minimum, and whether there is an **official** total word-count definition. If appendices do not count, move required narrative into Chapters 2–4 (or the Discussion) rather than relying only on appendix prose.

---

## Author checklist (meta — not part of the scholarly argument)

Use this for **submission hygiene**; the main `MANUSCRIPT.md` stays in thesis voice.

| Topic | Action |
|--------|--------|
| **Learning outcomes** | If required, replace Section 2.27 placeholder with the programme’s **official** wording after supervisor review. |
| **Programme reading list** | Cross-walk required texts to chapters: short notes per required item (what was taken from it, where it appears). Nordic public-sector AI ethics or business ethics add-ons only if the programme demands them. |
| **AI / tools disclosure** | If the faculty mandates a statement on LLMs or editors, add it to **front matter** with the **exact** wording the board requires. Verify every citation and Article number against primary sources (`metrics/*.json`, EUR-Lex)—generated drafts hallucinate. |
| **GDPR / DPIA** | A full GDPR compliance analysis is **not** claimed in this thesis; add a dedicated subsection or faculty ethics form **only** if required. |
| **Frozen artefact** | Cite a **git tag or commit** in the thesis so examiners can align text and code; use Zenodo or a zip if the programme requires a deposit. |
| **Repository privacy** | If the repo becomes private, archive a snapshot and document access rules for examiners. |
| **Final submission extras** | Confirm whether the programme expects: extended literature chapter, explicit Peffers steps in the introduction, reflection on learning outcomes, or vendor-neutral comparison to commercial tools—add in the faculty template without breaking Chapter 6 evidence binding. |

---

## Forks and derivative degree projects

If this repository is reused as a **template** for another thesis:

1. Freeze a **commit tag** for the examiner PDF.  
2. Regenerate **`metrics/experiment_comparison.json`** after any material change to data, gates, or `params.yaml`.  
3. Keep **Chapter 6** aligned with `verify_thesis_metrics.py`.  
4. Write the introduction and reflection in **your own** voice; expand the literature with **your** programme list—do not duplicate the reference manuscript verbatim.  
5. Optional stress experiments (`docs/stress_experiment.md`) are documented for extra robustness discussion; they are **not** required for the core GaC blocking claim.

---

## Appendix narrative vs word count

If appendices do not count toward the minimum, merge essential technical notes from Appendix G into Chapter 2 or 4 and **remove duplicate** prose rather than maintaining two versions.

---

## Documentation map

- Charter & precedence: [../DOCUMENTATION_FOUNDATION.md](../DOCUMENTATION_FOUNDATION.md)  
- Journey ticks: [../PROJECT_JOURNEY.md](../PROJECT_JOURNEY.md)  
- Writing hub (pages, figures): [../THESIS_WRITING_HUB.md](../THESIS_WRITING_HUB.md)
