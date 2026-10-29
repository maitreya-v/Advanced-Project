# Dashboard 2.0

Run this separate entry point from the repository root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Dashboard_2_0.py --server.port 8503
```

Open <http://localhost:8503>.

On macOS/Linux, run `.venv/bin/python -m streamlit run Dashboard_2_0.py --server.port 8503`.

- Equal-width left and right sections, compact spacing and a pale background
  with white panels, following the supplied layout references.
- Compact year, age and minimum edge strength sliders above the left snapshot
  graph, with labels beside the slider tracks.
- The original fixed graph positions, domain backgrounds, signs, strengths,
  navigation controls and validation styling.
- Snapshot details in the lower right, with Info, Edges, Groups, Legend, Changes, Story and
  Validation tabs. Clicking an edge opens its validation; the existing evidence
  pagination, source/PDF links and Back to info control are reused.
- Reports for 1970, 1990, 2010 and 2026, across ages 8, 32 and 45.
- Two horizontal story chains in the upper right. **Year A / Age A** and
  **Year B / Age B** independently select any pair of scenarios, including
  different years and ages, reverse ordering, or the same scenario. They remain
  independent of the left graph's year/age sliders. **Choose routes** opens separate
  **Start A / End A** and **Start B / End B** controls and route selectors, with a
  shared maximum step limit. Changing an endpoint refreshes and focuses only that
  scenario's chain, resetting its selected step while preserving the other side.
  The minimum-strength slider filters both chains; each route stays within its
  own scenario and retains its own selected step.
- Comparison counts show full-scenario changes **from A to B**. The **Changes**
  tab lists added/removed nodes and directed edges, sign changes, and strength
  values in A and B with `B − A` deltas. An edge that changes sign and strength
  appears in both categories. Route and strength filters do not change this
  full-scenario comparison. Identical scenarios show zero changes.
- Select an arrow, use Previous/Next or keyboard navigation, or choose **Scenario
  A / Scenario B** to focus the corresponding step. The **Story / Validation**
  toggle opens its explanation/examples or reviewed evidence in the lower panel.
  Moving to another step or scenario retains the chosen mode. Evidence resolves
  against the step's own year, age and directed endpoints.
- **Save or download comparison** preserves both named routes and exports standalone HTML
  or JSON. **Saved chains** opens the persistent library. Saved views keep their
  original scenario and filters; return to Explore chains to resume live controls.
  Saved links (`?saved_chain=<id>`) reopen both routes after a reload on the same
  host. Older single-chain saves remain supported. If only one scenario has a
  route, that chain can still be saved/downloaded.
- **View step validation**, or the Validation tab after selecting a chain step,
  opens that relationship's reviewed evidence for the chain's year and age.
  Selecting a graph edge returns the detail panel to the graph's scenario. The
  detail header labels whether it follows Graph, Chain or Saved chain.

Changing the graph's year/age sliders resets its selected edge. Changing an A/B
selector resets only that scenario's route and step, preserving endpoints and
the other side's selection. Changing minimum strength recalculates both routes.
Missing concepts and filtered/no-route results have separate scenario-labeled
messages including the requested endpoints, while full-scenario changes remain
available. Saved chains stay frozen when live controls change, including their
evidence scope. Graph zoom survives
an edge-click rerun. Info reports visible and total edges.

`dashboard_v2_graph.py` contains the graph loading and rendering functions
preserved from Dashboard 1.0, without importing or executing its user interface.
The existing validation module and report data are shared. Dashboard 1.0 and its
helpers have not been changed for this layout.

The page stays within the browser window without page scrolling. Each of the
four panels can scroll internally when its content exceeds its available height.
The left and right columns size independently: the controls use up to 168 pixels
and the chain workspace takes 64% of the available workspace height. The graph
and Snapshot panel use the remaining height in their respective columns.
Validation evidence still paginates inside the Snapshot panel.
The validation component reserves at least 144 pixels for readable page content;
its header and navigation are measured separately. When the component needs more
space than the Snapshot panel, that panel scrolls internally. This prevents Next
from becoming ineffective in short browser windows.

`dashboard_v2_viewport/index.html` reports the browser dimensions and listens for
window resizing, so panel heights update without refreshing the page. It requires
no additional Python dependency.

## Checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_dashboard_v2.py -v
```

Integration coverage exercises every year/age selection, strength filtering,
edge selection, switching tabs, closing validation, and clearing stale selection
when the graph changes. `tests/test_dashboard_v2_chains.py` also checks story-step
selection per side, stale events, graph/chain detail switching, the Story/Validation
toggle, scenario-specific evidence, saved comparison reopening, legacy single
chain saves, failed saves with downloads retained, missing endpoints and no-route
states. `tests/test_scenario_comparison.py` checks simultaneous sign/strength
changes, reversed edges, isolated nodes, and all 144 pairs of the 12 real scenarios.
Run them with:

```sh
.venv/bin/python -m pytest -q tests/test_dashboard_v2.py tests/test_dashboard_v2_chains.py tests/test_scenario_comparison.py
```

With the dashboard running and Playwright installed, run
`.venv/bin/python scripts/check_dashboard_v2_chain_endpoints.py` to check all
four endpoint selectors in a real browser, including opening the route popover,
preserving the other scenario's route/step, recovering from disconnected
endpoints, and the correct Story/Validation scope. Route dropdown defaults and
Max steps are supplied explicitly so opening a previously hidden popover cannot
reset endpoints to ADHD or the step limit to 1.

Browser checks exercise an actual canvas edge click,
validation pagination, Back to info, and desktop/laptop layouts.

With Dashboard 2.0 running on port 8503 and Playwright installed, run
`python scripts/check_dashboard_v2_pagination.py` to check every validation page
across compact 1970/2026 panels, including Previous and Next after Streamlit
reruns, reference transitions and a long edge title in a smaller window.
