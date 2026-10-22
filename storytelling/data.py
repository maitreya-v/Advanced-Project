"""Read authored graph records without executing the visualization scripts."""
from __future__ import annotations

import ast
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_STATUS = "Authored model; scientific validation pending"


def stable_id(source: str, target: str) -> str:
    return "e_" + hashlib.sha256(json.dumps([source, target]).encode()).hexdigest()[:16]


def load_evidence_registry(path: Path | None = None) -> dict:
    path = path or ROOT / "storytelling" / "evidence.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("version") != "1" or not isinstance(payload.get("edges"), dict):
        raise ValueError("The evidence registry has an unsupported format.")
    for edge_id, record in payload["edges"].items():
        if not re.fullmatch(r"e_[0-9a-f]{16}", edge_id):
            raise ValueError(f"Invalid evidence edge ID: {edge_id}")
        if not isinstance(record.get("quality_label"), str) or not isinstance(record.get("citations", []), list):
            raise ValueError(f"Invalid evidence record: {edge_id}")
        for citation in record.get("citations", []):
            if not str(citation.get("url", "")).startswith("https://"):
                raise ValueError(f"Evidence citations must use HTTPS: {edge_id}")
    return payload["edges"]


def literals(path: Path) -> dict:
    wanted = {"node_groups", "group_colors", "group_descriptions", "fallback_positions", "edges"}
    result = {}
    for item in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    result[target.id] = ast.literal_eval(item.value)
    if not {"node_groups", "edges"} <= result.keys():
        raise ValueError(f"Missing graph records in {path.name}")
    return result


def load_snapshot(path: Path, positions: dict) -> dict:
    match = re.fullmatch(r"(\d{4})_(\d+)\s*yo\.py", path.name)
    if not match:
        raise ValueError(f"Unrecognized snapshot filename: {path.name}")
    raw = literals(path)
    year, age = map(int, match.groups())
    colors = raw.get("group_colors", {})
    nodes = []
    for index, (name, domain) in enumerate(raw["node_groups"].items()):
        pos = positions.get(name, raw.get("fallback_positions", {}).get(name, {}))
        angle = 2 * math.pi * index / len(raw["node_groups"])
        nodes.append({
            "id": name, "label": name, "domain": domain,
            "x": pos.get("x", 650 * math.cos(angle)),
            "y": pos.get("y", 650 * math.sin(angle)),
            "fixed": True, "physics": False,
            "size": 32 if domain == "core" else 21,
            "color": {"background": "#f7f9fc", "border": colors.get(domain, "#aab4c0")},
            "borderWidth": 3,
            "font": {"size": 13, "color": "#24344a"},
            "title": (f"Node: {name}\nManual Domain: {domain}\n"
                      f"Local Domain: {pos.get('local_domain', domain)}\n"
                      f"Confidence: {pos.get('confidence', 0):.2f}\n"
                      "Confidence is layout neighborhood agreement, not scientific evidence."),
        })
    ids = {n["id"] for n in nodes}
    edges, seen = [], set()
    for source, target, sign, strength, explanation in raw["edges"]:
        edge_id = stable_id(source, target)
        if source not in ids or target not in ids:
            raise ValueError(f"Unknown edge endpoint in {path.name}: {source} → {target}")
        if edge_id in seen:
            raise ValueError(f"Duplicate edge in {path.name}: {source} → {target}")
        if sign not in ("+", "-") or not 0 <= strength <= 1:
            raise ValueError(f"Invalid sign or strength in {path.name}")
        seen.add(edge_id)
        edges.append({
            "id": edge_id, "from": source, "to": target,
            "sign": sign, "strength": float(strength), "explanation": explanation,
            "evidence_status": EVIDENCE_STATUS, "source_file": path.name,
            "color": "#48a88d" if sign == "+" else "#cf7b8a",
            "width": max(2, strength * 6), "arrows": "to",
            "title": f"{source} → {target}\nSign: {sign}\nStrength: {strength:.2f}\n{explanation}\n{EVIDENCE_STATUS}",
        })
    snapshot = {
        "year": year, "age": age, "file_name": path.name, "nodes": nodes, "edges": edges,
        "node_groups": raw["node_groups"], "group_colors": colors,
        "group_descriptions": raw.get("group_descriptions", {}),
        "ordered_groups": list(dict.fromkeys(raw["node_groups"].values())),
        "legend_text": "", "persona_text": "",
    }
    # Keep scientific-evidence metadata outside the structural fingerprint so
    # literature review updates do not invalidate otherwise grounded stories.
    snapshot["fingerprint"] = hashlib.sha256(json.dumps(snapshot, sort_keys=True).encode()).hexdigest()
    registry = load_evidence_registry()
    for edge in snapshot["edges"]:
        evidence = registry.get(edge["id"], {})
        edge["evidence_quality"] = evidence.get("quality_label", "Not yet reviewed")
        edge["evidence_summary"] = evidence.get(
            "summary", "No literature source has been attached to this authored relationship yet."
        )
        edge["citations"] = evidence.get("citations", [])
        edge["evidence_status"] = edge["evidence_quality"]
        edge["title"] += f"\nEvidence: {edge['evidence_quality']}"
    return snapshot


def load_snapshots(root: Path = ROOT) -> dict[int, dict[int, dict]]:
    positions = json.loads((root / "clusters.json").read_text(encoding="utf-8"))
    snapshots = {}
    for path in sorted(root.glob("*yo.py")):
        snapshot = load_snapshot(path, positions)
        snapshots.setdefault(snapshot["year"], {})[snapshot["age"]] = snapshot
    return snapshots
