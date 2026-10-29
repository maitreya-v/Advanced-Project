# Horizontal chains — implementation and handoff

## Dashboard 2.0 integration

The chain prototype is now available inside `Dashboard_2_0.py` with independent
Year A/Age A and Year B/Age B selectors. Any pair of scenarios can be compared,
including changes to both year and age or reverse ordering. **Choose routes**
sets independent Start A/End A and Start B/End B endpoints and routes, with a
shared maximum step limit. Endpoint edits refresh and focus their own chain;
the other scenario retains its route and selected step. The graph's
minimum-strength slider filters both chains. Unavailable routes show the
scenario and requested endpoints instead of a previous chain.

The comparison summary and **Changes** tab report added/removed nodes and directed
edges, sign changes, and A/B strengths with B-minus-A deltas across the complete
snapshots. Chain filters do not change these differences. Each chain has its own
step state. Select an arrow or Scenario A/B and use the **Story / Validation**
toggle for its authored explanation/examples or its own year/age-specific
paginated evidence. The chosen mode persists while navigating between steps.

Named saves, the Saved chains library, frozen saved views, reload links and
standalone HTML/JSON exports are available in the chain panel. Saved records
retain their own evidence scenario when the live graph changes. Existing
two-chain records reopen as Scenario A and B, while legacy single-chain saves
also work. Route selection is independent for each side; the app never combines
edges from different scenarios. The standalone prototype remains available.
See [Dashboard 2.0](DASHBOARD_2_0.md) for current usage and checks.

The original prototype handoff below describes the branch before this integration.

Maitreya's chain implementation is on `codex/horizontal-chain-prototype`: horizontal rendering, single-snapshot queries, selected-step text, persistent save/list/reopen, JSON/HTML exports and the legacy-export compatibility fix. The separate workspace is `Chain_Prototype.py`. `Dashboard.py`, `Dashboard_2_0.py`, the existing player and shared validation helpers keep their existing interfaces.

Run from the repository root:

```sh
python -m streamlit run Chain_Prototype.py --server.port 8504
```

The default is 2026 / age 8, Diagnosis Status → Quality of Life. The prototype initially selects a multi-step medication route to demonstrate a chain longer than three nodes. Every route returned by the bounded search is available in the route selector. No model service is required.

## Implemented

- One horizontal row with internal scrolling, ordered nodes, directed arrows, signs and original authored strengths.
- Arrow selection and Previous/Next controls. Arrow keys, Home/End and native button activation support keyboard navigation.
- Selected-step reasons and two existing fictional examples, with child/adult text determined by the scenario.
- Single-snapshot year, age, hop and strength controls. Endpoints remain selected when the scenario changes; route selection and active step reset for the new query.
- Separate missing-endpoint, filtered/no-route and incomplete-search states.
- Events bound to the scenario fingerprint, query, route and stable relationship ID; stale events cannot reopen text from another scenario.
- Persistent named saves in `saved_chains/`, listed in the sidebar and preserved across browser/server restarts. Identical saves reuse the original record instead of overwriting its creation time.
- A frozen Saved chains view, with a `?saved_chain=<id>` URL that reopens after a browser reload. Switching back to Explore restores the live filters and selected route.
- JSON records and standalone HTML containing the chain, every step's reason/examples, navigation and original explanation/review text. HTML has no external scripts or application-server dependencies.
- A storage/export contract that accepts one chain or two separately scoped chains for Arnav's future comparison view.
- Atomic file writes, source validation on reopen, readable failure messages, and working downloads when saving to the host fails. Invalid/stale files are preserved rather than overwritten.
- Both bundled legacy story formats export again after the 2026 review import. Original graph facts, scenario identity, captured review metadata and original cache keys remain checked.

## Contract for Arnav

Use snapshots from `storytelling.data.load_snapshots()`. The graph objects returned by `dashboard_v2_graph` have different IDs and omit fields needed by the route engine. Do not pass those presentation objects into the chain API.

```python
from storytelling.chain_core import query_chains, build_chain, apply_chain_selection
from storytelling.chain_view import chain_component

result = query_chains(snapshot, start, end, max_hops=5, minimum_strength=threshold)
# Handle missing endpoints, no routes and incomplete discovery before selecting a route.
chain = build_chain(snapshot, selected_route, max_hops=5, minimum_strength=threshold)
apply_chain_selection(None, chain, st.session_state, key="chain_a")
event = chain_component(
    chain=chain, selected_step=st.session_state["chain_a_step"],
    key="chain-a-view", default=None,
)
if apply_chain_selection(event, chain, st.session_state, key="chain_a"):
    st.rerun()
step = chain["steps"][st.session_state["chain_a_step"]]
```

`query_chains` preserves the existing `discover_routes` results: `paths`, `complete`, `stop_reason`, `returned_count`, `total_count`, `reachable` and `query`. It adds `scenario`, `query_id`, `state` (`ready`, `no_route`, `missing_endpoints`) and `missing_endpoints`.

