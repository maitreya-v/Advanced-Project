"""Attach reviewed edge decisions to dashboard snapshots and render references."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import re

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
VALIDATED_YEARS = {1970, 1990, 2010, 2026}
STATUS_STYLES = {
    "supported": {"color": "#16a34a", "dashes": False, "label": "Supported"},
    "partially_supported": {"color": "#2563eb", "dashes": [10, 5], "label": "Partially supported"},
    "contradicted": {"color": "#dc2626", "dashes": [3, 5], "label": "Contradicted"},
    "mixed_evidence": {"color": "#7c3aed", "dashes": [10, 4, 2, 4], "label": "Mixed evidence"},
    "insufficient_evidence": {"color": "#9ca3af", "dashes": [6, 6], "label": "Insufficient evidence"},
    "not_assessable": {"color": "#f59e0b", "dashes": [2, 6], "label": "Not assessable"},
}

graph_component = components.declare_component(
    "dashboard_validated_graph", path=str(ROOT / "dashboard_graph_component")
)
popup_component = components.declare_component(
    "dashboard_validation_popup", path=str(ROOT / "dashboard_validation_popup")
)


def attach_validation(snapshot, root=ROOT):
    if snapshot["year"] not in VALIDATED_YEARS:
        return snapshot

    folder = root / f"validation_{snapshot['year']}_age{snapshot['age']}"
    report = json.loads((folder / "edge_validation.json").read_text(encoding="utf-8"))
    source_bytes = (root / snapshot["file_name"]).read_bytes()
    normalized_bytes = source_bytes.replace(b"\r\n", b"\n")
    # The 1970 reports were generated on Windows; accept only newline changes.
    source_hashes = {
        hashlib.sha256(data).hexdigest()
        for data in (source_bytes, normalized_bytes, normalized_bytes.replace(b"\n", b"\r\n"))
    }
    if report["metadata"]["graph_sha256"] not in source_hashes:
        raise ValueError("The graph has changed since validation; reassess before displaying its decisions.")
    if (report["metadata"]["graph_year"], report["metadata"]["age"]) != (snapshot["year"], snapshot["age"]):
        raise ValueError("Validation report does not match this year and age.")
    if len(snapshot["edges"]) != len(report["edges"]):
        raise ValueError("Validation edge count does not match this graph.")

    validated = deepcopy(snapshot)
    decisions = {}
    for edge, decision in zip(validated["edges"], report["edges"]):
        if (edge["from"], edge["to"]) != (decision["source"], decision["dest"]):
            raise ValueError("Validation decision does not match the graph edge.")
        style = STATUS_STYLES[decision["validation_status"]]
        edge_id = f"validation-edge-{decision['edge_id']}"
        edge.update(id=edge_id, color=style["color"], dashes=style["dashes"])
        edge["title"] = (
            edge.get("title", "") + f"\n\nValidation: {style['label']}"
            "\nClick to open the paginated validation panel."
        )
        decisions[edge_id] = decision
    validated["validation"] = {"report": report, "folder": str(folder), "decisions": decisions}
    return validated


def inject_edge_selection(graph_html):
    bridge = """
