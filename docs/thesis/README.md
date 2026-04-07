# Thesis manuscript (`MANUSCRIPT.md`)

This folder holds the **thesis draft** in Markdown. **Replace** bracketed placeholders (`[Author]`, `[Supervisor]`, …) and align chapter titles with your **faculty template**.

## Export to Word (optional)

From the repository root, with [Pandoc](https://pandoc.org/) installed:

```bash
pandoc docs/thesis/MANUSCRIPT.md -o thesis-draft.docx --from markdown --toc --number-sections
```

Then apply your faculty **.dotx** styles in Word (Heading 1–3, captions, references).

## Source of truth

Narrative and claims follow [../THESIS_FOUNDATION.md](../THESIS_FOUNDATION.md). Evidence paths and numbers match **`metrics/`** at commit **`9556cce`** (or later if you regenerate JSON).
