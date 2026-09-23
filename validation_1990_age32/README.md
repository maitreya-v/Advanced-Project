# 1990 age-32 graph validation

Validation of **1990_32 yo.py**: **53 edges**, using only the **four supplied PDF files** in `1990 ADHD Papers`.

## Status counts

- `supported`: 0
- `partially_supported`: 0
- `contradicted`: 0
- `mixed_evidence`: 0
- `insufficient_evidence`: 47
- `not_assessable`: 6


## Method and limitations

**Scope**: 1990_32 yo.py, 58 edges, using only the four supplied PDF files in 1990 ADHD Papers. Direction, sign, and written reasoning were reviewed; numeric strength was excluded.

**Age Scope**: Adult evidence was required for adult claims. The supplied papers study children or adolescents and were not transferred as causal proof for adults aged 32.

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

Run `python validation_1990_age32/build_report.py`. The script parses but never executes or modifies the graph. It verifies the source edge text, PDF hashes, citations, JSON output, and Excel structure.
