# 2026 ADHD graph validation

Separate validated graphs and reports are available for all three personas:

| Age | Original edges | Supported | Partial support | Insufficient evidence | Not assessable | Graph | Excel report |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 8 | 68 | 2 | 31 | 22 | 13 | [Open graph](../../validation_2026_age8/validated_graph.html) | [Download report](../../validation_2026_age8/edge_validation.xlsx) |
| 32 | 74 | 2 | 25 | 38 | 9 | [Open graph](../../validation_2026_age32/validated_graph.html) | [Download report](../../validation_2026_age32/edge_validation.xlsx) |
| 45 | 70 | 2 | 22 | 39 | 7 | [Open graph](../../validation_2026_age45/validated_graph.html) | [Download report](../../validation_2026_age45/edge_validation.xlsx) |

No edges were classified as contradicted or mixed evidence. This does not mean every finding agrees: a null result on a different exposure, population or endpoint cannot refute the original causal claim. All 212 original edges remain visible. Click an edge to read its judgment, recommended revision, source quotation and one-based PDF page link. Line colors and dashes show evidence status; line widths retain the original, unvalidated numeric strengths.

## Corpus and review scope

The sole source is the supplied `2026 ADHD Papers` folder: **159 PDFs, 2,212 file pages and 158 distinct normalized full-text documents**. The two copies of `1-s2.0-S1087079226000754-main.pdf` have different binary hashes but identical normalized text. They count as one document. Reviews may also share primary studies; document counts are not independent-study counts.

The year identifies the graph snapshot and supplied corpus. Some papers have earlier online publication dates. Source dates were not silently relabeled as 2026.

Titles/first pages and available abstracts were screened across the corpus, followed by targeted review of relevant full-text passages. **53 selected passages from 38 documents** have been verified against actual source PDF pages. This is a bounded evidence review of the existing graph claims, not exhaustive critical appraisal of every full text or a systematic search of all ADHD research. Uncited documents were screened but do not become supporting evidence simply because they are in the folder.

## Interpretation

- Inherited liability and possible medication adverse effects have direct qualitative support across the lifespan. Their numeric strengths remain unvalidated.
- Pediatric medication, parent training and digital-treatment findings support narrower pathways, with population, intervention and outcome qualifications.
- Adult CBT findings concern specific symptom or functional endpoints. Workplace accommodations have observational support; flexible hours do not establish remote-work benefits.
- Digital reminders and monitoring can support adherence, but they differ from digital therapeutics targeting core symptoms. Pediatric efficacy is not transferred to adult personas.
- Planned telehealth/digital trials, co-design needs assessments, protocols and social-video content audits do not establish completed treatment-access or downstream diagnostic effects.
- Impairment, core symptoms, child quality of life, caregiver quality of life and employment are separate outcomes. Treatment gains cannot establish diagnosis-only benefits.
- Unordered categorical signs, undefined treatment dependency/overdiagnosis pressure, and adherence-to-treatment-receipt versus benefit mismatches are explicitly identified.

An insufficient-evidence judgment means the supplied corpus does not establish that edge. It is not proof that the relationship is false. Full methods and edge-specific qualifications are in each age folder.

## Files and reproducibility

The main `Dashboard.py` also displays these reports when 2026 and age 8, 32 or 45 are selected. It uses the same validation colors, edge-selection behavior, paginated evidence panel and served PDF links as 1970, 1990 and 2010. The year-level corpus panel counts 158 distinct reviewed PDF documents across all three ages, deduplicating the second sleep-review copy. Workbook screening totals remain separate from supplied/reviewed document counts.

`extracted_papers.json` contains source hashes, native PDF-page text, page counts and text-duplicate identifiers. Text normalization uses Unicode NFKC, removal of soft hyphens, end-of-line word dehyphenation and whitespace collapsing; it retains native PDF reading order to avoid interleaving columns. `screening.txt` provides the first-page screening excerpts.

`review_evidence.py` contains manually selected quotations and source-scope notes. `review_rules.py` explicitly maps every original graph edge to a judgment. Unmatched constructs fail rather than receiving an automatic status. `reviewed_decisions.json` records the reviewed graph bytes/edges and corpus hash.

Each age folder contains `validated_graph.html`, `edge_validation.xlsx`, `edge_validation.json`, `original_edges.json`, `manifest.json`, `supplied_papers.json`, `full_text_review.json`, `verification.json`, and reproduction entrypoints. Its `full_texts` directory is a relative link to the original supplied folder, avoiding three duplicate copies. Keep the age folders beside `2026 ADHD Papers` to preserve PDF links.

To rebuild existing reviewed outputs from the project root:

```sh
.venv/bin/python validation_2026_age8/build_report.py
.venv/bin/python validation_2026_age8/build_validated_graph.py
.venv/bin/python validation_2026_age32/build_report.py
.venv/bin/python validation_2026_age32/build_validated_graph.py
.venv/bin/python validation_2026_age45/build_report.py
.venv/bin/python validation_2026_age45/build_validated_graph.py
```

The report builder verifies original graph hashes, corpus membership, every PDF hash, and all selected quotations directly against PDF pages. It also round-trips all three Excel worksheets against their source values. These checks establish fidelity and provenance, not scientific certainty.

After a deliberate literature update, rerun `extract_corpus.py`, review the changed sources and affected rules, and only then regenerate `reviewed_decisions.json` with `review_rules.py`. Changing sources or graphs and rebuilding reports alone fails closed.
