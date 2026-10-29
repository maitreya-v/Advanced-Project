"""Structural A-to-B comparisons between any two canonical graph scenarios."""
from math import isclose


def compare_scenarios(a: dict, b: dict) -> dict:
    """Compare full snapshots, regardless of year/age ordering or route filters.

    Match directed relationships by endpoints. A sign change and a strength
    change can both apply to the same relationship and are reported separately.
    """
    old = {(edge["from"], edge["to"]): edge for edge in a["edges"]}
    new = {(edge["from"], edge["to"]): edge for edge in b["edges"]}
    nodes_a, nodes_b = ({node["id"] for node in snapshot["nodes"]} for snapshot in (a, b))

    def row(pair):
        before, after = old.get(pair), new.get(pair)
        return {"source": pair[0], "target": pair[1],
                "sign_a": before["sign"] if before else None,
                "sign_b": after["sign"] if after else None,
                "strength_a": before["strength"] if before else None,
                "strength_b": after["strength"] if after else None,
                "delta": round(after["strength"] - before["strength"], 10) if before and after else None}

    common = sorted(old.keys() & new.keys())
    sign_changes = [pair for pair in common if old[pair]["sign"] != new[pair]["sign"]]
    strength_changes = [pair for pair in common if not isclose(old[pair]["strength"], new[pair]["strength"], rel_tol=0, abs_tol=1e-9)]
    changed = set(sign_changes) | set(strength_changes)
    return {
        "scenario_a": {key: a[key] for key in ("year", "age", "fingerprint")},
        "scenario_b": {key: b[key] for key in ("year", "age", "fingerprint")},
        "added_nodes": sorted(nodes_b - nodes_a), "removed_nodes": sorted(nodes_a - nodes_b),
        "added_edges": [row(pair) for pair in sorted(new.keys() - old.keys())],
        "removed_edges": [row(pair) for pair in sorted(old.keys() - new.keys())],
        "sign_changes": [row(pair) for pair in sign_changes],
        "strength_changes": [row(pair) for pair in strength_changes],
        "unchanged_edges": [row(pair) for pair in common if pair not in changed],
    }
