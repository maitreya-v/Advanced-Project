# Dashboard 2.0

Run this separate entry point from the repository root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Dashboard_2_0.py --server.port 8503
```

Open <http://localhost:8503>.

- Equal-width left and right sections, compact spacing and a pale background
  with white panels, following the supplied layout references.
- Compact year, age and minimum edge strength sliders above the left snapshot
  graph, with labels beside the slider tracks.
- The original fixed graph positions, domain backgrounds, signs, strengths,
  navigation controls and validation styling.
- Snapshot details in the lower right, with Info, Edges, Groups, Legend and
  Validation tabs. Clicking an edge opens its validation; the existing evidence
  pagination, source/PDF links and Back to info control are reused.
- Reports for 1970, 1990, 2010 and 2026, across ages 8, 32 and 45.
- The taller upper-right panel is reserved for the future chain workspace. Chain and
  saved-chain functionality is intentionally deferred to a later revision.

Changing a slider resets the selected edge and Snapshot tab so evidence from
the previous graph cannot remain attached to the new graph. Graph zoom survives
an edge-click rerun. Info reports both visible and total edge counts.

`dashboard_v2_graph.py` contains the graph loading and rendering functions
preserved from Dashboard 1.0, without importing or executing its user interface.
The existing validation module and report data are shared. Dashboard 1.0 and its
helpers have not been changed for this layout.

The page stays within the browser window without page scrolling. Each of the
four panels can scroll internally when its content exceeds its available height.
The left and right columns size independently: the controls use up to 168 pixels
and the chain workspace takes 45% of the available workspace height. The graph
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
when the graph changes. Browser checks exercise an actual canvas edge click,
validation pagination, Back to info, and desktop/laptop layouts.

With Dashboard 2.0 running on port 8503 and Playwright installed, run
`python scripts/check_dashboard_v2_pagination.py` to check every validation page
across compact 1970/2026 panels, including Previous and Next after Streamlit
reruns, reference transitions and a long edge title in a smaller window.
