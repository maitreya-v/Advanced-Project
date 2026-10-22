# Directed Path Stories — Product and Technical Specification

Date: October 15, 2026. Status: core path-story workflow implemented; comparison and study extensions remain proposed.

## Implementation update

The Path story workspace starts with the entire graph and click-to-select Start/End controls. Find directed routes opens bounded route options and isolated playback. Every arrow displays a concise Reason and two fictional examples, without review banners or withheld examples. Ambiguous definitions are handled through explicit interpretations rather than blocking playback. Optional local Qwen writes examples for every edge while source facts stay unchanged. See `EDGE_REASONING_SPEC.md` and `IMPLEMENTATION_PLAN.md` for current behavior.

The original sections below retain the broader design target. Current discovery provides a searchable route selector and complete route table rather than twenty-row card pagination. Playback uses a fitted path-specific snake layout. Advanced alternative comparison, conversational branch exploration and a path-specific participant study remain future increments.

## 1. Product goal

Let a viewer choose a starting concept and an outcome, see the distinct directed routes connecting them, choose one route, inspect its relationships, and watch a story follow that exact route from beginning to end.

The central unit is an ordered path. Narrative should explain each transition and arrive at the chosen outcome. A collection of interesting but disconnected changes does not satisfy this mode.

Primary workflow:

```text
Choose year and age → Choose start and end → Find paths
→ Inspect route options → Select a route → Analyze path
→ Read or generate story → Trace the route → Compare alternatives
```

Keep automatic suggestions for viewers who do not know where to start. Suggestions should lead into the same route-selection flow.

## 2. Verified current state

The assessment covers the current GitHub commit `c5b06d3`, the Desktop Advanced_Project folder, and the workspace mirror. See `SYNC_REPORT.md` for the reconciliation.

| Capability | Existing implementation | Remaining gap |
|---|---|---|
| Directed graph | Snapshot scripts use `directed=True` and `arrows="to"`; NetworkX route discovery uses `DiGraph` | Make direction visually explicit during ordered playback |
| Snapshot coverage | Twelve scenarios: 1970, 1990, 2010, 2026 × ages 8, 32, 45 | A route must stay inside one scenario unless comparison is explicitly requested |
| Alternative routes | `story_paths.alternative_routes`: up to four shortest simple routes per reachable endpoint pair, cutoff default five edges | Endpoint-driven catalog of each route within the viewer's chosen bounds |
| Suggested stories | `discover_stories`: changes between years, one representative comparison per endpoint pair, maximum thirty suggestions | Preserve alternatives and unchanged routes; list route-level choices |
| Route prose | `story_paragraph`: deterministic paragraph assembled from edge hover explanations | Ordered scenes and stronger distinction between authored explanation and observed outcome |
| Highlighting | `highlight_path`: highlights the complete route simultaneously, sets selected width to five | Trace one edge at a time while preserving numeric-width meaning |
| Generated stories | Local Qwen3 via Ollama; up to four selected graph-change scenes | A path-specific schema that covers every hop in order |
| Player | Persistent vis-network component; overview, scenes, recap, zoom and evidence | Ordered traversal state and path progress |
| Evidence | GitHub snapshot review reports; separate local story literature registry | Shared snapshot-aware evidence adapter without changing canonical relationship IDs |
| Study tools | Existing 24-case comparison evaluation | Path-specific comprehension questions and route-matching checks |

All twelve inspected graphs contain directed cycles. The story engine must not assume a directed acyclic graph or run a topological sort as its route-finding algorithm.

In the 2026 age-8 graph there are 48 nodes and 68 directed edges. For `Diagnosis Status → Quality of Life`, exhaustive enumeration found eight simple directed paths with at most five edges. The present four-route sampler cannot represent all eight. The full verified list appears in `STORY_EXAMPLES.md`.

## 3. Scope and terminology

- A **route** is an ordered sequence of nodes connected by forward directed edges.
- A **simple route** does not repeat a node. Cycles remain in the graph but are not repeatedly traversed.
- A **hop** is one edge, so a five-hop route has six nodes.
- A **path story** explains one selected route in one snapshot.
- A **comparison story** explains differences between identified routes in two scenarios.
- An **editorial score** helps order options. It is separate from model strength and evidence review status.