`build_chain` returns the `horizontal-chain-v1` record:

| Field | Meaning |
| --- | --- |
| `scenario` | `year`, `age`, structural `fingerprint` |
| `chain_id` | Existing fingerprint-bound route ID |
| `query_id` | Scenario plus endpoints, hop limit and minimum strength |
| `query` | `start`, `end`, `max_hops`, `minimum_strength` |
| `node_ids`, `edge_ids` | Exact route ordering |
| `nodes` | Ordered display nodes: ID, label, domain, color |
| `steps` | Ordered index, stable edge ID, source, target, sign, strength, original explanation, reason, two examples, optional snapshot review |
| `origin`, `fiction_note` | Existing story provenance/illustration label |

Selection events carry `version`, `scenario`, `chain_id`, `query_id`, `step_index`, `edge_id` and a unique `event_id`. `apply_chain_selection` resets state when the query/route changes, validates events and deduplicates reruns. Use different state/component keys for A and B. Validation lookup should map by **year + age + source + target** to the dashboard's report IDs.

Arnav's comparison layer can call `query_chains` independently for any A/B scenarios. The component does not impose the older comparison engine's fixed-age/fixed-year restriction. It does not combine edges from separate scenarios.

## Saving and exports for Arnav

```python
from storytelling.chain_store import create_saved_chains, save_chains, load_saved_chains
from storytelling.chain_export import saved_chains_html

record = create_saved_chains([chain_a], "My chain", snapshots=snapshots)
path = save_chains(record, snapshots=snapshots)
reopened = load_saved_chains(path, snapshots=snapshots)
html = saved_chains_html(reopened, snapshots=snapshots)
# For a comparison, use [chain_a, chain_b]. Each retains its own scenario and route.
```

`saved-chains-v1` records contain `save_id`, `name`, timezone-aware `created_at`, and one or two complete chain records. IDs are content-derived from the format, name and chains; timestamps do not change the ID. Records are copied on creation, so changing the live chain cannot change a saved record.

Loading checks the envelope and content ID, then rebuilds each chain independently against its canonical source snapshot. Graph facts, route order, filters, current authored text and captured review metadata must match. A changed graph, rationale library or review requires a new save; the old JSON stays intact and any already exported HTML retains its captured content. These hashes detect changes; they are not signatures or proof of authorship.

`storytelling.chain_ui` also provides `render_save_controls(chains, snapshots)`, `render_saved_library(snapshots)` and `render_record_downloads(record, snapshots)` for integration into the new dashboard. `render_chain` combines the component and authored text for the standalone workspace; Arnav can instead use the component directly and place the selected step text in the lower-right dashboard panel.

Personal saved JSON files are ignored by Git. Downloaded JSON can also be reopened through `load_saved_chains(Path(...))` on another checkout with matching source data. The prototype's library reads its own saved directory; it does not add an upload/import screen.

The existing optional Qwen story workflow remains available in the original Path story workspace. This chain workspace uses authored reasons/examples and makes no model request.

## Remaining integration

- Arnav: independent A/B controls and pairing/comparison logic; Story / Validation switching and evidence mapping; integration into the reserved dashboard panel.
- Joint: agree on route-pairing behavior, then verify the populated four-panel dashboard.

No Arnav-owned comparison or Dashboard 2.0 assembly was implemented here. Existing saved-story files were not rewritten. The work is published on [codex/horizontal-chain-prototype](https://github.com/maitreya-v/Advanced-Project/tree/codex/horizontal-chain-prototype) for review and integration.

## Verification

```sh
python -m pytest -q tests/test_horizontal_chains.py tests/test_chain_store.py tests/test_chain_library.py tests/test_legacy_export_compatibility.py tests/test_path_stories.py tests/test_story_paths.py tests/test_storytelling.py tests/test_graph_selector.py tests/test_dashboard.py tests/test_dashboard_v2.py
```

**112 tests and 690 subtests passed.** The checks cover persistence in fresh app sessions, frozen saved records after live scenario changes, source/record alteration, interrupted writes, read-only save failures with downloads retained, two-scenario records/exports, and the two legacy formats, including rejection of rehashed altered facts.

Live browser checks confirmed horizontal row alignment, internal scrolling, click/keyboard story selection, age-change resets, saving a real chain, opening age 8 after changing the live age to 32, and a full reload reopening the saved view from its URL. No browser console errors were observed. Both bundled legacy stories were also exported to real HTML files.

The HTML export's complete embedded records and lack of remote scripts/dependencies were tested. A full exported-file browser replay was not completed: the in-app browser blocks `file:` URLs, and its download-event observer did not report the HTML download. No blocked file-navigation workaround was used. The exported HTML/JSON artifacts are available in the parent project's `outputs/` directory for opening directly in a normal browser.

The literature/PDF suites were not rerun for this change. The combined Dashboard 2.0 browser acceptance remains dependent on Arnav's integration.
