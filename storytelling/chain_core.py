"""Single-snapshot chain queries and the compact component's data contract."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from collections.abc import MutableMapping

from .path_story import baseline_path_story
from .paths import discover_routes, route_edges

CHAIN_VERSION = "horizontal-chain-v1"


def scenario(snapshot: dict) -> dict:
    return {key: snapshot[key] for key in ("year", "age", "fingerprint")}


def _query(snapshot: dict, start: str, end: str, max_hops: int, minimum_strength: float) -> dict:
    if isinstance(max_hops, bool) or not isinstance(max_hops, int) or not 1 <= max_hops <= 7:
        raise ValueError("Choose one to seven directed steps.")
    if (isinstance(minimum_strength, bool) or not isinstance(minimum_strength, (int, float))
            or not math.isfinite(minimum_strength) or not 0 <= minimum_strength <= 1):
        raise ValueError("Minimum strength must be between zero and one.")
    if not isinstance(start, str) or not isinstance(end, str) or start == end:
        raise ValueError("Choose different starting and ending concepts.")
    return {"start": start, "end": end, "max_hops": max_hops,
            "minimum_strength": float(minimum_strength)}


def _query_id(snapshot: dict, query: dict) -> str:
    encoded = json.dumps([scenario(snapshot), query], sort_keys=True).encode()
    return "cq_" + hashlib.sha256(encoded).hexdigest()[:24]


def query_chains(snapshot: dict, start: str, end: str, *, max_hops: int = 5,
                 minimum_strength: float = 0.0, limit: int = 500,
                 timeout_seconds: float = 1.0) -> dict:
    """Use canonical storytelling snapshots; preserve bounded-search status.

    Missing endpoints are a distinct state so a scenario change can preserve
    the user's endpoints instead of silently replacing them with other nodes.
    """
    query = _query(snapshot, start, end, max_hops, minimum_strength)
    if (isinstance(limit, bool) or not isinstance(limit, int) or limit < 1
            or isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(timeout_seconds) or timeout_seconds <= 0):
        raise ValueError("Use positive search limits.")
    nodes = {node["id"] for node in snapshot["nodes"]}
    missing = [node for node in (start, end) if node not in nodes]
    if missing:
        result = {"paths": [], "complete": False, "stop_reason": "missing_endpoints",
                  "returned_count": 0, "total_count": None, "reachable": False,
                  "query": query, "state": "missing_endpoints", "missing_endpoints": missing}
    else:
        result = discover_routes(snapshot, start, end, max_hops=max_hops,
                                 minimum_strength=minimum_strength, limit=limit,
                                 timeout_seconds=timeout_seconds)
        result["state"] = "ready" if result["paths"] else "no_route"
        result["missing_endpoints"] = []
    return {**result, "scenario": scenario(snapshot), "query_id": _query_id(snapshot, query)}


def build_chain(snapshot: dict, route: dict, *, max_hops: int = 5,
                minimum_strength: float = 0.0) -> dict:
    """Return ordered facts and authored text without calling a model.

    Route IDs remain the existing fingerprint-bound path IDs. Query IDs also
    bind selection events to the active endpoints, hop limit and threshold.
    """
    edges = route_edges(snapshot, route)
    query = _query(snapshot, route["node_ids"][0], route["node_ids"][-1], max_hops, minimum_strength)
    if len(edges) > max_hops or any(edge["strength"] < minimum_strength for edge in edges):
        raise ValueError("This chain does not meet the current route filters.")
    story = baseline_path_story(snapshot, route)
    nodes = {node["id"]: node for node in snapshot["nodes"]}
    return {
        "version": CHAIN_VERSION, "chain_id": route["path_id"],
        "query_id": _query_id(snapshot, query), "scenario": scenario(snapshot), "query": query,
        "node_ids": list(route["node_ids"]), "edge_ids": list(route["edge_ids"]),
        "nodes": [{"id": node_id, "label": nodes[node_id].get("label", node_id),
                   "domain": snapshot["node_groups"].get(node_id, "unknown"),
                   "color": snapshot["group_colors"].get(snapshot["node_groups"].get(node_id), "#8295a3")}
                  for node_id in route["node_ids"]],
        "steps": [{"index": index, "edge_id": edge["id"],
                   "source": edge["from"], "target": edge["to"],
                   "sign": edge["sign"], "strength": edge["strength"],
                   "explanation": edge["explanation"], "reason": chapter["reason"],
                   "examples": list(chapter["examples"]),
                   "snapshot_review": deepcopy(chapter["relationship"].get("snapshot_review"))}
                  for index, (edge, chapter) in enumerate(zip(edges, story["chapters"]))],
        "fiction_note": story["fiction_note"], "origin": story["origin"],
    }


def apply_chain_selection(event: object, chain: dict, state: MutableMapping,
                          *, key: str = "chain") -> bool:
    """Reset selection on context changes; reject stale or mismatched events."""
    context = (chain["query_id"], chain["chain_id"])
    if state.get(key + "_context") != context:
        state[key + "_context"] = context
        state[key + "_step"] = 0
        # A persistent component retains its last value across scenario
        # changes. Keep its event token so returning to an earlier scenario
        # cannot replay that old click as a new selection.
        state.setdefault(key + "_event", None)
    if not isinstance(event, dict):
        return False
    index = event.get("step_index")
    event_id = event.get("event_id")
    if (event.get("version") != CHAIN_VERSION or event.get("query_id") != chain["query_id"]
            or event.get("chain_id") != chain["chain_id"] or event.get("scenario") != chain["scenario"]
            or isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(chain["steps"])
            or not isinstance(event_id, str) or not 1 <= len(event_id) <= 128):
        return False
    if event.get("edge_id") != chain["steps"][index]["edge_id"] or state.get(key + "_event") == event_id:
        return False
    state[key + "_step"] = index
    state[key + "_event"] = event_id
    return True
