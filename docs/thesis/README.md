# Thesis manuscript (`MANUSCRIPT.md`)

This folder holds the **thesis draft** in Markdown (`MANUSCRIPT.md`). The **repository copy** is the working **full draft**; replace **only** bracketed title-page placeholders (`[Author Name]`, `[Supervisor]`, …) and align the exported Word file with the **faculty template** (manual step).

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

## Check metrics before locking PDF

```bash
python scripts/verify_thesis_metrics.py
```

To align inline Markdown code/bold in the manuscript after bulk edits:

```bash
python scripts/fix_manuscript_inline_md.py
```

## Source of truth

Narrative and claims follow [../THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md). Bind numbers to **`metrics/experiment_comparison.json`** (P3 comparison; includes **`git_commit`**) and regenerate with `python scripts/compare_profiles.py` after changing `params.yaml`, gates, or data—do not rely on a hand-pasted commit hash here.
