from pathlib import Path
import re
import base64
import time
import html

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

try:
    from streamlit_js_eval import streamlit_js_eval
except Exception:
    streamlit_js_eval = None


st.set_page_config(page_title="Chronological Year + Age Graph Explorer", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 3.2rem !important;
    padding-bottom: 0rem !important;
    padding-left: 2.25rem !important;
    padding-right: 2.25rem !important;
    max-width: 100% !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0.45rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 0.8rem !important;
}

h1, h2, h3 {
    margin-top: 0rem !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.15 !important;
}

iframe {
    border: none !important;
    margin-top: 0px !important;
}

button[data-baseweb="tab"] {
    padding-top: 0.25rem !important;
    padding-bottom: 0.25rem !important;
}
</style>
""", unsafe_allow_html=True)


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
        "__name__": "__graph_loader__",
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


def get_node_ids(snapshot):
    return {node.get("id") for node in snapshot["nodes"] if node.get("id")}


def compare_nodes(current_snapshot, comparison_snapshot):
    current_nodes = get_node_ids(current_snapshot)
    comparison_nodes = get_node_ids(comparison_snapshot)

    added_nodes = sorted(current_nodes - comparison_nodes)
    removed_nodes = sorted(comparison_nodes - current_nodes)

    return added_nodes, removed_nodes


def clean_multiline_text(raw_text: str) -> str:
    if not raw_text:
        return ""

    text = str(raw_text).replace("\r\n", "\n").replace("\r", "\n").strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def clean_text(value):
    value = str(value)
    value = re.sub(r"</?div[^>]*>", "", value, flags=re.IGNORECASE)
    value = re.sub(r"</?span[^>]*>", "", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    return html.escape(value.strip())


def parse_node_title(title_text: str) -> dict:
    parsed = {
        "manual_domain": "unknown",
        "local_domain": "unknown",
        "confidence": 0.0,
    }

    if not title_text:
        return parsed

    manual_match = re.search(r"Manual Domain:\s*(.+)", title_text)
    local_match = re.search(r"Local Domain:\s*(.+)", title_text)
    conf_match = re.search(r"Confidence:\s*([0-9.]+)", title_text)

    if manual_match:
        parsed["manual_domain"] = manual_match.group(1).strip().lower()

    if local_match:
        parsed["local_domain"] = local_match.group(1).strip().lower()

    if conf_match:
        parsed["confidence"] = float(conf_match.group(1).strip())

    return parsed


def soft_weight(conf: float) -> float:
    if conf >= 0.8:
        return 1.00
    if conf >= 0.6:
        return 0.85
    if conf >= 0.4:
        return 0.65
    if conf >= 0.2:
        return 0.45

    return 0.25


def build_domain_points(snapshot: dict) -> dict:
    domain_points = {}

    for node in snapshot["nodes"]:
        node_x = node.get("x")
        node_y = node.get("y")

        if node_x is None or node_y is None:
            continue

        title_info = parse_node_title(str(node.get("title", "")))
        local_domain = title_info["local_domain"] or "unknown"
        confidence = title_info["confidence"]

        if local_domain not in domain_points:
            domain_points[local_domain] = {
                "color": snapshot["group_colors"].get(local_domain, "#D3D3D3"),
                "points": [],
            }

        domain_points[local_domain]["points"].append(
            (float(node_x), float(node_y), soft_weight(confidence))
        )

    return domain_points


def compute_canvas_bounds(snapshot: dict) -> tuple[float, float, float, float]:
    xs = []
    ys = []

    for node in snapshot["nodes"]:
        if node.get("x") is not None and node.get("y") is not None:
            xs.append(float(node["x"]))
            ys.append(float(node["y"]))

    xs.extend([760, 760])
    ys.extend([470, 250])

    pad_x = 220
    pad_y = 180

    min_x = min(xs) - pad_x
    max_x = max(xs) + pad_x
    min_y = min(ys) - pad_y
    max_y = max(ys) + pad_y

    return min_x, max_x, min_y, max_y


def build_density_grid(domain_points, bounds, grid_size=260, sigma=120.0):
    min_x, max_x, min_y, max_y = bounds

    xs = np.linspace(min_x, max_x, grid_size)
    ys = np.linspace(min_y, max_y, grid_size)

    X, Y = np.meshgrid(xs, ys)
    fields = {}

    for domain, info in domain_points.items():
        Z = np.zeros_like(X, dtype=float)

        for px, py, weight in info["points"]:
            d2 = (X - px) ** 2 + (Y - py) ** 2
            Z += weight * np.exp(-d2 / (2.0 * sigma ** 2))

        fields[domain] = {
            "color": info["color"],
            "Z": Z,
        }

    return X, Y, fields


def polygon_to_svg_path(seg):
    if seg is None or len(seg) < 3:
        return None

    parts = [f"M {seg[0][0]:.2f} {seg[0][1]:.2f}"]

    for pt in seg[1:]:
        parts.append(f"L {pt[0]:.2f} {pt[1]:.2f}")

    parts.append("Z")
    return " ".join(parts)


def extract_domain_polygons(X, Y, fields):
    domain_polygons = {}
    opacities = [0.16, 0.22, 0.30]

    for domain, info in fields.items():
        Z = info["Z"]
        color = info["color"]
        zmax = float(np.max(Z))

        if zmax <= 1e-8:
            continue

        raw_levels = [zmax * 0.22, zmax * 0.40, zmax * 0.62, zmax * 1.001]
        levels = sorted(set(raw_levels))

        if len(levels) < 2:
            continue

        fig, ax = plt.subplots(figsize=(4, 4))
        cs = ax.contourf(X, Y, Z, levels=levels)
        plt.close(fig)

        polygons = []

        for band_idx, segs in enumerate(cs.allsegs):
            opacity = opacities[min(band_idx, len(opacities) - 1)]

            for seg in segs:
                if seg is None or len(seg) < 3:
                    continue

                path_d = polygon_to_svg_path(seg)

                if path_d:
                    polygons.append(
                        {
                            "path": path_d,
                            "opacity": opacity,
                        }
                    )

        if polygons:
            domain_polygons[domain] = {
                "color": color,
                "polygons": polygons,
            }

    return domain_polygons


def build_regions_svg(snapshot: dict) -> tuple[str, tuple[float, float, float, float]]:
    domain_points = build_domain_points(snapshot)
    bounds = compute_canvas_bounds(snapshot)
    X, Y, fields = build_density_grid(domain_points, bounds, grid_size=260, sigma=120.0)
    domain_polygons = extract_domain_polygons(X, Y, fields)

    min_x, max_x, min_y, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    domain_order = [
        "bias",
        "school",
        "family",
        "access",
        "environment",
        "work",
        "controversial",
        "treatment",
        "clinical",
        "core",
        "unknown",
    ]

    svg_parts = []

    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{min_x:.2f} {min_y:.2f} {width:.2f} {height:.2f}" '
        f'preserveAspectRatio="none">'
    )

    svg_parts.append(
        """
