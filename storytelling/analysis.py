"""Deterministic comparison, path discovery and explainable narrative ranking."""
from __future__ import annotations

import hashlib
import json
import re
import networkx as nx

ENGINE_VERSION = "1"
THEMES = {
    "Treatment and access": {"treatment", "access"},
    "School and family": {"school", "family"},
    "Recognition and bias": {"bias", "controversial"},
    "Work and daily life": {"work", "clinical", "environment"},
    "All changes": set(),
}


def story_key(before: dict, after: dict, theme: str, question: str = "") -> str:
    payload = [ENGINE_VERSION, before["fingerprint"], after["fingerprint"], theme, question.strip()]
    return hashlib.sha256(json.dumps(payload).encode()).hexdigest()[:24]


def validate_comparison(before: dict, after: dict) -> str:
    if before["year"] == after["year"] and before["age"] == after["age"]:
        raise ValueError("Choose two different snapshots.")
    if before["age"] == after["age"]:
        if before["year"] > after["year"]:
            raise ValueError("The starting year must come before the ending year.")
        return "historical"
    if before["year"] == after["year"]:
        return "age"
    raise ValueError("Hold age or year constant so the comparison has a clear meaning.")


def compare(before: dict, after: dict) -> dict:
    mode = validate_comparison(before, after)
    old = {e["id"]: e for e in before["edges"]}
    new = {e["id"]: e for e in after["edges"]}
    added, removed = sorted(new.keys() - old.keys()), sorted(old.keys() - new.keys())
    changed = [i for i in sorted(old.keys() & new.keys())
               if old[i]["sign"] != new[i]["sign"] or abs(old[i]["strength"] - new[i]["strength"]) > 1e-9]
    return {"mode": mode, "added": added, "removed": removed, "changed": changed,
            "unchanged": sorted((old.keys() & new.keys()) - set(changed)),
            "added_nodes": sorted({n["id"] for n in after["nodes"]} - {n["id"] for n in before["nodes"]}),
            "removed_nodes": sorted({n["id"] for n in before["nodes"]} - {n["id"] for n in after["nodes"]})}