“Each path” means each simple directed route matching the visible snapshot, endpoints, hop limit and filters, subject to explicitly reported computation limits. The application must never present four sampled routes as an exhaustive list.

Start and end are viewer-selected concepts. They need not be graph roots or leaves: feedback loops and multiple routes make automatic root-to-leaf assumptions unsuitable here.

### MVP includes

1. Single-snapshot endpoint selection and explicit direction.
2. Bounded route discovery with truthful completion status.
3. One selectable option per distinct discovered route.
4. Deterministic path analysis and a complete baseline story.
5. Start-to-end tracing with text and visual synchronization.
6. Optional local Qwen rewriting of the checked baseline.
7. JSON and standalone HTML export.

### Later increments

Route comparison across years; scenario comparison across ages; branch exploration; evidence filters; richer audience controls; feedback-loop stories; participant studies.

Do not introduce new numerical causal inference, patient-specific recommendations, or whole-graph exhaustive route discovery as part of the MVP.

## 4. Viewer experience

### A. Choose the story

Controls: year, age, starting concept, ending concept, maximum hops. A new session starts with 2026, age 8 and five hops, with no endpoints preselected; links from the explorer preserve its selected year and age. The full graph appears first. Click a node to set Start, then another to set End, or use the corresponding dropdowns. Set Start / Set End, Fit whole graph, zoom and Clear selections remain available.

The **Find directed routes** action performs graph analysis without contacting the model, then opens **2. Routes and stories**. Selecting a route isolates it in the player. **Generate story for this path** requests new local Qwen narration for that exact route. Return to **1. Full graph and endpoints** to change the query; changed endpoints or filters invalidate old results. Optional future presets such as recognition, school support, treatment access and side effects should fill editable controls, not silently impose a route.

Display active scope next to results: “2026 · Age 8 · Up to 5 directed edges · All signs”. Use the complete selected snapshot by default. If a graph display threshold is applied to route discovery, make that an explicit toggle and include it in the scope label.

### B. Choose a route

Use a scrollable route list or cards. Each option includes:

- Full ordered node sequence, with a compact meaningful title.
- Hop count, intermediate domains and whether a direct shortcut exists.
- Per-edge signs and authored strengths, available without generating a story.
- Evidence coverage split into report-reviewed, contextual-literature and unreviewed relationships.
- A selection action that previews the complete route on the graph.

Show all routes when the result is small. Paginate larger complete results, initially twenty per page. Ranking changes order, not eligibility. Provide “Shortest first”, “Domain”, “Fewest unreviewed edges”, and “Route title” sorting.

Display completeness prominently:

| State | Wording |
|---|---|
| Search exhausted | “8 routes found within 5 edges” |
| Path count limit hit | “500 routes found; additional routes may exist. Narrow your search.” |
| Time limit hit | “Search stopped at the time limit; showing routes found so far.” |
| No bounded route | “No directed route found within 5 edges.” |
| End unreachable even without cutoff | “This outcome is not reachable from the selected start in this graph.” |

Distinguish paths found from rows shown. A twenty-row page must not imply only twenty routes exist. Do not label a partial result the global “best routes”.

### C. Analyze the selection

Show a persistent route breadcrumb and an edge table: step, source, target, sign, authored strength, original explanation, source file and review status. The viewer should understand the route before requesting prose.

Include three short analyses: what the route connects; which intermediate concepts distinguish it; what is unknown about its evidence. A minimum or mean edge strength may be provided as a descriptive summary, labeled precisely. Avoid naming this an estimated bottleneck or real-world effectiveness score.

### D. Play the story

Layout: graph canvas beside narration; ordered breadcrumb above; overview, numbered steps and recap below. Provide Next, Back, Replay, Play/Pause, Fit route, Explore here and Return to story.

At the opening, mark Start and End and preview the route faintly. At each step, illuminate the next directed edge, mark the arrived node and retain the visited prefix. Keep future route segments visible but subdued; remove unrelated nodes and edges from the player entirely. The full graph remains available in the first tab. At recap, display the complete traced path.

