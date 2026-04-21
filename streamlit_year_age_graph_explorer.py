
# Import the standard path utilities.
from pathlib import Path
# Import regular expressions for filename parsing and import stripping.
import re
# Import the operating system module for the sandboxed script execution environment.
import os
# Import Streamlit.
import streamlit as st
# Import the Streamlit HTML renderer.
import streamlit.components.v1 as components
# Import PyVis.
from pyvis.network import Network

# Set the page configuration.
st.set_page_config(page_title="Chronological Year + Age Graph Explorer", layout="wide")

# Store the directory that contains this app file and the uploaded graph scripts.
BASE_DIR = Path(__file__).resolve().parent

# Store helper node ids that should not be shown as part of the actual graph.
HELPER_NODE_IDS = {"LEGEND_NODE", "PERSONA_DESC", "PERIOD_NODE", "Persona", "PERSONA_NODE"}

# Define a fake network class so the source graph scripts can be executed safely and captured.
class FakeNetwork:
    # Initialize the fake network.
    def __init__(self, *args, **kwargs):
        # Store captured nodes.
        self.nodes = []
        # Store captured edges.
        self.edges = []

    # Ignore barnes_hut calls from the source scripts.
    def barnes_hut(self, *args, **kwargs):
        # Do nothing.
        return None

    # Ignore toggle_physics calls from the source scripts.
    def toggle_physics(self, *args, **kwargs):
        # Do nothing.
        return None

    # Ignore set_options calls from the source scripts.
    def set_options(self, *args, **kwargs):
        # Do nothing.
        return None

    # Capture nodes that the source script adds.
    def add_node(self, *args, **kwargs):
        # Copy keyword arguments.
        node_payload = dict(kwargs)
        # Preserve the node id from the first positional argument.
        if len(args) >= 1:
            node_payload.setdefault("id", args[0])
        # Save the node.
        self.nodes.append(node_payload)

    # Capture edges that the source script adds.
    def add_edge(self, *args, **kwargs):
        # Copy keyword arguments.
        edge_payload = dict(kwargs)
        # Preserve the source node id from the first positional argument.
        if len(args) >= 1:
            edge_payload.setdefault("from", args[0])
        # Preserve the target node id from the second positional argument.
        if len(args) >= 2:
            edge_payload.setdefault("to", args[1])
        # Save the edge.
        self.edges.append(edge_payload)

    # Ignore write_html calls from the source scripts.
    def write_html(self, *args, **kwargs):
        # Do nothing.
        return None

    # Return empty html if ever called.
    def generate_html(self, *args, **kwargs):
        # Return an empty string.
        return ""

# Define a fake webbrowser object so the source scripts do not try to open tabs.
class FakeWebBrowser:
    # Ignore open calls.
    def open(self, *args, **kwargs):
        # Do nothing.
        return None

# Discover all year-age source graph files next to this app.
def discover_source_files():
    # Create the output mapping.
    file_map = {}
    # Loop through all matching python files.
    for path in sorted(BASE_DIR.glob("*yo.py")):
        # Try to parse year and age from the filename.
        match = re.match(r"^(\d{4})_(\d+)\s*yo\.py$", path.name)
        # Skip anything that does not match the pattern.
        if not match:
            continue
        # Read the year value.
        year = int(match.group(1))
        # Read the age value.
        age = int(match.group(2))
        # Create the year bucket if needed.
        file_map.setdefault(year, {})
        # Save the file path for this year-age combination.
        file_map[year][age] = path
    # Return the discovered map.
    return file_map

