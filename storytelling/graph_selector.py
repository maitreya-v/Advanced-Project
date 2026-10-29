"""A full-graph endpoint picker with validated Streamlit selection events."""
import json

import streamlit as st
import streamlit.components.v1 as components

from .data import ROOT

graph_selector_component = components.declare_component(
    "story_endpoint_selector", path=str(ROOT / "storytelling" / "path_selector_component")
)


@st.cache_data(show_spinner=False)
def full_graph_html(snapshot: dict) -> str:
    template = (ROOT / "storytelling" / "full_graph.html").read_text(encoding="utf-8")
    library = (ROOT / "lib" / "vis-9.1.2" / "vis-network.min.js").read_text(encoding="utf-8")
    graph = {key: snapshot[key] for key in ("fingerprint", "year", "age", "nodes", "edges")}
    payload = json.dumps(graph, ensure_ascii=False)
    payload = payload.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return template.replace("/* VIS_LIBRARY */", library).replace("/* GRAPH_DATA */", payload)


def apply_node_selection(selection: dict | None, snapshot: dict, state,
                         start_key: str, end_key: str) -> bool:
    if not isinstance(selection, dict) or selection.get("fingerprint") != snapshot["fingerprint"]:
        return False
    event_id = selection.get("event_id")
    if not isinstance(event_id, str) or not 1 <= len(event_id) <= 100:
        return False
    event_key = "path_graph_event_" + snapshot["fingerprint"]
    if state.get(event_key) == event_id:
        return False
    role = selection.get("role")
    if role == "clear":
        state[start_key] = None
        state[end_key] = None
    elif role in {"start", "end"}:
        node_id = selection.get("node_id")
        if not isinstance(node_id, str) or node_id not in {node["id"] for node in snapshot["nodes"]}:
            return False
        state[start_key if role == "start" else end_key] = node_id
    else:
        return False
    state[event_key] = event_id
    return True
