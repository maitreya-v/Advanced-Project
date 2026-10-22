# Directed Path Stories — Implementation Plan

Status: repository reconciliation and core path-story workflow implemented.

## Delivery update — October 15, 2026

Milestones 1–5 have an integrated implementation: bounded endpoint queries, route options, path isolation, source metadata, ordered playback and offline exports. The current request removes the review gate: every selected edge has one reason and two tiny fictional examples. All 73 tests pass, including 703 subtests. See `EDGE_REASONING_SPEC.md` for the current format.

The full-graph workflow is now explicit: first select Start and End by clicking graph nodes, then find routes in a second tab and generate a story for the chosen path. The full graph stays available for changing the query; playback isolates the route. New tests cover all graph records, click-event validation, stale selections, endpoint-to-route integration, on-demand generation and direct links with year/age context. A live node-click check exposed repetitive fallback text on the school route; authored scenes now pass preparation checks for every relationship in every supported snapshot, including overlapping concept names such as Gender / Gender Bias.

The rationale library supplies two examples for all 124 unique signed relationships. Previously gated entries now have concise, explicit interpretations and examples. Snapshot review statuses no longer block generation or display review banners. Local Qwen writes examples for every edge while reasons, signs and source facts stay locked. The `edge-examples-v5` cache prevents gated records from reappearing; older stories remain exportable as historical artifacts.

Remaining design refinements include scientific review of inferred mechanisms, card pagination and richer path-specific camera options. Milestone 6's full alternative/historical route comparison and milestone 7's participant study are not implemented. The older comparison workspace remains operational.

## 0. Completed prerequisite: one combined application

- Base: GitHub Advanced-Project `c5b06d3`.
- Integrated: local Qwen generation, saved stories, offline player and evaluation lab.
- Preserved: GitHub corpus, papers, review artifacts, validation panels and changed-route suggestions.
- Reconciled: Dashboard entry points, runtime dependencies, ignore patterns and test expectations.
- Verified: 35 tests passed, including 25 subtests.

Use this combined checkout for subsequent development. Keep old Deploy_AP copies as references until the combined app has been reviewed.

## 1. Add deterministic endpoint-driven route discovery

### Deliverables

Create `storytelling/paths.py` with graph construction, endpoint validation, bounded simple-route enumeration and deterministic path IDs. Return a structured discovery result, not a bare route list. Keep `story_paths.py` suggestions operational.

Add a new Path story workspace entry in `Dashboard.py` and a route-selection UI in `storytelling/path_ui.py`. Choose year/age and endpoints, expose the hop limit, list all completed results with pagination, and show completion status.

### Implementation decisions

1. Build from canonical snapshot records loaded by `storytelling/data.py`.
2. Add all snapshot nodes, then forward edges; never convert to an undirected graph.
3. Use deterministic adjacency and explicit simple-path traversal.
4. Check deadlines inside traversal expansion and prune by distance to the endpoint.
5. Separate “no bounded path” from “not reachable”.
6. Keep topology filters separate from purely visual fading.
7. Cache the query using snapshot fingerprint, endpoints, hop limit and filters.

### Checks

Real-data fixture: eight routes for Diagnosis Status to Quality of Life in 2026, age 8, at most five edges. Synthetic fixtures: wrong-way edges, isolated endpoints, direct routes, two equal-length alternatives, cycles, same start/end, unknown node, cutoff boundary and capped results.

### Exit condition

A viewer can choose every route in the verified eight-route query, see its full node sequence and preview it without a model call.

## 2. Analyze the selected route and unify evidence references

### Deliverables

Add path facts and an ordered edge-analysis table. Add a snapshot-aware evidence adapter, either `storytelling/evidence_adapter.py` or a small focused extension of `data.py`.

### Implementation decisions

1. Keep endpoint-derived stable relationship IDs.
2. Map report decisions by snapshot and source/target; do not copy explorer presentation IDs into the story schema.
3. Retain report source-hash checks and review scope.
4. Preserve contextual literature metadata separately.
5. Store evidence version separately from structural version.
6. Summarize reviewed and unreviewed edges explicitly; avoid a composite clinical-confidence score.
7. Explain negative edges in their local context; do not infer a quantitative whole-route effect.

### Checks

Verify all nine report-backed scenarios against source hashes. Test stale reports, unknown endpoints, missing reports and 2026 context-only literature. Check that adding review metadata does not change route identity. Verify that review-aware generated narration invalidates when relevant evidence changes.

### Exit condition

Every route step has inspectable source data and accurately scoped evidence, and saved-story IDs still resolve to the correct edges.

## 3. Build complete rule-based path stories

### Deliverables

Add `storytelling/path_director.py` with a path-specific schema, deterministic opening, one step per edge, synthesis and validation. Extend exports with a versioned `path` format while retaining existing change-story loading.

### Implementation decisions

1. Freeze route ordering before prose generation.
2. Produce a title and readable relationship explanation for each hop.
3. Use model framing in the opening and conclusion without repeating a long disclaimer at every step.
4. Include the exact ordered edge facts with each step.
5. Reject scene omissions, duplicates, reversed direction and invented numbers.
6. Validate titles and synthesis as well as scene bodies.
7. Use a separate path-story schema; leave the four-scene change-story contract intact.