# Execute one source script in a sandbox and capture its final graph data.
def load_snapshot_from_script(script_path):
    # Read the script text.
    code_text = script_path.read_text(encoding="utf-8")
    # Remove the original imports so the fake objects remain in control.
    code_text = re.sub(r"^\s*from pyvis\.network import Network\s*$", "", code_text, flags=re.MULTILINE)
    # Remove the original webbrowser import.
    code_text = re.sub(r"^\s*import webbrowser\s*$", "", code_text, flags=re.MULTILINE)
    # Remove the original os import.
    code_text = re.sub(r"^\s*import os\s*$", "", code_text, flags=re.MULTILINE)
    # Build the sandbox globals.
    sandbox_globals = {
        "__name__": "__main__",
        "Network": FakeNetwork,
        "webbrowser": FakeWebBrowser(),
        "os": os,
    }
    # Execute the source script.
    exec(compile(code_text, str(script_path), "exec"), sandbox_globals)
    # Read the captured fake network.
    fake_net = sandbox_globals["net"]
    # Read the optional metadata dictionaries if they exist.
    group_colors = dict(sandbox_globals.get("group_colors", {}))
    # Read the optional group descriptions if they exist.
    group_descriptions = dict(sandbox_globals.get("group_descriptions", {}))
    # Read the optional node-to-group mapping if it exists.
    node_groups = dict(sandbox_globals.get("node_groups", {}))
    # Create containers for graph nodes and helper text.
    graph_nodes = []
    # Create containers for helper text labels.
    helper_text = {}
    # Loop through captured nodes.
    for node in fake_net.nodes:
        # Read the node id.
        node_id = node.get("id")
        # Capture legend/persona helper nodes separately.
        if node_id in HELPER_NODE_IDS:
            # Save the helper label text.
            helper_text[node_id] = node.get("label", "")
            # Skip adding the helper node to the main graph.
            continue
        # Save the visible graph node.
        graph_nodes.append(node)
    # Read the captured edges exactly as produced by the source script.
    graph_edges = list(fake_net.edges)
    # Derive a readable year from the filename.
    filename_match = re.match(r"^(\d{4})_(\d+)\s*yo\.py$", script_path.name)
    # Read the year.
    year_value = int(filename_match.group(1))
    # Read the age.
    age_value = int(filename_match.group(2))
    # Create the ordered set of groups as they appear in visible nodes.
    ordered_groups = []
    # Track seen groups.
    seen_groups = set()
    # Loop through visible nodes in order.
    for node in graph_nodes:
        # Read the node group.
        group_name = node_groups.get(node.get("id"), None)
        # Add the group only once and only if metadata exists for it.
        if group_name and group_name not in seen_groups and group_name in group_colors:
            # Save order.
            ordered_groups.append(group_name)
            # Mark seen.
            seen_groups.add(group_name)
    # Return the normalized snapshot.
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

# Cache all parsed snapshots so the app stays responsive.
@st.cache_data(show_spinner=False)
def load_all_snapshots():
    # Discover all available source files.
    file_map = discover_source_files()
    # Create the output snapshot matrix.
    snapshot_map = {}
    # Loop through years in sorted order.
    for year in sorted(file_map):
        # Create the year bucket.
        snapshot_map[year] = {}
        # Loop through ages in sorted order.
        for age in sorted(file_map[year]):
            # Parse and store this snapshot.
            snapshot_map[year][age] = load_snapshot_from_script(file_map[year][age])
    # Return all snapshots.
    return snapshot_map

# Build the display network HTML for one selected snapshot.
def build_network_html(snapshot):
    # Create the PyVis network.
    net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")
    # Apply stable options for fixed-position graphs.
    net.set_options(
        """
        var options = {
          "layout": {
            "improvedLayout": false
          },
          "physics": {
            "enabled": false
          },
          "interaction": {
            "dragNodes": false,
            "dragView": true,
            "zoomView": true,
            "hover": true,
            "navigationButtons": true
          },
          "edges": {
            "smooth": false,
            "font": {
              "size": 12,
              "align": "top"
            }
          }
        }
        """
    )
    # Add every visible node exactly from the captured snapshot.
    for original_node in snapshot["nodes"]:
        # Copy the node payload.
        node_payload = dict(original_node)
        # Read and remove the id.
        node_id = node_payload.pop("id")
        # Add the node back into the rendered network.
        net.add_node(node_id, **node_payload)
    # Add every captured edge exactly from the snapshot.
    for original_edge in snapshot["edges"]:
        # Copy the edge payload.
        edge_payload = dict(original_edge)
        # Read and remove the source id.
        source_id = edge_payload.pop("from")
        # Read and remove the target id.
        target_id = edge_payload.pop("to")
        # Add the edge back into the rendered network.
        net.add_edge(source_id, target_id, **edge_payload)
    # Generate the html.
    graph_html = net.generate_html(notebook=False)
    # Inject tooltip styling so multiline plain text stays readable.
    graph_html = graph_html.replace(
        "</head>",
        """
<style>
div.vis-tooltip {
    white-space: pre-line !important;
    max-width: 360px !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    border: 1px solid #d9d9d9 !important;
    background: #ffffff !important;
    color: #111111 !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12) !important;
    font-family: Arial, sans-serif !important;
}
</style>
</head>
""",
        1,
    )
    # Return the html.
    return graph_html

