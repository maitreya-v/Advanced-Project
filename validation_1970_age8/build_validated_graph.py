"""Build a standalone graph that displays every edge's validation decision."""
from pathlib import Path
import html
import json
import os
import re
import sys

from pyvis.network import Network

BASE = Path(__file__).resolve().parent
PROJECT_ROOT = BASE.parent
sys.path.insert(0, str(PROJECT_ROOT))
MATCH = re.fullmatch(r"validation_(\d{4})_age(\d+)", BASE.name)
if not MATCH:
    raise RuntimeError(f"Unexpected validation folder name: {BASE.name}")

YEAR, AGE = MATCH.groups()
GRAPH = PROJECT_ROOT / f"{YEAR}_{AGE} yo.py"
REPORT = BASE / "edge_validation.json"
OUTPUT = BASE / "validated_graph.html"

STATUS_STYLES = {
    "supported": {"color": "#16a34a", "dashes": False, "label": "Supported"},
    "partially_supported": {"color": "#2563eb", "dashes": [10, 5], "label": "Partially supported"},
    "contradicted": {"color": "#dc2626", "dashes": [3, 5], "label": "Contradicted"},
    "mixed_evidence": {"color": "#7c3aed", "dashes": [10, 4, 2, 4], "label": "Mixed evidence"},
    "insufficient_evidence": {"color": "#9ca3af", "dashes": [6, 6], "label": "Insufficient evidence"},
    "not_assessable": {"color": "#f59e0b", "dashes": [2, 6], "label": "Not assessable"},
}


class CaptureNetwork:
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
        payload = dict(kwargs)
        if args:
            payload.setdefault("id", args[0])
        self.nodes.append(payload)

    def add_edge(self, *args, **kwargs):
        payload = dict(kwargs)
        if len(args) > 0:
            payload.setdefault("from", args[0])
        if len(args) > 1:
            payload.setdefault("to", args[1])
        self.edges.append(payload)

    def write_html(self, *args, **kwargs):
        return None

    def generate_html(self, *args, **kwargs):
        return ""


def capture_graph():
    code = GRAPH.read_text(encoding="utf-8")
    code = re.sub(r"^\s*from pyvis\.network import Network\s*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*from graph_background_utils import .*$", "", code, flags=re.MULTILINE)
    namespace = {"__name__": "__validated_graph_loader__", "Network": CaptureNetwork}
    previous_cwd = Path.cwd()
    try:
        os.chdir(PROJECT_ROOT)
        exec(code, namespace)
    finally:
        os.chdir(previous_cwd)
    return namespace["net"]


def build():
    captured = capture_graph()
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    decisions = report["edges"]
    graph_edges = [edge for edge in captured.edges]

    if len(decisions) != len(graph_edges):
        raise RuntimeError(f"Expected {len(graph_edges)} decisions, found {len(decisions)}")

    net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff", cdn_resources="in_line")
    net.set_options('''
    var options = {
      "layout": {"improvedLayout": false},
      "physics": {"enabled": false},
      "interaction": {"dragNodes": false, "dragView": true, "zoomView": true, "hover": true, "navigationButtons": true},
      "edges": {"smooth": false, "font": {"size": 12, "align": "top"}}
    }
    ''')

    helper_nodes = {"LEGEND_NODE", "PERSONA_DESC", "PERIOD_NODE", "Persona", "PERSONA_NODE"}
    for original in captured.nodes:
        payload = dict(original)
        node_id = payload.pop("id")
        if node_id in helper_nodes:
            continue
        net.add_node(node_id, **payload)

    for decision, original in zip(decisions, graph_edges):
        payload = dict(original)
        source = payload.pop("from")
        destination = payload.pop("to")
        if (decision["source"], decision["dest"]) != (source, destination):
            raise RuntimeError(f"Decision {decision['edge_id']} does not match graph edge {source} -> {destination}")

        status = decision["validation_status"]
        style = STATUS_STYLES[status]
        original_title = payload.get("title", "")
        payload["color"] = style["color"]
        payload["dashes"] = style["dashes"]
        payload["title"] = (
            f"{original_title}\n\nValidation: {style['label']}\n"
            f"Decision: {decision['observation_from_validation']}\n"
            f"Recommended action: {decision['recommended_action']}"
        )
        net.add_edge(source, destination, **payload)

    graph_html = net.generate_html(notebook=False)
    counts = report["metadata"]["status_counts"]
    legend_rows = "".join(
        f'<div style="margin:5px 0"><span style="display:inline-block;width:22px;border-top:4px solid {style["color"]};margin-right:8px"></span>'
        f'{html.escape(style["label"])}: {counts.get(status, 0)}</div>'
        for status, style in STATUS_STYLES.items()
    )
    legend = f'''<div style="position:fixed;right:18px;top:18px;z-index:9999;background:rgba(255,255,255,.94);border:1px solid #d1d5db;border-radius:10px;padding:12px 16px;font:13px Arial;color:#111827;box-shadow:0 2px 10px rgba(0,0,0,.12)"><b>{YEAR} | Age {AGE} validation</b>{legend_rows}<div style="margin-top:8px;color:#6b7280;max-width:260px">All original edges are retained. Hover over an edge for the decision and recommended action.</div></div>'''
    graph_html = graph_html.replace("</body>", legend + "</body>", 1)
    OUTPUT.write_text(graph_html, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(graph_edges)} validated edges")


if __name__ == "__main__":
    build()
