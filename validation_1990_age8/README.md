# 1990 age-8 graph validation

Validation of **1990_8 yo.py**: **58 edges**, using only the **four supplied PDF files** in `1990 ADHD Papers`.

## Status counts

- `supported`: 0
- `partially_supported`: 6
- `contradicted`: 0
- `mixed_evidence`: 0
- `insufficient_evidence`: 48
- `not_assessable`: 4


## Method and limitations

**Scope**: 1990_8 yo.py, 58 edges, using only the four supplied PDF files in 1990 ADHD Papers. Direction, sign, and written reasoning were reviewed; numeric strength was excluded.

**Age Scope**: Evidence specific to children near age eight was preferred. Older-child and adolescent evidence was treated as partial when it did not report an age-eight estimate.

**Causal Standard**: Associations, reviews, and clinical recommendations were not automatically treated as proof of causal direction. Undefined categorical signs were marked not_assessable.

**Source Limits**: This is a validation against the supplied corpus, not a systematic review of all 1990 ADHD literature. A status of insufficient_evidence is not evidence that an edge is false.

**Strength**: The graph's numeric edge strengths were not validated.

**Duplicate**: No exact duplicate PDF files were found in the supplied corpus.

## Fixed status definitions

- `supported`: Evidence supports the stated direction, sign, and reasoning within the declared scope.
- `partially_supported`: Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.
- `contradicted`: Relevant evidence opposes the claimed direction or sign within the declared scope.
- `mixed_evidence`: Relevant evidence both supports and opposes the same defined claim.
- `insufficient_evidence`: Available evidence does not establish or refute the causal claim.
- `not_assessable`: Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.


## Reproduce

Run `python validation_1990_age8/build_report.py`. The script parses but never executes or modifies the graph. It verifies the source edge text, PDF hashes, citations, JSON output, and Excel structure.
