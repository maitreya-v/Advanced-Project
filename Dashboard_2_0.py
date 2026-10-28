"""Compact ADHD Explorer. Run with: python -m streamlit run Dashboard_2_0.py."""
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from dashboard_validation import attach_validation, graph_component, render_validation, STATUS_STYLES
from dashboard_v2_graph import (
    load_all_snapshots, build_network_html, extract_strength_from_title,
    clean_multiline_text, clean_text,
)

ROOT = Path(__file__).resolve().parent
viewport_component = components.declare_component("dashboard_v2_viewport", path=str(ROOT / "dashboard_v2_viewport"))
st.set_page_config(page_title="ADHD Explorer · Dashboard 2.0", layout="wide", initial_sidebar_state="collapsed")
st.html("""
<style>
:root { --v2-ink:#173248; --v2-muted:#667f91; --v2-line:#dce6eb; }
[data-testid="stAppViewContainer"] { background:#edf2f5; height:100dvh; overflow:hidden; }
[data-testid="stMain"] { height:100dvh; overflow:hidden !important; }
.block-container { max-width:none; height:100dvh; overflow:hidden; padding:0.5rem 1rem; }
[data-testid="stHeader"] { background:transparent; height:0; }
[data-testid="stToolbar"] { right:0.5rem; top:0.2rem; }
[data-testid="stVerticalBlock"] { gap:0.45rem; }
[data-testid="stHorizontalBlock"] { gap:0.75rem; }
[data-testid="stLayoutWrapper"] { min-width:0; }
.v2-header { display:flex; align-items:center; justify-content:center; position:relative;
  height:48px; background:#fff; border:1px solid var(--v2-line); border-radius:14px; }
.v2-header h1 { color:var(--v2-ink); font:600 29px/1.1 system-ui,sans-serif; letter-spacing:-0.8px; margin:0; padding:0; }
.v2-version { position:absolute; left:16px; font:600 10px system-ui,sans-serif;
  letter-spacing:1.3px; color:var(--v2-muted); text-transform:uppercase; }
.st-key-v2_controls, .st-key-v2_future, .st-key-v2_graph, .st-key-v2_snapshot {
  background:#fff; border:1px solid var(--v2-line); border-radius:14px; padding:12px 15px;
  box-shadow:0 2px 5px #183e5510;
}
.st-key-v2_controls { padding:7px 12px; }
.st-key-v2_future { background:linear-gradient(135deg,#f9fcfc,#f3f8fa); }
.v2-future { display:flex; align-items:flex-start; }
.v2-future span { color:#879da9; font:600 10px system-ui,sans-serif; letter-spacing:1.5px; text-transform:uppercase; }
.st-key-v2_controls [data-testid="stWidgetLabel"] p { font-size:12px; color:var(--v2-ink); }
.st-key-v2_controls [data-testid="stSlider"], .st-key-v2_controls [data-testid="stSelectSlider"] { padding:0; }
.st-key-v2_controls [data-testid="stVerticalBlock"] { gap:0; }
.st-key-v2_controls [data-testid="stHorizontalBlock"] { flex-wrap:nowrap; gap:8px; }
.v2-control-label { color:var(--v2-ink); font-size:12px; padding-top:12px; line-height:1.25; }
.st-key-v2_controls [data-baseweb="slider"] { padding-top:10px; padding-bottom:10px; }
.st-key-v2_viewport { display:none; }
.st-key-v2_workspace > [data-testid="stHorizontalBlock"] { flex-wrap:nowrap; }
.st-key-v2_workspace > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
  flex:1 1 0%; width:calc(50% - 6px); min-width:0;
}
.st-key-v2_controls [data-testid="stSliderTickBarMin"],
.st-key-v2_controls [data-testid="stSliderTickBarMax"] { font-size:10px; }
.v2-section { display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:3px; }
.v2-section h2 { margin:0; padding:0; font:650 16px/1.3 system-ui,sans-serif; color:var(--v2-ink); }
.v2-context { font:11px system-ui,sans-serif; color:var(--v2-muted); }
.st-key-v2_graph { padding:10px 8px 4px; }
.st-key-v2_graph .v2-section { padding:0 7px; }
iframe { display:block; border:0; }
[data-testid="stTabs"] [role="tablist"] { gap:14px; min-height:34px; }
[data-testid="stTabs"] button[role="tab"] { padding:5px 0; font-size:12px; }
[data-testid="stTabs"] [role="tabpanel"] { padding-top:10px; }
.v2-facts { display:grid; grid-template-columns:repeat(4,1fr); gap:6px; margin:4px 0 12px; }
.v2-fact { background:#f2f7f9; border:1px solid #e4ecef; border-radius:8px; padding:9px 10px; }
.v2-fact b { display:block; color:var(--v2-ink); font-size:19px; line-height:1.2; }
.v2-fact span { color:var(--v2-muted); font-size:11px; }
.v2-source { font-size:11px; color:var(--v2-muted); overflow-wrap:anywhere; margin-bottom:9px; }
.v2-groups { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.v2-group strong { color:var(--v2-ink); font-size:12px; }
.v2-group p { color:#526b7b; font-size:11px; line-height:1.4; margin:3px 0 0 17px; }
.v2-dot { display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:7px; }
.st-key-v2_snapshot p { font-size:13px; }
@media (max-width:850px) {
  .block-container { padding:0.5rem; }
  .v2-header { height:48px; }
  .v2-header h1 { font-size:24px; }
  .v2-version { display:none; }
  .v2-facts { grid-template-columns:repeat(2,1fr); }
}
</style>
<header class="v2-header"><span class="v2-version"></span><h1>ADHD Explorer</h1></header>
""")