Keep the entire route in view initially. Offer “Follow camera” as an optional control; do not force a distracting camera jump on every hop. A path-local left-to-right view is useful as an alternative to the stable whole-graph layout.

Width continues to encode authored strength. Use a halo or separate overlay for active traversal. Color in the main story indicates sign; use a separate badge for evidence status. The explorer can retain its existing validation color convention, with its own legend.

## 5. Discovery algorithm and limits

Build a `DiGraph` from canonical snapshot edges. Include isolated snapshot nodes explicitly. Validate endpoints, cutoff and filters before searching.

Recommended default maximum hops: five; supported MVP range: one to seven. Include one-edge direct routes. Reject identical start/end selections with a clear message; feedback-loop exploration is a separate future mode.

For one selected endpoint pair, enumerate simple paths using a deterministic bounded depth-first search, with NetworkX `all_simple_paths` as the correctness reference. Lexically order adjacency for reproducibility. Reachability checks and reverse distance-to-target pruning can avoid exploring branches that cannot reach the destination within the remaining hops.

Proposed interactive limits: 500 returned routes and one second of search work, configurable and measured on the demo machine. These are design targets, not established benchmark results. Check cancellation/time budget inside traversal expansion; checking only after a yielded route can leave the application blocked on a long unsuccessful branch.

When stopping at the route cap, use lookahead to distinguish exactly 500 completed routes from 500 plus undisplayed routes. Record `complete`, `stop_reason`, `returned_count`, and `total_count`; exact total is null when unknown. Support longer offline searches later rather than silently blocking the interface.

Use shortest-route sampling for automatic suggestions and explicitly label it as sampling. Keep the existing changed-route ranking for comparison suggestions; it should not remove routes from an endpoint-selected catalog.

NetworkX defines simple paths as having no repeated nodes and cutoff in edge counts; its documentation warns that the total number of simple paths can grow factorially. These motivate the bounds and completion contract. [NetworkX all_simple_paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.simple_paths.all_simple_paths.html). The existing alternative-route method uses the separate shortest-simple-path interface. [NetworkX shortest_simple_paths](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.simple_paths.shortest_simple_paths.html).

## 6. Analysis and interpretation

Compute path facts before writing a story:

1. Ordered canonical nodes and edge IDs.
2. Edge-by-edge signs, strengths and explanations.
3. Intermediate domains and domain transitions.
4. Source and review coverage for this exact scenario.
5. Shared prefixes, suffixes and branch points with alternatives.
6. Optional before/after presence for a separately chosen comparison.

Do not multiply edge strengths into a probability or causal effect. Do not treat stronger authored weights as stronger scientific evidence. An edge with negative sign does not automatically mean a bad outcome: reducing Functional Impairment can be part of a route toward Quality of Life.

If a symbolic product of signs is ever shown, label it “encoded sign pattern under a simple chain assumption” and keep it out of the default narrative. Feedback, confounding, nonlinearity and measurement definitions prevent treating the sign product as a demonstrated real-world net effect.

Use the original explanations as authored model statements. Even an original explanation containing “likely” does not make its numeric strength a probability. The story must preserve uncertainty rather than intensify that wording.

## 7. Evidence integration

Retain endpoint-derived canonical `e_...` IDs in story data. Existing explorer validation IDs are presentation IDs; map review decisions by snapshot and source/target rather than replacing canonical IDs.

The evidence adapter must:

- Check the report year, age, source hash and edge endpoints using the existing safeguards.
- Attach the snapshot-specific review decision and observation to the matching relationship.
- Preserve the separate contextual literature registry and its scope labels.
- Show “No snapshot-specific report” for 2026 while retaining any contextual citations.
- Distinguish source relevance, relationship review and validation of a complete route.
- Surface stale or unavailable review metadata without presenting it as current.

The current reports state that strengths were not assessed. A supported edge label therefore does not validate its numeric strength. Evidence for each edge also does not establish a complete mediated effect for the path.

Separate structural and evidence fingerprints. Structural changes invalidate route and narration caches; evidence changes refresh evidence panels and invalidate generated text that discusses evidence. Export both versions so a saved story is reproducible.