### Checks

Verify direct, four-edge, five-edge and seven-edge stories. Confirm every source edge appears once and in order. Test negative signs, unsupported numbers, unrelated named concepts, altered endpoints, stale fingerprints and legacy saved-story compatibility.

### Exit condition

The viewer can read a coherent complete story for any discovered route without installing or running a model.

## 4. Add ordered visual tracing

### Deliverables

Extend `storytelling/player.py` and `player.html` with a path presentation branch, or a focused path template if that keeps legacy behavior clearer. Render the breadcrumb, Start/End markers, active edge, visited prefix and recap.

### Implementation decisions

1. Navigation runs inside the persistent graph component.
2. Preserve numeric edge width and the story's sign-color legend.
3. Use a halo or second drawing layer to emphasize the active edge.
4. Support manual stepping first; then add timed autoplay and pause.
5. Cancel timers when changing route, replaying or leaving the player.
6. Respect reduced motion; make automatic camera following optional.
7. Keep the full route legible in a textual breadcrumb.

### Checks

Use a real browser for screenshot and interaction QA. Confirm exactly one active edge, correct visited prefixes after Back, reset after switching paths, keyboard navigation, narrow-screen layout, reduced motion and offline export. These frontend behaviors need browser checks beyond Python schema tests.

### Exit condition

A person can follow the story from its first node to its last and identify the corresponding edge at every step.

## 5. Add optional local Qwen narration

### Deliverables

Reuse `LocalOllama` from `storytelling/director.py` to rewrite locked path facts. Add concise audience and question controls. Keep on-demand generation and a checked baseline fallback.

### Implementation decisions

1. Send only the selected route and needed scope/evidence facts.
2. Ask for the path schema, with every ordered step required.
3. Permit one bounded repair attempt, following the existing generator pattern.
4. Rebuild visuals from checked facts, not model-provided graph instructions.
5. Cache per route and narration settings.
6. Preserve the current baseline when generation times out or fails checks.
7. Do not generate all route stories automatically when options are listed.

### Checks

Mock client tests for route fidelity, omissions, invented relationships, evidence overclaims and timeout fallback. Then generate at least one actual short, one five-hop and one side-effect example locally; record model, latency, repair rate and human review findings.

### Exit condition

Optional generated prose is more readable while following exactly the same route and facts as the deterministic baseline.

## 6. Compare alternatives and historical structure

### Deliverables

Add side-by-side selected routes with shared prefixes, branch points, merge points and independent source identities. Extend the existing route-suggestion mode to drill into the full endpoint catalog.

### Implementation decisions

1. Compare alternatives within one snapshot first.
2. Compare across years with a fixed age next.
3. Treat sign/strength changes as meaningful even when topology is unchanged.
4. Preserve unchanged routes and direct shortcuts in the catalog.
5. Label matching heuristics; let viewers override the suggested route pairing.
6. Avoid a route built from a union of different snapshots' edges.

### Checks

Persisting shortest path with a changed longer alternative; identical routes with changing strengths; one absent route; endpoint absent in one scenario; no route within a cutoff but reachability beyond it; separate age scenarios.

### Exit condition

Viewers can explain how two stories differ without mistaking a selected comparison for exhaustive historical or causal evidence.

## 7. Evaluate understanding

Extend the existing evaluation protocol with path questions:

1. What were the starting and ending concepts?
2. Which concept came immediately after Treatment Access?
3. What does the arrow direction mean in this model?
4. Does a negative edge always imply a worse final outcome?
5. Which relationship on this route lacks snapshot-specific review?
6. Is the numeric strength a probability or measured effect size?
7. Is a route absent within five hops necessarily impossible in the graph?

Compare static highlighted route, deterministic traced story and generated traced story. Keep route content and evidence panels matched across conditions so the comparison tests narration and tracing rather than different facts. Use a small pilot to identify confusing questions before running the main study. Report actual participant counts and results; graph fidelity and clinical validity remain separate outcomes.

## Recommended delivery order

Ship milestones 1–4 as the first complete demo. Milestone 5 adds generated language; milestone 6 adds richer exploration. Conduct a small pilot before expanding the study in milestone 7.

The highest-value first demonstration is the eight-option 2026 age-8 query with a medication route, a school route and a side-effect route. It demonstrates directed traversal, alternative explanations and balanced selection in a small inspectable example.

## Decisions resolved by this plan

| Question | Default |
|---|---|
| Must the viewer choose endpoints? | Editable endpoints plus optional suggestions |
| What does “all paths” mean? | Every simple route within explicit query bounds; partial status when limits interrupt |
| How long can routes be? | Default five edges; MVP range one to seven |
| Do cycles become repeated story steps? | No; dedicated loop mode later |
| Should the model find paths? | Graph code finds and analyzes them; the model rewrites checked narration |
| Should every option be generated immediately? | No; generate only the selected route on request |
| Which local model should be used? | Reuse the existing Qwen/Ollama client and evaluate its path stories |
| Is one route clinically better than another? | No such conclusion is inferred from authored weights or editorial scores |
| Does this require a frontend rewrite? | No; retain Streamlit and vis-network for the MVP |
| Does this require multiple agents? | No; the existing bounded director is sufficient initially |
