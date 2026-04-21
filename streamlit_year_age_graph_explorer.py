from pathlib import Path
import re
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

st.set_page_config(page_title="Chronological Year + Age Graph Explorer", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
HELPER_NODE_IDS = {"LEGEND_NODE", "PERSONA_DESC", "PERIOD_NODE", "Persona", "PERSONA_NODE"}


class FakeNetwork:
    def __init__(self, *args, **kwargs):
        self.nodes = []
        self.edges = []

    def barnes_hut(self, *args, **kwargs):
        return None

    def toggle_physics(self, *args, **kwargs):
        return None

    def set_options(self, *args, **kwargs):
        return None

    def add_node(self, *args, **kwargs):
        node_payload = dict(kwargs)
        if len(args) >= 1:
            node_payload.setdefault("id", args[0])
        self.nodes.append(node_payload)

    def add_edge(self, *args, **kwargs):
        edge_payload = dict(kwargs)
        if len(args) >= 1:
            edge_payload.setdefault("from", args[0])
        if len(args) >= 2:
            edge_payload.setdefault("to", args[1])
        self.edges.append(edge_payload)

    def write_html(self, *args, **kwargs):
        return None

    def generate_html(self, *args, **kwargs):
        return ""


class FakeWebBrowser:
    def open(self, *args, **kwargs):
        return None


def discover_source_files() -> dict[int, dict[int, Path]]:
    file_map: dict[int, dict[int, Path]] = {}

    for path in sorted(BASE_DIR.glob("*yo.py")):
        match = re.match(r"^(\d{4})_(\d+)\s*yo\.py$", path.name)
        if not match:
            continue

        year = int(match.group(1))
        age = int(match.group(2))
        file_map.setdefault(year, {})
        file_map[year][age] = path

    return file_map


def load_snapshot_from_script(script_path: Path) -> dict:
    code_text = script_path.read_text(encoding="utf-8")

    code_text = re.sub(
        r"^\s*from pyvis\.network import Network\s*$",
        "",
        code_text,
        flags=re.MULTILINE,
    )
    code_text = re.sub(
        r"^\s*import webbrowser\s*$",
        "",
        code_text,
        flags=re.MULTILINE,
    )
    code_text = re.sub(
        r"^\s*import os\s*$",
        "",
        code_text,
        flags=re.MULTILINE,
    )

    sandbox_globals = {
        "__name__": "__main__",
        "Network": FakeNetwork,
        "webbrowser": FakeWebBrowser(),
        "os": __import__("os"),
    }

    exec(code_text, sandbox_globals)

    if "net" not in sandbox_globals:
        raise RuntimeError(f"No global 'net' object was created by {script_path.name}")

    fake_net: FakeNetwork = sandbox_globals["net"]

    group_colors = dict(sandbox_globals.get("group_colors", {}))
    group_descriptions = dict(sandbox_globals.get("group_descriptions", {}))
    node_groups = dict(sandbox_globals.get("node_groups", {}))

    graph_nodes = []
    helper_text = {}

    for node in fake_net.nodes:
        node_id = node.get("id")
        if node_id in HELPER_NODE_IDS:
            helper_text[node_id] = node.get("label", "")
            continue
        graph_nodes.append(node)

    graph_edges = list(fake_net.edges)

    filename_match = re.match(r"^(\d{4})_(\d+)\s*yo\.py$", script_path.name)
    if not filename_match:
        raise RuntimeError(f"Unexpected filename format: {script_path.name}")

    year_value = int(filename_match.group(1))
    age_value = int(filename_match.group(2))

    ordered_groups = []
    seen_groups = set()

    for node in graph_nodes:
        group_name = node_groups.get(node.get("id"))
        if group_name and group_name not in seen_groups and group_name in group_colors:
            ordered_groups.append(group_name)
            seen_groups.add(group_name)

    return {
        "year": year_value,
        "age": age_value,
        "file_name": script_path.name,
        "nodes": graph_nodes,
        "edges": graph_edges,
        "group_colors": group_colors,
        "group_descriptions": group_descriptions,
        "node_groups": node_groups,
        "ordered_groups": ordered_groups,
        "legend_text": helper_text.get("LEGEND_NODE", ""),
        "persona_text": helper_text.get("PERSONA_DESC", helper_text.get("Persona", "")),
    }


@st.cache_data(show_spinner=False)
def load_all_snapshots() -> dict[int, dict[int, dict]]:
    file_map = discover_source_files()
    snapshot_map: dict[int, dict[int, dict]] = {}

    for year in sorted(file_map):
        snapshot_map[year] = {}
        for age in sorted(file_map[year]):
            snapshot_map[year][age] = load_snapshot_from_script(file_map[year][age])

    return snapshot_map


def build_network_html(snapshot: dict) -> str:
    net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")

    net.set_options(
        """
        var options = {
          "layout": { "improvedLayout": false },
          "physics": { "enabled": false },
          "interaction": {
            "dragNodes": false,
            "dragView": true,
            "zoomView": true,
            "hover": true,
            "navigationButtons": true
          },
          "edges": {
            "smooth": false,
            "font": { "size": 12, "align": "top" }
          }
        }
        """
    )

    for original_node in snapshot["nodes"]:
        node_payload = dict(original_node)
        node_id = node_payload.pop("id")
        net.add_node(node_id, **node_payload)

    for original_edge in snapshot["edges"]:
        edge_payload = dict(original_edge)
        source_id = edge_payload.pop("from")
        target_id = edge_payload.pop("to")
        net.add_edge(source_id, target_id, **edge_payload)

    return net.generate_html(notebook=False)


def clean_multiline_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = str(raw_text).replace("\r\n", "\n").replace("\r", "\n").strip()
    return re.sub(r"\n{3,}", "\n\n", text)


SNAPSHOTS = load_all_snapshots()

if not SNAPSHOTS:
    st.error("No year-age graph source files were found next to this app.")
    st.stop()

available_years = sorted(SNAPSHOTS.keys())

st.title("Chronological Year + Age Graph Explorer")
st.caption(
    "Choose a year and an age to switch between fixed graph snapshots. "
    "Each snapshot is loaded directly from the year-age source graph files."
)

st.sidebar.header("Controls")

selected_year = st.sidebar.select_slider(
    "Choose a year",
    options=available_years,
    value=available_years[0],
)

year_specific_ages = sorted(SNAPSHOTS[selected_year].keys())
default_age = 8 if 8 in year_specific_ages else year_specific_ages[0]

selected_age = st.sidebar.select_slider(
    "Choose an age",
    options=year_specific_ages,
    value=default_age,
)

selected_snapshot = SNAPSHOTS[selected_year][selected_age]
graph_html = build_network_html(selected_snapshot)

left_col, right_col = st.columns([4.8, 1.2])

with left_col:
    st.subheader(f"Graph for {selected_year} | Age {selected_age}")
    components.html(graph_html, height=930, scrolling=True)

with right_col:
    st.subheader("Snapshot")
    st.write(f"**Year:** {selected_year}")
    st.write(f"**Age:** {selected_age}")
    st.write(f"**Source file:** `{selected_snapshot['file_name']}`")
    st.write(f"**Nodes:** {len(selected_snapshot['nodes'])}")
    st.write(f"**Edges:** {len(selected_snapshot['edges'])}")

    st.divider()
    st.subheader("Edges")
    st.markdown(
        """
        Green edge (+): positive effect  
        Red edge (-): negative effect  
        Arrow direction: source influences target  
        Edge thickness: causal strength  
        Hover an edge: see effect, why, and strength
        """
    )

    st.divider()
    st.subheader("Node groups")
    for group_name in selected_snapshot["ordered_groups"]:
        group_color = selected_snapshot["group_colors"].get(group_name, "#dddddd")
        group_description = selected_snapshot["group_descriptions"].get(group_name, "")
        st.markdown(
            f"""
            <div style="margin-bottom: 10px;">
              <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:14px; height:14px; border-radius:50%; background:{group_color}; border:1px solid #999;"></div>
                <strong>{group_name.replace("_", " ").title()}</strong>
              </div>
              <div style="margin-left:22px; font-size:0.92rem; color:#555;">{group_description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Description")
    persona_text = clean_multiline_text(selected_snapshot["persona_text"])
    if persona_text:
        st.markdown(
            f"""
            <div style="padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; background: #fafafa; white-space: pre-wrap;">
            {persona_text}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.write("No description block was found in this source snapshot.")