## 8. Story construction

Build a deterministic baseline with one structured explanation per hop. The format is **Cause → Effect · Positive/Negative**, **Reason**, **Example 1**, **Example 2**. Each reason and example contains one to three concise sentences. The earlier slow fictional-character style and minimum-fifty-five-word chapters are superseded. The four-scene limit belongs to change stories and must not truncate route coverage.

Use the exact source/target/sign to select a mechanism, not a destination-only template. A concrete event and consequence should explain the arrow, without repeated doctor conversations, questionnaires or unfinished-story metaphors. Give two fictional examples for every selected relationship; clarify ambiguous labels within the reason rather than adding a review gate.

Local Qwen can write two new examples for every arrow, but cannot rewrite reasons or change source facts. Fictional treatment responses may illustrate supplied mechanisms, without being patient observations, treatment advice or guaranteed outcomes. Generation is optional and explicitly requested; listing or switching route options performs no inference.

The model can select wording and explanatory emphasis. It cannot change endpoints, reorder hops, invent nodes, assign new weights, remove inconvenient edges or invent source citations. A comparison story is a separate schema with explicit snapshot identity per route.

Keep the old change-story generator working. Add a discriminated `path` story schema rather than loosening its existing fact-validation rules.

### Earlier prototype record

The following is retained as design history. The implemented `edge-reasoning-v4` record uses `chapters` containing `edge_id`, `reason`, `examples`, `status`, `title`, `relationship` and `mechanism_sources`; see `EDGE_REASONING_SPEC.md`.

```json
{
  "version": "path-v1",
  "mode": "path",
  "snapshot": {"year": 2026, "age": 8, "structural_fingerprint": "..."},
  "path_id": "p_...",
  "node_ids": ["Diagnosis Status", "Treatment Access", "Behavioral Therapy", "Functional Impairment", "Quality of Life"],
  "edge_ids": ["e_...", "e_...", "e_...", "e_..."],
  "query": {"max_hops": 5, "filters": {}},
  "discovery": {"complete": true, "returned_count": 8, "stop_reason": "exhausted"},
  "origin": "rule-based",
  "opening": {"title": "From recognition to daily life", "narration": "..."},
  "steps": [{"index": 0, "edge_id": "e_...", "title": "Access enters the story", "narration": "..."}],
  "closing": {"title": "The route as a whole", "narration": "..."},
  "evidence_fingerprint": "..."
}
```

The example `steps` array is abbreviated; a valid saved story must contain every ordered edge. Create `path_id` from snapshot identity, structural fingerprint and ordered edge IDs. Cache narration by path ID, audience, question, story format, generator/prompt version and evidence fingerprint when evidence is discussed. Route-discovery caches also include cutoff and every topology-affecting filter.

## 9. Grounding and playback checks

Reject a story unless:

- Its route begins and ends at the requested concepts.
- Every adjacent node pair has the stated forward edge in the chosen snapshot.
- Nodes do not repeat, and hop count matches the route.
- Scene order exactly matches edge order; every edge is covered once.
- Numbers, signs and relationship names agree with the computed facts.
- Titles, opening and conclusion obey the same grounding rules as step narration.
- Claims about evidence refer to attached review records with the correct scope.
- Age scenarios are not narrated as one person's life history.

Schema checks and literal matching cannot prove semantic accuracy of unrestricted prose. Keep a deterministic fallback and human review for research-facing generated narratives. If model generation fails, retain the valid baseline and identify its origin.

Player state is `overview → step 0 → ... → step n−1 → recap`. At step `i`, the active edge is `edge_ids[i]` and the arrived node is `node_ids[i+1]`. Visited edges are the prefix through `i`. Backward navigation reconstructs the prefix rather than leaving stale highlights. Pause cancels timers; changing routes stops old playback and resets to overview.

