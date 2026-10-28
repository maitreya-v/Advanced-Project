"""Standalone chain workspace: python -m streamlit run Chain_Prototype.py."""
import re

import streamlit as st

from storytelling.chain_core import build_chain, query_chains
from storytelling import chain_store as storage
from storytelling.chain_ui import render_chain, render_record_downloads, render_save_controls, render_saved_library
from storytelling.data import load_snapshots

st.set_page_config(page_title="Story chain prototype", layout="wide")
st.html("""<style>
.block-container { max-width:1380px; padding:1.5rem 2rem; }
[data-testid="stVerticalBlock"] { gap:.65rem; }
.prototype-label { color:#698092; font:600 11px system-ui; text-transform:uppercase; letter-spacing:1.4px; }
h1 { font-size:30px !important; padding-top:0 !important; }
</style><div class="prototype-label">Dashboard 2.0 · chain prototype</div>""")
st.title("Follow a story, one arrow at a time")
st.caption("Choose a scenario and route, then select an arrow to read its story. Save chains to return to them later.")

snapshots = load_snapshots()
with st.sidebar:
    opened = render_saved_library(snapshots)
if opened is not None:
    st.session_state["chain_open_id"] = opened["save_id"]
    st.session_state["chain_mode"] = "Saved chains"
    st.query_params["saved_chain"] = opened["save_id"]
elif "chain_mode" not in st.session_state:
    requested = st.query_params.get("saved_chain", "")
    st.session_state["chain_mode"] = "Saved chains" if re.fullmatch(r"[a-f0-9]{24}", requested) else "Explore chains"
    if requested:
        st.session_state["chain_open_id"] = requested
mode = st.radio("View", ["Explore chains", "Saved chains"], horizontal=True, key="chain_mode", label_visibility="collapsed")
notice = st.session_state.pop("chain_saved_notice", None)
if notice:
    st.success(notice)
if mode == "Saved chains":
    saved_id = st.session_state.get("chain_open_id", "")
    if not re.fullmatch(r"[a-f0-9]{24}", saved_id):
        st.info("Choose a saved chain in the sidebar and click Open saved chain.")
        st.stop()
    try:
        record = storage.load_saved_chains(storage.DEFAULT_DIRECTORY / (saved_id + ".json"), snapshots=snapshots)
        st.subheader(record["name"])
        st.caption("Saved view · this route and its story are preserved independently of your live filters.")
        for index, saved_chain in enumerate(record["chains"]):
            render_chain(saved_chain, key=f"saved_chain_{index}")
        render_record_downloads(record, snapshots, key="saved_chain_downloads")
    except (OSError, ValueError) as error:
        st.error(f"This saved chain cannot be opened: {error}")
    st.stop()
st.query_params.pop("saved_chain", None)
settings = st.session_state.get("chain_live_settings", {})
controls = st.columns([1, 1, 2, 1])
years = sorted(snapshots)
year = controls[0].selectbox("Year", years, index=years.index(settings.get("year", 2026)), key="chain_year")
ages = sorted(snapshots[year])
age = controls[1].selectbox("Age", ages, index=ages.index(settings.get("age", ages[0])), key="chain_age")
minimum = controls[2].slider("Minimum edge strength", 0.0, 1.0, settings.get("minimum", 0.0), 0.01, key="chain_strength")
max_hops = controls[3].selectbox("Maximum steps", range(1, 8), index=settings.get("max_hops", 5) - 1, key="chain_hops")
snapshot = snapshots[year][age]
# Keep endpoints available when switching scenarios; missing concepts are
# reported by query_chains instead of silently selecting another concept.
concepts = sorted({node["id"] for ages in snapshots.values() for item in ages.values() for node in item["nodes"]})
left, right = st.columns(2)
start = left.selectbox("Start concept", concepts, index=concepts.index(settings.get("start", "Diagnosis Status")), key="chain_start")
end = right.selectbox("End concept", concepts, index=concepts.index(settings.get("end", "Quality of Life")), key="chain_end")
st.session_state["chain_live_settings"] = {"year": year, "age": age, "minimum": minimum,
                                           "max_hops": max_hops, "start": start, "end": end,
                                           "route_id": settings.get("route_id")}
if start == end:
    st.info("Choose different starting and ending concepts.")
    st.stop()

@st.cache_data(show_spinner=False, max_entries=48)
def cached_query(graph, first, last, hops, strength):
    return query_chains(graph, first, last, max_hops=hops, minimum_strength=strength)

result = cached_query(snapshot, start, end, max_hops, minimum)
if result["state"] == "missing_endpoints":
    st.info("This scenario does not contain: " + ", ".join(result["missing_endpoints"]) + ". Choose other endpoints or another scenario.")
    st.stop()
if not result["complete"]:
    st.warning(f"Search reached its limit. Showing {result['returned_count']} routes found so far; others may exist.")
if not result["paths"]:
    st.info(f"No directed route within {max_hops} steps meets these filters." if result["reachable"]
            else "No directed route connects these concepts with the current strength filter.")
    st.stop()

routes = {route["path_id"]: route for route in result["paths"]}
default = next((index for index, route in enumerate(result["paths"])
                if len(route["node_ids"]) > 3 and "Medication Treatment" in route["node_ids"]), 0)
if st.session_state.get("chain_route_query") != result["query_id"] or "chain_route" not in st.session_state:
    previous_route = settings.get("route_id") if st.session_state.get("chain_route_query") == result["query_id"] else None
    st.session_state["chain_route_query"] = result["query_id"]
    st.session_state["chain_route"] = previous_route if previous_route in routes else result["paths"][default]["path_id"]
route_id = st.selectbox("Route", list(routes), key="chain_route",
                        format_func=lambda key: f"{routes[key]['hop_count']} steps · " + " → ".join(routes[key]["node_ids"]))
st.caption(f"{result['returned_count']} routes {'found' if result['complete'] else 'shown'} · {year} · Age {age}")
st.session_state["chain_live_settings"]["route_id"] = route_id
try:
    chain = build_chain(snapshot, routes[route_id], max_hops=max_hops, minimum_strength=minimum)
except (ValueError, KeyError, OSError) as error:
    st.error(f"This chain could not be prepared from the current source records: {error}")
    st.stop()
render_chain(chain)
render_save_controls([chain], snapshots)