@st.cache_data(show_spinner=False, max_entries=48)
def graph_html(snapshot, threshold, height):
    return build_network_html(snapshot, threshold, height)


def render_snapshot(snapshot, selected_edge, visible_edges, panel_height):
    """Keep the original Snapshot tabs and the shared validation pagination."""
    st.html(f'<div class="v2-section"><h2>Snapshot</h2><span class="v2-context">{snapshot["year"]} · Age {snapshot["age"]}</span></div>')
    info, edges, groups, legend, validation = st.tabs(
        ["Info", "Edges", "Groups", "Legend", "Validation"], key="snapshot_tabs", on_change="rerun",
    )
    with info:
        facts = [(snapshot["year"], "Year"), (snapshot["age"], "Age"),
                 (len(snapshot["nodes"]), "Nodes"), (len(visible_edges), "Visible edges")]
        st.html('<div class="v2-facts">' + ''.join(
            f'<div class="v2-fact"><b>{value}</b><span>{label}</span></div>' for value, label in facts
        ) + '</div>')
        st.html(f'<div class="v2-source">Source: {html.escape(snapshot["file_name"])} · {len(snapshot["edges"])} total edges</div>')
        description = clean_multiline_text(snapshot["persona_text"])
        if description:
            st.markdown("**Description**")
            st.caption(description)
        st.caption("Click a graph edge to open its validation and research references.")
    with edges:
        st.markdown("**Edge color and dashes:** validation status  \n"
                    "**Sign (+ / −):** positive / negative effect  \n"
                    "**Arrow:** source influences target  \n"
                    "**Thickness:** authored model strength  \n"
                    "**Hover:** original reason and strength  \n"
                    "**Click:** validation and page-linked references")
        st.caption(f"Showing {len(visible_edges)} of {len(snapshot['edges'])} edges at the current strength threshold. Numeric strengths are not validated effect sizes.")
    with groups:
        cards = []
        for name, color in snapshot["group_colors"].items():
            cards.append(f'<div class="v2-group"><strong><span class="v2-dot" style="background:{html.escape(color, quote=True)}"></span>{clean_text(name.replace("_", " ").title())}</strong><p>{clean_text(snapshot["group_descriptions"].get(name, ""))}</p></div>')
        st.html('<div class="v2-groups">' + ''.join(cards) + '</div>')
    with legend:
        st.markdown("**Node border color:** manual domain.  \n"
                    "**Background regions:** fuzzy local clusters derived from node positions and domain colors.  \n"
                    "**Manual domain:** the authored category, such as clinical, access, treatment, school or family.  \n"
                    "**Local domain:** cluster-based grouping from the saved layout.  \n"
                    "**Hover:** domain, original reasoning and strength.")
        st.markdown("**Validation status**")
        st.html(''.join(f'<div style="font-size:12px;margin:5px 0"><span class="v2-dot" style="background:{style["color"]}"></span>{style["label"]}</div>' for style in STATUS_STYLES.values()))
    with validation:
        render_validation(snapshot, selected_edge, panel_height, minimum_content_height=144)