The exported story embeds the graph library and checked data. Playback, replay and route inspection should work offline. Add a textual route list, keyboard controls, adequate active-edge contrast and reduced-motion behavior. Network events and camera methods are available in the existing library. [vis-network documentation](https://visjs.github.io/vis-network/docs/network/).

## 10. Comparison mode

After single-route MVP, allow the same endpoint pair in two years while holding age fixed. Enumerate routes independently in each snapshot. Label exact matches as persisted; identify added or absent routes within the declared bounds; show changes in edge sign/strength even when route topology persists.

A route absent under a cutoff is not necessarily unreachable. A replacement-looking route does not prove the old mechanism was replaced in reality. Do not manufacture a path by taking some edges from 2010 and other edges from 2026.

Pair alternatives using shared nodes/edges with the pairing rationale shown. Allow viewers to choose a different pairing; the highest-ranked comparison is editorial, not definitive. Age comparisons likewise remain comparisons between separate scenarios.

## 11. Recommendations and ideation

| Priority | Idea | Why it helps | Constraint |
|---|---|---|---|
| P0 | Endpoint selector plus route catalog | Directly fulfills the requested start-to-end workflow | Always report search bounds and completeness |
| P0 | Numbered breadcrumb plus cumulative trace | Lets viewers connect prose to direction | Keep weights visually unchanged |
| P0 | Rule-based story before model rewriting | Gives an immediate dependable demo | Label generated and baseline origins |
| P0 | One coherent route per story | Makes the narrative interpretable | Avoid disconnected high-ranked facts |
| P1 | Compare two routes with same endpoints | Reveals why alternatives tell different stories | Keep story scope clear |
| P1 | Shared-prefix and branch-point views | Explains where routes diverge | Do not merge distinct narratives silently |
| P1 | Balanced route suggestions | Exposes side effects and barriers as well as support | Do not rank only favorable narratives |
| P1 | Evidence drawer at each hop | Makes limitations inspectable | Review relevance differs from quantitative validation |
| P1 | Left-to-right route view | Clarifies traversal when the global layout is tangled | Retain a link to the whole graph |
| P1 | Guided endpoint presets | Helps new viewers choose meaningful questions | Presets remain editable |
| P2 | “Why this route?” explanation | Makes editorial recommendations transparent | Show the actual ranking ingredients |
| P2 | Audience styles: brief, classroom, research | Adapts wording while retaining facts | Scope and uncertainty survive rewriting |
| P2 | Optional fictional vignette | Makes the explanation relatable | Label invented events and distinguish hypothetical responses from observed clinical outcomes |
| P2 | Side-by-side path evidence map | Helps Madhura review weak coverage | Do not average review labels into clinical certainty |
| P2 | Professor presentation export | Supports demonstrations and feedback | Include graph scope and source provenance |
| P2 | “What other route reaches this outcome?” | Encourages exploration after a story | Recompute directed routes, not invented continuations |
| P3 | Feedback-loop explorer | Explains cycles present in every snapshot | Separate repeated traversal from simple-path stories |
| P3 | Structural edge-exclusion sandbox | Shows how connectivity changes if an edge is hidden | Label as graph surgery, not a treatment counterfactual |
| P3 | Longitudinal route timeline | Tracks represented structure across all four years | Same-age snapshots remain separate historical scenarios |

Start with the eight verified diagnosis-to-quality-of-life options. They include a direct summary link, school-support routes, treatment routes and a side-effect route. This is a stronger demonstration than an automatically selected favorable path alone.

## 12. Acceptance criteria

1. The verified 2026 age-8 diagnosis-to-quality-of-life query returns all eight simple routes within five hops when search completes.
2. The direct route is included; the four-route sampler is never labeled exhaustive.
3. Selecting an option previews that exact ordered route.
4. A story for a five-edge route covers all five edges in order, followed by a recap.
5. Step navigation and tracing agree; replay and route switching clear stale state.
6. Signs, strengths and source metadata match source records; edge width is not overwritten for attention.
7. Review decisions are matched to the correct snapshot while canonical IDs remain stable.
8. Missing paths, cycles, cutoffs, partial results and disconnected graphs have explicit behavior.
9. Valid baseline stories remain available without Ollama; failed rewriting preserves them.
10. Standalone exports open and play offline with keyboard and reduced-motion support.
11. Existing corpus, validation, change-story and evaluation tests continue to pass.
12. User testing measures directed-route understanding separately from whether the underlying graph is clinically supported.
