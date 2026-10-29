# Edge reasoning and tiny stories

Current requirement, October 15, 2026. Every selected edge displays a reason and two concise fictional examples, without a review gate. This supersedes the earlier slow character approach and the subsequent example-withholding behavior.

## Exact presentation

### Cause → Effect · Positive/Negative

**Reason:** One to three simple sentences explaining cause → what changes → why that affects the outcome. Distinguish a plausible interpretation from evidence establishing causation.

**Example 1:** One to three concise fictional sentences showing a concrete event and its consequence.

**Example 2:** Another short fictional scenario showing the same mechanism in a different situation. Do not repeat the first example with a different name.

Provide examples for every arrow. For an ambiguous label, state the interpretation briefly inside the reason rather than blocking examples. Keep the original graph unchanged and do not turn a hypothetical interpretation into a scientific claim.

## Example: Symptom Severity → Functional Impairment · Positive

**Reason:** More frequent attention or impulse-control difficulties can interrupt following instructions, organizing work and completing activities. The symptom becomes functional impairment when it prevents someone from doing something they need or want to do.

**Example 1:** Mira understands the classroom assignment, but repeatedly loses her place in the instructions and starts again. By the deadline the work is unfinished, so an attention difficulty has become a practical obstacle.

**Example 2:** Noah keeps interrupting during a group activity and misses the agreed next step. The group cannot finish the shared task smoothly, showing how a symptom can affect participation rather than just appear on a checklist.

The examples are invented. Clinical context is available from [NIMH](https://www.nimh.nih.gov/health/topics/attention-deficit-hyperactivity-disorder-adhd); it does not validate the graph's numeric strength.

## Example: Early Life Nutrition → Genetic Risk · Negative

**Reason:** This example follows the source's developmental-vulnerability interpretation of the arrow, not a change in inherited DNA. Adequate early nutrition is imagined as avoiding an added nutrition-related developmental burden while genetic susceptibility stays unchanged.

**Example 1:** Mira is assumed to have inherited ADHD susceptibility. In this hypothetical example, adequate early nourishment avoids adding a nutrition-related developmental difficulty; the inherited susceptibility itself does not change.

**Example 2:** Noah has the same assumed inherited susceptibility across two imagined childhood situations. A nutrition-related deficiency adds a developmental challenge in one situation, while adequate nourishment avoids that extra challenge in the other.

[NHGRI gene–environment context](https://www.genome.gov/genetics-glossary/Gene-Environment-Interaction) distinguishes environmental influences from inherited susceptibility; it does not validate this graph's particular nutrition arrow.

## Implementation

- Rationale lookup uses the exact source, target and sign, never just the destination node.
- The library contains two illustrations for every one of the 124 unique signed relationships in the supplied snapshots. Illustrative does not mean scientifically validated.
- Snapshot review metadata is retained in exported source records but does not gate examples or produce review banners in the player.
- The model receives every selected edge and its locked interpretation and writes two examples for each, without skipping any relationship.
- Positive/negative headings, reasons, ordered relationship facts and source context are assembled outside the model.
- Examples contain twelve to seventy words, one to three sentences, and no numeric statistics, treatment dosing, guarantees or instructions. Hypothetical treatment responses are allowed for the supplied treatment mechanism.
- The player begins at the first edge. Back, Next edge, Replay, Play/Pause and the breadcrumb trace the exact selected route.
- Source context is separate from the short explanation. Modern studies do not validate historical snapshots, graph weights or the complete path.
- Cache version is `edge-examples-v5`; the cache key includes the rationale library. Old review-gated stories are not auto-loaded, while older saved stories remain exportable.

## Remaining review

Regex and schema checks cannot verify unrestricted prose or prove a sign is scientifically correct. Human review is still required, particularly for inferred social mechanisms, treatment illustrations, age generalization and mediated relationships. The existing one-to-seven-step discovery limit is unchanged by this storytelling revision.
