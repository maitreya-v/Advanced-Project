# 1970 age-45 graph validation

Existing reports replaced using the correct **1970_45 yo.py** graph: **37 edges**, **four supplied references only**.

## Status counts

- `supported`: 0
- `partially_supported`: 0
- `contradicted`: 0
- `mixed_evidence`: 0
- `insufficient_evidence`: 31
- `not_assessable`: 6

## Method and limitations

**Scope**: 1970_45 yo.py, 37 edges, using only four supplied papers (PMIDs 5538099, 5523436, 5491539, 4950109). Review direction, sign and reasoning; strength excluded.

**Result**: No adult edge receives causal support from these four pediatric/animal papers. Relevant pediatric statements are retained as context, not transferred as adult findings. Undefined signs/endpoints are not_assessable; other adult claims have insufficient_evidence. Missing support is not disproof.

**Historical scope**: The references and graph concern 1970. Historical MBD/hyperkinesis populations do not automatically equal the modern ADHD node. Clinical statements are distinguished from experimental results. No automatic penalty for a 1990 mismatch is applied.

**Age scope**: Schain ages 7-13; Obler approximately 7-12; Wikler initial eligibility 5-15. None studies adult patients aged 45. Family histories mentioning relatives are not adult outcome studies. Childhood age trends are not used to contradict adult severity or impairment claims.

**Source completeness**: Schain, Obler and Geller supplied articles are complete. Brain_function.pdf contains printed pp. 634-643; pp. 644-645 are absent. The preceding article fragment on p. 634 is excluded.

**Evidence limits**: Schain supplies clinical management statements and observational cases. Wikler is cross-sectional and reports drug-free results. Obler tests phobia desensitization, an intervention absent from this graph. Geller is an infant-rat lesion experiment, not human ADHD evidence.

**Status standard**: Only the six status_definitions values are allowed. Contextual associations become insufficient_evidence; undefined categorical signs/endpoints become not_assessable; clinical or narrower support becomes partially_supported. Contradicted does not imply a proven reversed causal edge.

**Status counts**: {"supported": 0, "partially_supported": 0, "contradicted": 0, "mixed_evidence": 0, "insufficient_evidence": 31, "not_assessable": 6}

**Evidence format**: Each edge has 9 fields. Evidence contains PMID, exact_excerpt, location (PDF/printed page and section), relevance. Shared references provide citations and URLs. Empty evidence means no directly relevant passage found; no missing evidence is invented.

**Excerpt transcription**: Line wrapping and end-of-line hyphenation normalized; quotations from the four supplied PDFs, with page locations. No title-only excerpts used as causal evidence.

**Original preservation**: Neither original graph modified. Original 1970 SHA-256: 0bfc025ea1f9a2f707a0cc47f3e0b1503efd0a18c9b14c982f7df23fcdd74e96

**Source isolation**: Only the four PDFs copied into this age folder are used. No additional bibliography records or adult studies were introduced. Earlier validation folders are untouched.

**Reproduce**: Run python validation_1970_age45/build_report.py. The reviewed judgments are stored in fulltext_review.py and checked against the actual 1970 source on every run.

## Fixed status definitions

- `supported`: Evidence supports the stated direction, sign and reasoning within the declared scope.
- `partially_supported`: Evidence supports only part of the claim, a narrower population/outcome, or a clinical mechanism rather than the full causal claim.
- `contradicted`: Relevant evidence opposes the claimed direction or sign; the observation specifies the scope and limitations of that opposition.
- `mixed_evidence`: Relevant evidence supports and opposes the same defined claim; differences in population or outcome alone do not establish conflict.
- `insufficient_evidence`: Available evidence does not establish or refute the causal claim.
- `not_assessable`: Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.
