"""Bounded discovery and verification of ordered directed routes."""
from __future__ import annotations

import hashlib
import json
import time
from copy import deepcopy
from pathlib import Path

import networkx as nx

from .data import ROOT


def route_id(snapshot: dict, edge_ids: list[str]) -> str:
    payload = [snapshot["fingerprint"], edge_ids]
    return "p_" + hashlib.sha256(json.dumps(payload).encode()).hexdigest()[:20]


def route_edges(snapshot: dict, route: dict) -> list[dict]:
    nodes = route["node_ids"]
    if len(nodes) < 2 or len(nodes) != len(set(nodes)):
        raise ValueError("Choose a simple route with at least one directed edge.")
    catalog = {edge["id"]: edge for edge in snapshot["edges"]}
    if len(route["edge_ids"]) != len(nodes) - 1:
        raise ValueError("Route nodes and edges do not match.")
    edges = []
    for source, target, edge_id in zip(nodes, nodes[1:], route["edge_ids"]):
        edge = catalog.get(edge_id)
        if edge is None or (edge["from"], edge["to"]) != (source, target):
            raise ValueError("The route contains a missing or reversed relationship.")
        edges.append(deepcopy(edge))
    if route["path_id"] != route_id(snapshot, route["edge_ids"]):
        raise ValueError("This route belongs to different graph data.")
    return edges


def discover_routes(snapshot: dict, start: str, end: str, max_hops: int = 5,
                    limit: int = 500, timeout_seconds: float = 1.0,
                    minimum_strength: float = 0.0, clock=None) -> dict:
    if not 1 <= max_hops <= 7 or limit < 1 or timeout_seconds <= 0:
        raise ValueError("Use one to seven hops and positive search limits.")
    if not 0 <= minimum_strength <= 1:
        raise ValueError("Minimum strength must be between zero and one.")
    graph = nx.DiGraph()
    graph.add_nodes_from(sorted(node["id"] for node in snapshot["nodes"]))
    edge_lookup = {}
    for edge in snapshot["edges"]:
        if edge["strength"] >= minimum_strength:
            graph.add_edge(edge["from"], edge["to"])
            edge_lookup[edge["from"], edge["to"]] = edge["id"]
    if start not in graph or end not in graph:
        raise ValueError("Both endpoints must be present in this snapshot.")
    if start == end:
        raise ValueError("Choose different start and end concepts. Feedback loops are separate stories.")
    clock = clock or time.monotonic
    deadline = clock() + timeout_seconds
    distances = nx.single_source_shortest_path_length(graph.reverse(copy=False), end)
    reachable = start in distances
    adjacency = {node: sorted(graph.successors(node)) for node in graph}
    stack = [(start,)] if reachable else []
    paths = []
    stop_reason = "exhausted"
    while stack:
        if clock() >= deadline:
            stop_reason = "time_limit"
            break
        path = stack.pop()
        current = path[-1]
        if current == end:
            if len(paths) == limit:
                stop_reason = "path_limit"
                break
            edge_ids = [edge_lookup[source, target] for source, target in zip(path, path[1:])]
            paths.append({
                "path_id": route_id(snapshot, edge_ids), "node_ids": list(path),
                "edge_ids": edge_ids, "hop_count": len(edge_ids),
                "domains": list(dict.fromkeys(snapshot["node_groups"].get(node, "unknown") for node in path)),
            })
            continue
        remaining = max_hops - len(path) + 1
        if remaining <= 0 or distances.get(current, max_hops + 1) > remaining:
            continue
        for target in reversed(adjacency[current]):
            if target not in path and distances.get(target, max_hops + 1) < remaining:
                stack.append(path + (target,))
    paths.sort(key=lambda route: (route["hop_count"], route["node_ids"]))
    complete = stop_reason == "exhausted"
    return {
        "paths": paths, "complete": complete, "stop_reason": stop_reason,
        "returned_count": len(paths), "total_count": len(paths) if complete else None,
        "reachable": reachable,
        "query": {"start": start, "end": end, "max_hops": max_hops,
                  "minimum_strength": minimum_strength},
    }


def path_snapshot(snapshot: dict, route: dict) -> dict:
    edges = route_edges(snapshot, route)
    selected = set(route["node_ids"])
    result = deepcopy(snapshot)
    result["nodes"] = [node for node in result["nodes"] if node["id"] in selected]
    result["edges"] = edges
    return result


def attach_path_review(snapshot: dict, edges: list[dict], root: Path = ROOT) -> list[dict]:
    result = deepcopy(edges)
    folder = root / f"validation_{snapshot['year']}_age{snapshot['age']}"
    report_path = folder / "edge_validation.json"
    if not report_path.exists():
        return result
    report = json.loads(report_path.read_text(encoding="utf-8"))
    metadata = report["metadata"]
    raw = (root / snapshot["file_name"]).read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    hashes = {hashlib.sha256(value).hexdigest() for value in (raw, normalized, normalized.replace(b"\n", b"\r\n"))}
    if metadata["graph_sha256"] not in hashes or (metadata["graph_year"], metadata["age"]) != (snapshot["year"], snapshot["age"]):
        raise ValueError("The snapshot review is stale or belongs to another scenario.")
    decisions = {(item["source"], item["dest"]): item for item in report["edges"]}
    expected = {(edge["from"], edge["to"]) for edge in snapshot["edges"]}
    if len(decisions) != len(report["edges"]) or set(decisions) != expected:
        raise ValueError("The review relationships do not match this snapshot.")
    for edge in result:
        decision = decisions[edge["from"], edge["to"]]
        edge["snapshot_review"] = {
            "status": decision["validation_status"],
            "observation": decision["observation_from_validation"],
            "strength_assessed": metadata.get("strength_assessed", False),
            "source": report_path.relative_to(root).as_posix(),
        }
    return result
