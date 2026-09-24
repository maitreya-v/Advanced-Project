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
    references = {
        item.get("pmid") or item["source_id"]: item
        for item in report["references"]
    }
    graph_edges = [edge for edge in captured.edges]
    evidence_by_edge = {}

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
        edge_id = f"validation-edge-{decision['edge_id']}"
        payload["id"] = edge_id
        payload["color"] = style["color"]
        payload["dashes"] = style["dashes"]
        payload["title"] = (
            f"{original_title}\n\nValidation: {style['label']}\n"
            "Click this edge to inspect the research evidence."
        )
        evidence_items = []
        for item in decision["evidence"]:
            source_key = item.get("pmid") or item["source_id"]
            reference = references[source_key]
            page_match = re.search(r"PDF page\s+(\d+)", item["location"])
            page_fragment = f"#page={page_match.group(1)}" if page_match else ""
            evidence_items.append({
                **item,
                "source_label": f"PMID {source_key}" if item.get("pmid") else source_key,
                "citation": reference.get("citation") or reference["title"],
                "paper_url": reference.get("url"),
                "doi_url": f"https://doi.org/{reference['doi']}" if reference.get("doi") else None,
                "local_pdf": f"{reference['local_pdf']}{page_fragment}",
                "evidence_scope": reference.get("evidence_scope", ""),
            })
        evidence_by_edge[edge_id] = {
            "edge_id": decision["edge_id"],
            "source": source,
            "destination": destination,
            "status": style["label"],
            "status_color": style["color"],
            "decision": decision["observation_from_validation"],
            "recommended_action": decision["recommended_action"],
            "evidence": evidence_items,
        }
        net.add_edge(source, destination, **payload)

    graph_html = net.generate_html(notebook=False)
    counts = report["metadata"]["status_counts"]
    legend_rows = "".join(
        f'<div style="margin:5px 0"><span style="display:inline-block;width:22px;border-top:4px solid {style["color"]};margin-right:8px"></span>'
        f'{html.escape(style["label"])}: {counts.get(status, 0)}</div>'
        for status, style in STATUS_STYLES.items()
    )
    legend = f'''<div id="validation-legend" style="position:fixed;right:18px;top:18px;z-index:9998;background:rgba(255,255,255,.94);border:1px solid #d1d5db;border-radius:10px;padding:12px 16px;font:13px Arial;color:#111827;box-shadow:0 2px 10px rgba(0,0,0,.12)"><b>{YEAR} | Age {AGE} validation</b>{legend_rows}<div style="margin-top:8px;color:#6b7280;max-width:260px">All original edges are retained. Click an edge to inspect its research evidence.</div></div>'''
    evidence_json = json.dumps(evidence_by_edge, ensure_ascii=False).replace("</", "<\\/")
    evidence_panel = f'''
<style>
#evidence-panel {{ position:fixed; right:0; top:0; bottom:0; width:420px; z-index:10000; background:#fff; border-left:1px solid #d1d5db; box-shadow:-5px 0 18px rgba(0,0,0,.16); transform:translateX(105%); transition:transform .2s ease; overflow-y:auto; padding:20px; font:14px/1.45 Arial,sans-serif; color:#111827; }}
#evidence-panel.open {{ transform:translateX(0); }}
#evidence-panel h2 {{ font-size:19px; margin:0 34px 5px 0; }}
#evidence-panel h3 {{ font-size:15px; margin:20px 0 8px; }}
#evidence-panel .status {{ display:inline-block; color:#fff; font-weight:700; border-radius:999px; padding:4px 9px; margin:5px 0 10px; }}
#evidence-panel .evidence-card {{ border:1px solid #d1d5db; border-radius:9px; padding:12px; margin:10px 0; background:#f9fafb; }}
#evidence-panel mark {{ display:block; background:#fef3c7; color:#111827; padding:10px; border-left:4px solid #f59e0b; margin:9px 0; white-space:normal; }}
#evidence-panel a {{ color:#1d4ed8; font-weight:600; margin-right:12px; }}
#evidence-close {{ position:absolute; right:14px; top:12px; border:0; background:#e5e7eb; border-radius:50%; width:30px; height:30px; cursor:pointer; font-size:18px; }}
</style>
<aside id="evidence-panel" aria-label="Research evidence">
  <button id="evidence-close" aria-label="Close evidence panel">×</button>
  <div id="evidence-content"></div>
</aside>
<script>
const validationEvidence = {evidence_json};
const evidencePanel = document.getElementById('evidence-panel');
const evidenceContent = document.getElementById('evidence-content');
function addText(tag, text, className) {{ const el=document.createElement(tag); el.textContent=text; if(className) el.className=className; evidenceContent.appendChild(el); return el; }}
function addLink(parent, text, href) {{ const a=document.createElement('a'); a.textContent=text; a.href=href; a.target='_blank'; a.rel='noopener'; parent.appendChild(a); }}
function showEvidence(edgeId) {{
  const item=validationEvidence[edgeId]; if(!item) return;
  evidenceContent.replaceChildren();
  addText('h2', item.source+' → '+item.destination);
  const badge=addText('div', item.status, 'status'); badge.style.background=item.status_color;
  addText('h3','Validation decision'); addText('p',item.decision);
  addText('h3','Recommended action'); addText('p',item.recommended_action);
  addText('h3','Research evidence');
  if(!item.evidence.length) {{ addText('p','No directly relevant excerpt was found in the four-paper corpus. The decision is based on the absence of suitable evidence or an undefined graph construct.'); }}
  item.evidence.forEach((ev,index) => {{
    const card=document.createElement('section'); card.className='evidence-card'; evidenceContent.appendChild(card);
    const heading=document.createElement('strong'); heading.textContent='Source '+(index+1)+' · '+ev.source_label; card.appendChild(heading);
    const citation=document.createElement('p'); citation.textContent=ev.citation; card.appendChild(citation);
    const quote=document.createElement('mark'); quote.textContent='“'+ev.exact_excerpt+'”'; card.appendChild(quote);
    const location=document.createElement('p'); location.textContent='Location: '+ev.location; card.appendChild(location);
    const relevance=document.createElement('p'); relevance.textContent='Why it matters: '+ev.relevance; card.appendChild(relevance);
    const links=document.createElement('p'); card.appendChild(links);
    addLink(links,'Open supplied PDF',ev.local_pdf); if(ev.paper_url) addLink(links,'Publisher / index',ev.paper_url); if(ev.doi_url) addLink(links,'DOI',ev.doi_url);
  }});
  evidencePanel.classList.add('open');
}}
document.getElementById('evidence-close').addEventListener('click',()=>evidencePanel.classList.remove('open'));
network.on('selectEdge', params => {{ if(params.edges.length) showEvidence(String(params.edges[0])); }});
</script>
'''
    graph_html = graph_html.replace("</body>", legend + evidence_panel + "</body>", 1)
    OUTPUT.write_text(graph_html, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(graph_edges)} validated edges")


if __name__ == "__main__":
    build()
