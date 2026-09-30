# 1990 age-32 graph validation

Validation of **1990_32 yo.py**: **53 edges**, using only the **four supplied PDF files and 25 saved PubMed HTML abstracts** in `1990 ADHD Papers`.

## Status counts

- `supported`: 0
- `partially_supported`: 3
- `contradicted`: 0
- `mixed_evidence`: 0
- `insufficient_evidence`: 44
- `not_assessable`: 6


## Method and limitations

**Scope**: 1990_32 yo.py, 53 edges, using the four supplied PDF files and 25 saved PubMed HTML abstracts in 1990 ADHD Papers. Direction, sign, and written reasoning were reviewed; numeric strength was excluded.

**Age Scope**: Adult evidence is required for adult claims. The added adult review is treated as partial clinical context without an age-32-specific estimate. Child and adolescent studies are not transferred as adult causal proof.

**Causal Standard**: Associations, reviews, and clinical recommendations were not automatically treated as proof of causal direction. Undefined categorical signs were marked not_assessable.

**Source Limits**: This is a validation against the supplied corpus, not a systematic review of all 1990 ADHD literature. A status of insufficient_evidence is not evidence that an edge is false.

**Strength**: The graph's numeric edge strengths were not validated.

**Duplicate**: No exact duplicate PDFs or duplicate PMID records were found. HTML pages are deduplicated by PMID; repeated sentences in an abstract are not independent findings.

**Html Scope**: HTML evidence is restricted to the main English abstract of each saved record, excluding similar/cited articles. All 25 records are dated 1990. Abstract-only limitations are retained; the side-effect abstract (PMID 2196520) is marked truncated and repeats a passage.

**Adult Scope**: The adult review (PMID 2251528) supplies clinical context, not a controlled treatment estimate or specific results at age 32 or 45. Pediatric findings are not transferred to adult graphs.

## Fixed status definitions

- `supported`: Evidence supports the stated direction, sign, and reasoning within the declared scope.
- `partially_supported`: Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.
- `contradicted`: Relevant evidence opposes the claimed direction or sign within the declared scope.
- `mixed_evidence`: Relevant evidence both supports and opposes the same defined claim.
- `insufficient_evidence`: Available evidence does not establish or refute the causal claim.
- `not_assessable`: Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.


## Reproduce

Run `python validation_1990_age32/build_report.py`. The script parses but never executes or modifies the graph. It verifies the source edge text, PDF and HTML hashes, abstract excerpts, citations, JSON output, and Excel structure. Rebuild the interactive graph with `python validation_1990_age32/build_validated_graph.py`.
