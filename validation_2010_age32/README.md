# 2010 age-32 graph validation

Validation of **2010_32 yo.py**: **62 edges**, using only the **25 supplied PDF files (24 unique documents)** in `2010 ADHD Papers`.

## Status counts

- `supported`: 0
- `partially_supported`: 17
- `contradicted`: 0
- `mixed_evidence`: 0
- `insufficient_evidence`: 38
- `not_assessable`: 7


## Method and limitations

**Scope**: 2010_32 yo.py, 62 edges, using only the 25 supplied PDF files in 2010 ADHD Papers (24 unique documents; one exact duplicate). Direction, sign, and written reasoning were reviewed; numeric strength was excluded.

**Age Scope**: Adult evidence was required for adult claims. Young-adult and general-adult evidence was treated as partial when it did not report an age-32 estimate. Pediatric findings were not transferred as adult causal proof.

**Causal Standard**: Associations, reviews, and clinical recommendations were not automatically treated as proof of causal direction. Undefined categorical signs were marked not_assessable.

**Source Limits**: This is a validation against the supplied corpus, not a systematic review of all 2010 ADHD literature. A status of insufficient_evidence is not evidence that an edge is false.

**Strength**: The graph's numeric edge strengths were not validated.

**Duplicate**: s12402-010-0036-9 (1).pdf is byte-identical to s12402-010-0036-9.pdf and was counted once as a unique document.

## Fixed status definitions

- `supported`: Evidence supports the stated direction, sign, and reasoning within the declared scope.
- `partially_supported`: Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.
- `contradicted`: Relevant evidence opposes the claimed direction or sign within the declared scope.
- `mixed_evidence`: Relevant evidence both supports and opposes the same defined claim.
- `insufficient_evidence`: Available evidence does not establish or refute the causal claim.
- `not_assessable`: Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.


## Reproduce

Run `python validation_2010_age32/build_report.py`. The script parses but never executes or modifies the graph. It verifies the source edge text, PDF hashes, citations, JSON output, and Excel structure.
