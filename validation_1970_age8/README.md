# 1970 age-eight graph validation

Existing reports replaced using the correct **1970_8 yo.py** graph: **47 edges**, **four supplied references only**.

## Status counts

- `supported`: 0
- `partially_supported`: 3
- `contradicted`: 1
- `mixed_evidence`: 0
- `insufficient_evidence`: 36
- `not_assessable`: 7

## Method and limitations

**Scope**: 1970_8 yo.py, 47 edges, using only four supplied papers (PMIDs 5538099, 5523436, 5491539, 4950109). Review direction, sign and reasoning; strength excluded.

**Result**: 3 partially_supported edges: diagnosis to medication consideration (35), medication to symptom severity (40), medication to side effects (43). Edge 4 positive age sign is contradicted within the hyperactivity trend described, not all ADHD domains. No original edge fully supported as written.

**Historical scope**: The references and graph concern 1970. Historical MBD/hyperkinesis populations do not automatically equal the modern ADHD node. Clinical statements are distinguished from experimental results. No automatic penalty for a 1990 mismatch is applied.

**Age scope**: Schain ages 7-13; Obler approximately 7-12; Wikler initial eligibility 5-15. Age eight is within these ranges but no separate causal estimate at exactly eight is established.

**Source completeness**: Schain, Obler and Geller supplied articles are complete. Brain_function.pdf contains printed pp. 634-643; pp. 644-645 are absent. The preceding article fragment on p. 634 is excluded.

**Evidence limits**: Schain supplies clinical management statements and observational cases. Wikler is cross-sectional and reports drug-free results. Obler tests phobia desensitization, an intervention absent from this graph. Geller is an infant-rat lesion experiment, not human ADHD evidence.

**Status standard**: Only the six status_definitions values are allowed. Contextual associations become insufficient_evidence; undefined categorical signs/endpoints become not_assessable; clinical or narrower support becomes partially_supported. Contradicted does not imply a proven reversed causal edge.

**Status counts**: {"supported": 0, "partially_supported": 3, "contradicted": 1, "mixed_evidence": 0, "insufficient_evidence": 36, "not_assessable": 7}

**Evidence format**: Each edge has 9 fields. Evidence contains PMID, exact_excerpt, location (PDF/printed page and section), relevance. Shared references provide citations and URLs. Empty evidence means no directly relevant passage found; no missing evidence is invented.

**Excerpt transcription**: Line wrapping and end-of-line hyphenation normalized; quotations from the four supplied PDFs, with page locations. No title-only excerpts used as causal evidence.

**Original preservation**: Neither original graph modified. Original 1970 SHA-256: 6f972f4d1af4c1acd51bfc3ecf940be3f47f902c1b512d835d22df764eb2fa16

**Legacy files**: Other copied bibliography records and 1990_8 yo.original.py are legacy material and NOT validation inputs. Only the four specified PDFs are used. The 1990 validation folder is not modified.

**Reproduce**: Run python validation_1970_age8/build_report.py. The reviewed judgments are stored in fulltext_review.py and checked against the actual 1970 source on every run.

## Fixed status definitions

- `supported`: Evidence supports the stated direction, sign and reasoning within the declared scope.
- `partially_supported`: Evidence supports only part of the claim, a narrower population/outcome, or a clinical mechanism rather than the full causal claim.
- `contradicted`: Relevant evidence opposes the claimed direction or sign; the observation specifies the scope and limitations of that opposition.
- `mixed_evidence`: Relevant evidence supports and opposes the same defined claim; differences in population or outcome alone do not establish conflict.
- `insufficient_evidence`: Available evidence does not establish or refute the causal claim.
- `not_assessable`: Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.