def fact_catalog(before: dict, after: dict, theme: str, question: str = "") -> list[dict]:
    changes = compare(before, after)
    if changes["mode"] == "historical":
        before_label = f"the {before['year']} snapshot"
        after_label = f"the {after['year']} snapshot"
    else:
        before_label = f"the age {before['age']} scenario"
        after_label = f"the age {after['age']} scenario"
    old = {e["id"]: e for e in before["edges"]}
    new = {e["id"]: e for e in after["edges"]}
    graph = nx.DiGraph()
    for e in after["edges"]:
        graph.add_edge(e["from"], e["to"], edge_id=e["id"])
    domains = {**before["node_groups"], **after["node_groups"]}
    wanted = THEMES.get(theme, set())
    tokens = {t for t in re.findall(r"[a-z]+", question.lower()) if len(t) > 3}
    outcomes = {"Diagnosis Status", "Quality of Life", "Functional Impairment", "Treatment Access"}
    facts = []

    def add(kind, previous, current, claim, title, delta=0.0):
        involved = list(dict.fromkeys([v for e in previous + current for v in (e["from"], e["to"])]))
        theme_relevance = sum(domains.get(n) in wanted for n in involved) / max(1, len(involved)) if wanted else 0.5
        matched = sorted(t for t in tokens if t in " ".join(involved).lower())
        query_relevance = len(matched) / max(1, len(tokens))
        relevance = max(theme_relevance, query_relevance)
        novelty = {"added": 1, "removed": 1, "restructured": 1, "sign_changed": 1,
                   "strengthened": 0.35, "weakened": 0.35, "unchanged": 0}[kind]
        reach = float(bool(outcomes.intersection(involved)))
        # Weights describe editorial priority, never evidence or causal certainty.
        parts = {"relevance": round(40 * relevance, 2), "novelty": 25 * novelty,
                 "weight_change": round(20 * min(abs(delta), 1), 2), "outcome_connection": 15 * reach}
        key = json.dumps([kind, [e["id"] for e in previous], [e["id"] for e in current]])
        facts.append({"id": "f_" + hashlib.sha256(key.encode()).hexdigest()[:12],
                      "kind": kind, "title": title, "claim": claim, "nodes": involved,
                      "before_edges": previous, "after_edges": current,
                      "score": round(sum(parts.values()), 2), "score_parts": parts,
                      "rank_reason": f"Theme relevance {parts['relevance']:g}/40 · novelty {parts['novelty']:g}/25 · weight change {parts['weight_change']:g}/20 · outcome connection {parts['outcome_connection']:g}/15",
                      "matched_terms": matched})

    restructured = set()
    for eid in changes["removed"]:
        e = old[eid]
        if e["from"] in graph and e["to"] in graph:
            paths = list(nx.all_simple_paths(graph, e["from"], e["to"], cutoff=3))
            paths.sort(key=lambda p: (len(p), p))
            if paths:
                path = paths[0]
                edges = [new[graph[a][b]["edge_id"]] for a, b in zip(path, path[1:])]
                add("restructured", [e], edges,
                    f"{before_label.capitalize()} directly links {e['from']} to {e['to']}. That direct edge is absent from {after_label}, which contains the path {' → '.join(path)}. This is a structural comparison, not proof that the path is causally equivalent.",
                    f"A different route to {e['to']}")
                restructured.add(eid)
    for eid in changes["added"]:
        e = new[eid]
        add("added", [], [e],
            f"{after_label.capitalize()} includes {e['from']} → {e['to']} (sign {e['sign']}, modeled strength {e['strength']:.2f}); this edge is absent from {before_label}. Absence does not establish that the relationship did not exist in reality.",
            f"A new connection: {e['from']}")
    for eid in changes["removed"]:
        if eid not in restructured:
            e = old[eid]
            add("removed", [e], [],
                f"{e['from']} → {e['to']} appears in {before_label} (sign {e['sign']}, modeled strength {e['strength']:.2f}) and is absent from {after_label}. This describes the model's coverage, not disappearance in reality.",
                f"An earlier connection: {e['from']}")
    for eid in changes["changed"] + changes["unchanged"]:
        a, b = old[eid], new[eid]
        delta = b["strength"] - a["strength"]
        if a["sign"] != b["sign"]:
            kind = "sign_changed"
            claim = f"Between {before_label} and {after_label}, the encoded sign of {b['from']} → {b['to']} changes from {a['sign']} to {b['sign']}; modeled strength changes from {a['strength']:.2f} to {b['strength']:.2f}."
        else:
            kind = "strengthened" if delta > 1e-9 else "weakened" if delta < -1e-9 else "unchanged"
            claim = (f"Between {before_label} and {after_label}, modeled strength for {b['from']} → {b['to']} "
                     + (f"stays at {b['strength']:.2f}" if kind == "unchanged" else f"changes from {a['strength']:.2f} to {b['strength']:.2f}")
                     + f". Its {b['sign']} sign is unchanged. These are authored model weights, not measured effect sizes or probabilities.")
        add(kind, [a], [b], claim, f"{b['from']} and {b['to']}", delta)
    return sorted(facts, key=lambda f: (-f["score"], f["id"]))


def select_facts(facts: list[dict], count: int = 4) -> list[dict]:
    """Prefer coverage and continuity over repeated descriptions of one edge."""
    remaining, selected, seen = list(facts), [], set()
    while remaining and len(selected) < count:
        best = max(remaining, key=lambda f: f["score"] - 18 * len(seen.intersection(f["nodes"])) / max(1, len(f["nodes"])))
        selected.append(best)
        remaining.remove(best)
        seen.update(best["nodes"])
    return selected
