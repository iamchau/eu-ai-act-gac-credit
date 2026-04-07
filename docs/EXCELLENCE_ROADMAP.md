# Excellence roadmap — manuscript and repository

**Purpose:** Single checklist to move the thesis and repo toward **examiner-grade** quality. **Authority:** [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) (RQs, evidence) and [DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md) (precedence). **Rules:** Dr. Voss wins on compliance; the Thesis Excellence Mentor project rule applies to prose craft within those bounds.

**Related:** Author-facing meta (word count, AI disclosure, fork/reuse) lives in [thesis/README.md](thesis/README.md), not in the main thesis argument.

---

## Principles

| Layer | Rule |
|--------|------|
| Evidence | Chapter 6 numbers trace to committed `metrics/*.json` and `scripts/verify_thesis_metrics.py`. |
| Law | EUR-Lex for quoted Articles; [COMPLIANCE_MATRIX.md](COMPLIANCE_MATRIX.md) is a scaffold. |
| Voice | One thesis author; handbook instructions belong in README/hub, not the scholarly chapters. |
| Precedence | `params.yaml` + code → foundation → oversight docs → rest ([DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md)). |

---

## Phases

### Phase A — Spine coherence

- [x] `MANUSCRIPT.md` RQs match [THESIS_FOUNDATION.md](THESIS_FOUNDATION.md) §2 (thesis-ready one-liners) — verified 2026-04-07.
- [x] Scope table (proposal vs implementation): cross-ref to foundation Section 4 in manuscript Section 1.7.
- [ ] [DR_VOSS_REVIEW_LOG.md](DR_VOSS_REVIEW_LOG.md) updated when claims or evidence change materially — ongoing.

### Phase B — Manuscript excellence

- [x] Abstract: problem, method, main finding, contribution, explicit limitation (single closing sentence).
- [x] Introduction: chapter map (Table 1a) + RQ blockquotes aligned with foundation one-liners.
- [x] **Limitations:** canonical block Section 7.5; methods detail Section 4.5; cross-references elsewhere, not full repeats.
- [x] **Discussion** overview paragraph (Chapter 7 opening); **Conclusion** opening de-bolded (Chapter 8); **Section 7.1** prose pass.
- [ ] Results report only; interpretation in Discussion — spot-check before PDF.
- [ ] References: faculty style; Regulation from EUR-Lex — **author** applies template to final Word export.
- [ ] Figures/tables per [THESIS_WRITING_HUB.md](THESIS_WRITING_HUB.md); captions state CI/proxy limits where needed.

### Phase C — Evidence freeze

- [x] `python scripts/verify_thesis_metrics.py` passes before PDF lock — run again after any metrics change.
- [ ] Examiner git tag — **commands** in [thesis/README.md](thesis/README.md); tag **after** commit freeze.
- [ ] Sub-RQ1 demo JSON + Sub-RQ2 latency JSON + URLs aligned with Chapter 6 — verify at PDF lock.

### Phase D — Code and CI

- [ ] Gate behaviour matches narrative (`src/gate_*.py`, `params.yaml`).
- [ ] CI green; [DOCUMENTATION_FOUNDATION.md](DOCUMENTATION_FOUNDATION.md) deprecations (Gate C, MLflow) respected in docs.

### Phase E — Documentation ecosystem

- [ ] No stale facts in `docs/*.md` vs charter deprecations table.
- [ ] [PROJECT_JOURNEY.md](PROJECT_JOURNEY.md) ticks updated; [PROJECT_PLAN.md](../PROJECT_PLAN.md) “Last updated” bumped after milestones.

### Phase F — Submission

- [ ] Pandoc → Word with `--reference-doc` if required ([thesis/README.md](thesis/README.md)).
- [ ] Final PDF: quoted legal text from official consolidated source.

### Phase G — Examination

- [ ] Appendix H Q&A aligned with frozen claims.
- [ ] Short repo walkthrough: `params.yaml` → `metrics/` → workflows.

---

## Priority order (execution)

1. Phase A (spine) — avoids wasted editing.  
2. Phase B (voice + limitations spine) — highest examiner impact.  
3. Phase C at freeze time.  
4. Phases D–E in parallel where possible.  
5. F–G before defence.

---

## Definition of done (excellence bar)

- [ ] RQs and evidence paths are explicit and consistent.  
- [ ] No “compliance in a box” or unqualified legal compliance claims.  
- [ ] Meta instructions not dominating scholarly chapters.  
- [ ] One limitations architecture (7.5 + 4.5), not five scattered versions.  
- [ ] Verify script passes; tagged snapshot for examiners.

*Maintainer: tick items as completed; align with supervisor and faculty template.*