source_files = [ROOT / "clusters.json", *sorted(ROOT.glob("*yo.py"))]
signature = tuple((path.name, path.stat().st_mtime_ns, path.stat().st_size) for path in source_files)
snapshots = load_all_snapshots(signature)
if not snapshots:
    st.error("No year and age snapshots were found.")
    st.stop()

with st.container(key="v2_viewport"):
    viewport = viewport_component(key="v2_viewport_value", default={"height": 900, "width": 1440})
try:
    viewport_height = int(viewport["height"])
except (TypeError, KeyError, ValueError):
    viewport_height = 900
workspace_height = max(220, viewport_height - 82)
controls_height = min(168, int(workspace_height * 0.4))
chain_height = int(workspace_height * 0.45)
graph_panel_height = workspace_height - controls_height - 8
snapshot_height = workspace_height - chain_height - 8
height = max(100, graph_panel_height - 64)

with st.container(key="v2_workspace"):
    graph_col, detail_col = st.columns(2, gap="small")
with graph_col, st.container(key="v2_controls", height=controls_height):
    label, slider = st.columns([1.15, 4], gap="small")
    label.html('<div class="v2-control-label">Choose year</div>')
    year = slider.select_slider("Choose year", options=sorted(snapshots), key="v2_year", label_visibility="collapsed")
    label, slider = st.columns([1.15, 4], gap="small")
    label.html('<div class="v2-control-label">Choose an age</div>')
    age = slider.select_slider("Choose an age", options=sorted(snapshots[year]), key="v2_age", label_visibility="collapsed")
    label, slider = st.columns([1.15, 4], gap="small")
    label.html('<div class="v2-control-label">Minimum edge strength</div>')
    threshold = slider.slider("Minimum edge strength", 0.0, 1.0, 0.0, 0.01, key="v2_strength", label_visibility="collapsed")

snapshot = attach_validation(snapshots[year][age])
visible_edges = [edge for edge in snapshot["edges"] if extract_strength_from_title(edge.get("title", "")) >= threshold]
context = (year, age, threshold)
if st.session_state.get("v2_context") != context:
    st.session_state.update(v2_context=context, v2_selected_edge=None,
                            snapshot_tabs="Info", validation_selection_token=None)
    st.session_state.pop("validation_pending_tab", None)

with graph_col, st.container(key="v2_graph", height=graph_panel_height):
    st.html(f'<div class="v2-section"><h2>Graph</h2><span class="v2-context">{year} · Age {age} · {len(visible_edges)} edges</span></div>')
    selection = graph_component(
        html=graph_html(snapshot, threshold, height), height=height + 8,
        key=f"v2-graph-{year}-{age}-{threshold}", default=None,
    )
    if isinstance(selection, dict):
        edge_id = selection.get("edge_id")
        token = (*context, selection.get("sequence"))
        if edge_id in {edge["id"] for edge in visible_edges} and st.session_state.get("validation_selection_token") != token:
            st.session_state["v2_selected_edge"] = edge_id
            st.session_state["validation_selection_token"] = token
            st.session_state["snapshot_tabs"] = "Validation"
    if not visible_edges:
        st.caption("No edges meet this threshold. Lower minimum edge strength to show connections.")

if "validation_pending_tab" in st.session_state:
    st.session_state["snapshot_tabs"] = st.session_state.pop("validation_pending_tab")

with detail_col:
    with st.container(key="v2_future", height=chain_height):
        st.html('<div class="v2-future" aria-label="Reserved future chain workspace"><span>Chain workspace</span></div>')
    with st.container(key="v2_snapshot", height=snapshot_height):
        render_snapshot(snapshot, st.session_state.get("v2_selected_edge"), visible_edges, max(200, snapshot_height - 110))
