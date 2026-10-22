# 2026 age-45 graph validation

Validation of **2026_45 yo.py**: **70 edges**, using the supplied **159 PDFs / 158 distinct full-text documents** in `2026 ADHD Papers`.

Open [validated_graph.html](validated_graph.html) in a browser and click any edge for its status, decision and page-linked evidence. Colors and dashes encode validation; original widths retain unvalidated strengths.

Review [edge_validation.xlsx](edge_validation.xlsx) for the edge, reference and methodology worksheets. Machine-readable decisions are in [edge_validation.json](edge_validation.json), with provenance in [manifest.json](manifest.json) and checks in [verification.json](verification.json).

## Status counts

- `supported`: 2
- `partially_supported`: 22
- `contradicted`: 0
- `mixed_evidence`: 0
- `insufficient_evidence`: 39
- `not_assessable`: 7

## Method and limitations

**Scope**: 2026_45 yo.py: all 70 original edges reviewed against 159 supplied PDFs (158 distinct normalized full-text documents), 2,212 file pages. The year refers to the graph snapshot and supplied folder, not a claim that all papers were first published in 2026.

**Review Depth**: All supplied documents were screened by titles/first pages and available abstracts; relevant full-text passages were reviewed for graph claims. This is a targeted corpus validation, not exhaustive critical appraisal of all 2,212 pages or an external systematic review.

**Age Scope**: Adult ADHD evidence relevant to age 45 was preferred. Broad adult findings receive partial support when no exact-age effect or matching mechanism is established. Pediatric-only evidence and studies restricted to age 50+ are not transferred to this adult persona.

**Causal Standard**: Assess direction, sign, endpoint and written reasoning. Association, clinical recommendations, co-occurrence, service uptake and mechanistic plausibility are distinguished from experimental causal evidence. Null tests on different exposures/outcomes are not labeled contradictions.

**Strength**: Numeric edge strengths and the widths that encode them are retained for fidelity and are NOT validated effect sizes. All original edges, signs, reasoning, node positions and domain colors are preserved; only validation styling and evidence are added.

**Constructs**: Categorical variables require comparator coding; undefined treatment dependency/overdiagnosis pressure and treatment-receipt-versus-benefit mismatches are not assessable. Treatment effects do not establish diagnosis-only benefits.

**Duplicates**: The two 1-s2.0-S1087079226000754-main PDFs have different binary hashes but identical normalized page text and represent one sleep-intervention review. Duplicate copies are not independent evidence. Other reviews may share primary studies; 158 distinct documents are not 158 independent studies.

**Quotations**: PDF locations use one-based file pages. Native PDF reading order preserves columns; Unicode NFKC, soft-hyphen removal, end-of-line word dehyphenation and whitespace normalization are documented in extract_corpus.py. Every selected quotation is checked against actual source PDF-page text at build time.

**Provenance**: Graph SHA-256, every supplied PDF SHA-256, text hashes and reviewed corpus hash are checked. New/changed graphs or source PDFs require reassessment before rebuilding. full_texts is a relative directory link to the original supplied corpus; keep these folders beside 2026 ADHD Papers.

**Limits**: Insufficient evidence means this corpus does not establish the claim; it does not mean the edge is false. Supported refers to the declared qualitative pathway, not clinical recommendations or personalized treatment advice. No external papers were added.

## Reproduce

From the project root, run:

```sh
.venv/bin/python validation_2026_age45/build_report.py
.venv/bin/python validation_2026_age45/build_validated_graph.py
```

Requires the project environment (`pyvis`, `pymupdf`). Reports validate against the saved, manually reviewed decisions; they do not automatically re-review changed literature. Shared review sources and reproducible text extraction are in [paper_reviews/2026](../paper_reviews/2026/README.md). The `full_texts` directory links to the supplied PDFs; no original graph or paper is modified.