<defs>
  <filter id="softBlur" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="6" />
  </filter>
</defs>
"""
    )

    for domain in domain_order:
        if domain not in domain_polygons:
            continue

        color = domain_polygons[domain]["color"]
        polygons = domain_polygons[domain]["polygons"]

        svg_parts.append(f'<g id="region-{domain}" filter="url(#softBlur)">')

        for poly in polygons:
            svg_parts.append(
                f'<path d="{poly["path"]}" '
                f'fill="{color}" fill-opacity="{poly["opacity"]:.3f}" '
                f'stroke="{color}" stroke-opacity="0.35" stroke-width="8" '
                f'stroke-linejoin="round" />'
            )

        svg_parts.append("</g>")

    svg_parts.append("</svg>")

    return "\n".join(svg_parts), bounds


def inject_background_into_html(graph_html: str, snapshot: dict) -> str:
    svg_text, bounds = build_regions_svg(snapshot)

    min_x, max_x, min_y, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    svg_b64 = base64.b64encode(svg_text.encode("utf-8")).decode("utf-8")
    svg_data_url = f"data:image/svg+xml;base64,{svg_b64}"

    js_block = f"""
<script type="text/javascript">
window.addEventListener("load", function() {{
    var bgImage = new Image();
    bgImage.src = "{svg_data_url}";

    bgImage.onload = function() {{
        if (typeof network !== "undefined") {{
            network.on("beforeDrawing", function(ctx) {{
                ctx.save();
                ctx.globalAlpha = 1.0;
                ctx.drawImage(
                    bgImage,
                    {min_x},
                    {min_y},
                    {width},
                    {height}
                );
                ctx.restore();
            }});
            network.redraw();
        }}
    }};
}});
</script>
"""

    if "</body>" in graph_html:
        graph_html = graph_html.replace("</body>", js_block + "\n</body>", 1)
    else:
        graph_html += "\n" + js_block

    return graph_html


def extract_strength_from_title(title: str) -> float:
    if not title:
        return 0.0

    match = re.search(r"Strength:\s*([0-9.]+)", title)

    if match:
        return float(match.group(1))

    return 0.0


def build_network_html(snapshot: dict, strength_threshold: float, graph_height: int) -> str:
    net = Network(
        height=f"{graph_height}px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
    )

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
        strength = extract_strength_from_title(original_edge.get("title", ""))

        if strength < strength_threshold:
            continue

        edge_payload = dict(original_edge)
        source_id = edge_payload.pop("from")
        target_id = edge_payload.pop("to")

        net.add_edge(source_id, target_id, **edge_payload)

    graph_html = net.generate_html(notebook=False)
    graph_html = inject_background_into_html(graph_html, snapshot)
    graph_html += f"<!-- refresh {time.time()} -->"

    return graph_html


SNAPSHOTS = load_all_snapshots()

if not SNAPSHOTS:
    st.error("No year-age graph source files were found next to this app.")
    st.stop()

available_years = sorted(SNAPSHOTS.keys())

st.markdown("""
<h2 style="margin:0; padding:0; line-height:1.15;">
Chronological Year + Age Graph Explorer
</h2>
<p style="margin:3px 0 10px 0; font-size:13px; color:#9ca3af;">
Choose a year and age to switch between fixed graph snapshots.
</p>
""", unsafe_allow_html=True)

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

strength_threshold = st.sidebar.slider(
    "Minimum edge strength",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.01,
)

selected_snapshot = SNAPSHOTS[selected_year][selected_age]

with st.sidebar.expander("Node Changes", expanded=False):
    compare_mode = st.radio(
        "Compare with",
        ["Previous year", "Previous age"],
        index=0,
        horizontal=True,
    )

    comparison_snapshot = None
    comparison_label = None

    if compare_mode == "Previous year":
        previous_years = [y for y in available_years if y < selected_year]

        if previous_years:
            prev_year = max(previous_years)

            if selected_age in SNAPSHOTS[prev_year]:
                comparison_snapshot = SNAPSHOTS[prev_year][selected_age]
                comparison_label = f"{prev_year} | Age {selected_age}"

    else:
        previous_ages = [a for a in year_specific_ages if a < selected_age]

        if previous_ages:
            prev_age = max(previous_ages)
            comparison_snapshot = SNAPSHOTS[selected_year][prev_age]
            comparison_label = f"{selected_year} | Age {prev_age}"

    if comparison_snapshot is None:
        st.caption("No comparison available.")

    else:
        added_nodes, removed_nodes = compare_nodes(
            selected_snapshot,
            comparison_snapshot,
        )

        st.caption(f"Compared with: {comparison_label}")

        change_tab = st.radio(
            "Change type",
            [f"Added ({len(added_nodes)})", f"Removed ({len(removed_nodes)})"],
            horizontal=True,
            label_visibility="collapsed",
        )

        active_nodes = added_nodes if change_tab.startswith("Added") else removed_nodes
        active_color = "#86efac" if change_tab.startswith("Added") else "#fca5a5"
        active_label = "Added Node" if change_tab.startswith("Added") else "Removed Node"

        if not active_nodes:
            st.info("No nodes in this category.")

        else:
            selected_changed_node = st.selectbox(
                active_label,
                active_nodes,
                index=0,
            )

            st.markdown(
                f"""
                <div style="
                    background:{active_color};
                    color:#111827;
                    padding:12px 12px;
                    border-radius:10px;
                    font-size:14px;
                    font-weight:700;
                    line-height:1.35;
                    margin-top:8px;
                    margin-bottom:6px;
                    word-break:break-word;
                    min-height:42px;
                ">
                    {html.escape(selected_changed_node)}
                </div>
                """,
                unsafe_allow_html=True,
            )


if streamlit_js_eval is not None:
    viewport_height = streamlit_js_eval(
        js_expressions="window.innerHeight",
        key="viewport_height",
    )
else:
    viewport_height = None

try:
    viewport_height = int(viewport_height) if viewport_height else 900
except Exception:
    viewport_height = 900

graph_height = max(560, min(720, viewport_height - 250))

graph_html = build_network_html(
    selected_snapshot,
    strength_threshold,
    graph_height,
)

left_col, right_col = st.columns([4.8, 1.2], gap="medium")

with left_col:
    st.markdown(
        f"<div style='font-size:17px; font-weight:700; margin:0 0 6px 0;'>"
        f"Graph: {selected_year} | Age {selected_age}"
        f"</div>",
        unsafe_allow_html=True,
    )

    components.html(
        graph_html,
        height=graph_height + 35,
        scrolling=False,
    )

with right_col:
    st.markdown(
        "<div style='font-size:16px; font-weight:700; margin:0 0 2px 0;'>Snapshot</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Info", "Edges", "Groups", "Legend"])

    with tab1:
        st.write(f"**Year:** {selected_year}")
        st.write(f"**Age:** {selected_age}")
        st.write(f"**Source:** `{selected_snapshot['file_name']}`")
        st.write(f"**Nodes:** {len(selected_snapshot['nodes'])}")
        st.write(f"**Edges:** {len(selected_snapshot['edges'])}")

        persona_text = clean_multiline_text(selected_snapshot["persona_text"])

        if persona_text:
            st.markdown("**Description**")
            st.caption(persona_text)

    with tab2:
        st.markdown("""
