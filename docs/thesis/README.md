# Thesis manuscript (`MANUSCRIPT.md`)

This folder holds the **thesis draft** in Markdown (`MANUSCRIPT.md`). The **repository copy** is the working **full draft**; replace **only** bracketed title-page placeholders (`[Author Name]`, `[Supervisor]`, …) and align the exported Word file with the **faculty template** (manual step).

## Export to Word (optional)

From the repository root, with [Pandoc](https://pandoc.org/) installed:

```bash
pandoc docs/thesis/MANUSCRIPT.md -o thesis-draft.docx --from markdown --toc --number-sections
```

Then apply your faculty **.dotx** styles in Word (Heading 1–3, captions, references).

## Source of truth

Narrative and claims follow [../THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md). Bind numbers to **`metrics/experiment_comparison.json`** (P3 comparison; includes **`git_commit`**) and regenerate with `python scripts/compare_profiles.py` after changing `params.yaml`, gates, or data—do not rely on a hand-pasted commit hash here.