# Convert multiline helper text into a cleaner display block.
def clean_multiline_text(raw_text):
    # Handle missing text.
    if not raw_text:
        # Return an empty string.
        return ""
    # Normalize line endings and trim surrounding whitespace.
    text = str(raw_text).replace("\r\n", "\n").replace("\r", "\n").strip()
    # Collapse repeated blank lines a little for better sidebar readability.
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Return the cleaned text.
    return text

# Load all snapshots.
SNAPSHOTS = load_all_snapshots()

# Stop early if no files were found.
if not SNAPSHOTS:
    # Show an error message.
    st.error("No year-age graph source files were found next to this app.")
    # Stop the app.
    st.stop()

# Build the sorted year list.
available_years = sorted(SNAPSHOTS.keys())

# Build the union of all available ages across years.
available_ages = sorted({age for year in available_years for age in SNAPSHOTS[year].keys()})

# Show the page title.
st.title("Chronological Year + Age Graph Explorer")

# Show the short description.
st.caption("Choose a year and an age to switch between fixed graph snapshots. Each snapshot is loaded from your source graph files so the graph changes exactly with the selected year-age combination.")

# Create the sidebar header.
st.sidebar.header("Controls")

# Create the year slider.
selected_year = st.sidebar.select_slider("Choose a year", options=available_years, value=available_years[0])

# Read the ages available for the chosen year.
year_specific_ages = sorted(SNAPSHOTS[selected_year].keys())

# Choose a sensible default age.
default_age = 8 if 8 in year_specific_ages else year_specific_ages[0]

# Create the age slider.
selected_age = st.sidebar.select_slider("Choose an age", options=year_specific_ages, value=default_age)

# Read the selected snapshot.
selected_snapshot = SNAPSHOTS[selected_year][selected_age]

# Build the graph html.
graph_html = build_network_html(selected_snapshot)

# Create the main layout.
left_col, right_col = st.columns([4.8, 1.2])

# Render the graph area.
with left_col:
    # Show the graph title.
    st.subheader(f"Graph for {selected_year} | Age {selected_age}")
    # Render the graph.
    components.html(graph_html, height=930, scrolling=True)

# Render the right panel.
with right_col:
    # Show the overview title.
    st.subheader("Snapshot")
    # Show the selected year.
    st.write(f"**Year:** {selected_year}")
    # Show the selected age.
    st.write(f"**Age:** {selected_age}")
    # Show the source file.
    st.write(f"**Source file:** `{selected_snapshot['file_name']}`")
    # Show the node count.
    st.write(f"**Nodes:** {len(selected_snapshot['nodes'])}")
    # Show the edge count.
    st.write(f"**Edges:** {len(selected_snapshot['edges'])}")

    # Add a divider.
    st.divider()

    # Show the universal edge legend.
    st.subheader("Edges")
    # Render the edge legend card.
    st.markdown(
        """
        <div style="background:#f7f7f7;padding:14px 16px;border-radius:12px;line-height:1.7;">
        <b>Green edge (+)</b>: positive effect<br>
        <b>Red edge (-)</b>: negative effect<br>
        <b>Arrow direction</b>: source influences target<br>
        <b>Edge thickness</b>: causal strength<br>
        <b>Hover an edge</b>: see effect, why, and strength
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Add a divider.
    st.divider()

    # Show the node legend title.
    st.subheader("Node groups")
    # Loop through ordered groups for this snapshot.
    for group_name in selected_snapshot["ordered_groups"]:
        # Read the color.
        group_color = selected_snapshot["group_colors"].get(group_name, "#dddddd")
        # Read the description.
        group_description = selected_snapshot["group_descriptions"].get(group_name, "")
        # Render a colored legend row.
        st.markdown(
            f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;">
                <div style="width:14px;height:14px;border-radius:3px;background:{group_color};margin-top:4px;flex:0 0 14px;"></div>
                <div><b>{group_name.replace("_", " ").title()}</b><br>{group_description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Add a divider.
    st.divider()

    # Show the description title.
    st.subheader("Description")
    # Clean the persona text.
    persona_text = clean_multiline_text(selected_snapshot["persona_text"])
    # Show the persona text if it exists.
    if persona_text:
        # Render the description in a readable card.
        st.markdown(
            f"""
            <div style="background:#f7f7f7;padding:14px 16px;border-radius:12px;line-height:1.6;white-space:pre-line;">
            {persona_text}
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Handle a missing description.
    else:
        # Show a fallback message.
        st.write("No description block was found in this source snapshot.")