**Pastel teal edge (+):** positive effect  
**Dusty rose edge (-):** negative effect  
**Arrow:** source influences target  
**Thickness:** causal strength  
**Hover:** reason + strength
""")

        with tab3:
            group_items = list(selected_snapshot["group_colors"].items())

            groups_html = '<div style="display:grid; grid-template-columns:1fr 1fr; column-gap:18px; row-gap:10px; margin-top:8px;">'

            for group_name, group_color in group_items:
                raw_description = selected_snapshot["group_descriptions"].get(group_name, "")

                safe_name = clean_text(group_name.replace("_", " ").title())
                safe_desc = clean_text(raw_description)

                groups_html += (
                    f'<div style="min-height:48px;">'
                    f'<div style="display:flex; align-items:center; gap:6px;">'
                    f'<span style="display:inline-block; width:10px; height:10px; '
                    f'border-radius:50%; background:{group_color}; flex-shrink:0;"></span>'
                    f'<span style="font-size:12px; font-weight:700;">{safe_name}</span>'
                    f'</div>'
                    f'<div style="font-size:10px; color:#9ca3af; margin-left:16px; '
                    f'margin-top:2px; line-height:1.25;">{safe_desc}</div>'
                    f'</div>'
                )

            groups_html += "</div>"

            st.markdown(groups_html, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
**Node Border Color**  
Manual domain from `node_groups`.

**Background Regions**  
Fuzzy local clusters from node positions and domain colors.

**Manual Domain**  
Predefined category: clinical, access, bias, treatment, school, work, family, core, etc.

**Local Domain**  
Cluster-based grouping from `clusters.json`.

**Hover Info**  
Shows domain, explanation, and strength.
""")