<script>
network.on('selectEdge', function(params) {
    if (!params.edges.length) return;
    window.parent.postMessage({
        type: 'dashboard-validation-edge',
        edge_id: String(params.edges[0])
    }, '*');
});
</script>
"""
    return graph_html.replace("</body>", bridge + "</body>", 1)


def render_validation(snapshot, selected_edge, panel_height=570):
    validation = snapshot.get("validation")
    if not validation:
        st.caption("No validation report is available for this snapshot.")
        return

    decision = validation["decisions"].get(selected_edge)
    if not decision:
        st.caption("Click an edge in the graph to view its validation and research references.")
        for status, count in validation["report"]["metadata"]["status_counts"].items():
            style = STATUS_STYLES[status]
            st.markdown(f":{ {'supported': 'green', 'partially_supported': 'blue', 'contradicted': 'red', 'mixed_evidence': 'violet', 'insufficient_evidence': 'gray', 'not_assessable': 'orange'}[status]}[**{style['label']}**]: {count}")
        return

    if st.session_state.get("snapshot_tabs") == "Validation":
        show_validation_panel(snapshot, selected_edge, panel_height)
    else:
        st.caption("Select the Validation tab to read the selected edge's evidence.")


def reference_pdf_url(folder, local_file, location):
    """Expose a supplied PDF through the component's existing asset route."""
    if not local_file:
        return None
    source = (Path(folder) / local_file).resolve()
    source.relative_to(ROOT)
    if source.suffix.lower() != ".pdf" or not source.is_file():
        return None
    data = source.read_bytes()
    name = hashlib.sha256(data).hexdigest() + ".pdf"
    asset_folder = ROOT / "dashboard_validation_popup" / "references"
    asset_folder.mkdir(exist_ok=True)
    target = asset_folder / name
    if not target.exists():
        target.write_bytes(data)
    page = re.search(r"PDF page\s+(\d+)", location, re.IGNORECASE)
    return "references/" + name + ("#page=" + page[1] if page else "")


def popup_payload(snapshot, selected_edge):
    validation = snapshot["validation"]
    decision = validation["decisions"][selected_edge]
    references = {
        item.get("pmid") or item["source_id"]: item
        for item in validation["report"]["references"]
    }
    evidence_items = []
    for evidence in decision["evidence"]:
        source_id = evidence.get("pmid") or evidence["source_id"]
        reference = references[source_id]
        evidence_items.append({
            **evidence,
            "source_label": f"PMID {source_id.removeprefix('PMID_')}" if evidence.get("pmid") or source_id.startswith("PMID_") else source_id,
            "citation": reference.get("citation") or reference["title"],
            "scope": reference.get("evidence_scope", ""),
            "url": reference.get("url"),
            "doi_url": "https://doi.org/" + reference["doi"] if reference.get("doi") else None,
            "local_file": reference.get("local_pdf") or reference.get("local_html"),
            "pdf_url": reference_pdf_url(validation["folder"], reference.get("local_pdf"), evidence.get("location", "")),
        })
    return {
        "edge_title": f"{decision['source']} → {decision['dest']}",
        "year": snapshot["year"], "age": snapshot["age"],
        "status": STATUS_STYLES[decision["validation_status"]]["label"],
        "status_color": STATUS_STYLES[decision["validation_status"]]["color"],
        "decision": decision["observation_from_validation"],
        "action": decision["recommended_action"],
        "evidence": evidence_items,
    }


def show_validation_panel(snapshot, selected_edge, panel_height):
    payload = popup_payload(snapshot, selected_edge)
    result = popup_component(
        payload=payload, height=panel_height,
        key=f"validation-panel-{snapshot['year']}-{snapshot['age']}-{selected_edge}-{st.session_state.get('validation_selection_token')}-{st.session_state.get('validation_panel_generation', 0)}",
        default=None,
    )
    if isinstance(result, dict) and result.get("closed"):
        st.session_state["validation_pending_tab"] = "Info"
        st.session_state["validation_panel_generation"] = st.session_state.get("validation_panel_generation", 0) + 1
        st.rerun()
    index = result.get("reference_index") if isinstance(result, dict) else None
    if isinstance(index, int) and not isinstance(index, bool) and 0 <= index < len(payload["evidence"]):
        source_file = payload["evidence"][index]["local_file"]
        if source_file:
            path = (Path(snapshot["validation"]["folder"]) / source_file).resolve()
            path.relative_to(ROOT)
            if path.is_file() and path.suffix.lower() != ".pdf":
                st.download_button(
                    "Download saved abstract",
                    data=path.read_bytes(), file_name=path.name,
                    mime="text/html",
                    key="popup-paper-download", on_click="ignore",
                )
