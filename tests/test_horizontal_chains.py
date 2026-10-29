"""Check canonical chain facts, scenario changes and component event isolation."""
from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

from storytelling.chain_core import apply_chain_selection, build_chain, query_chains
from storytelling.chain_view import chain_preview_html
from storytelling.data import load_snapshots

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def snapshots():
    return load_snapshots()


@pytest.fixture(scope="module")
def chain(snapshots):
    snapshot = snapshots[2026][8]
    result = query_chains(snapshot, "Diagnosis Status", "Quality of Life")
    route = next(route for route in result["paths"] if len(route["node_ids"]) > 4)
    return build_chain(snapshot, route)


def event_for(chain, index=1, event_id="arrow-1"):
    return {"version": chain["version"], "scenario": chain["scenario"],
            "chain_id": chain["chain_id"], "query_id": chain["query_id"],
            "edge_id": chain["edge_ids"][index], "step_index": index, "event_id": event_id}


def test_real_routes_preserve_order_strengths_and_authored_text(snapshots, chain):
    result = query_chains(snapshots[2026][8], "Diagnosis Status", "Quality of Life")
    assert result["complete"] and result["returned_count"] == 8
    assert chain["query_id"] == result["query_id"]
    assert chain["node_ids"] == [node["id"] for node in chain["nodes"]]
    source = {edge["id"]: edge for edge in snapshots[2026][8]["edges"]}
    for index, step in enumerate(chain["steps"]):
        edge = source[step["edge_id"]]
        assert (step["source"], step["target"]) == tuple(chain["node_ids"][index:index + 2])
        assert (step["sign"], step["strength"], step["explanation"]) == (edge["sign"], edge["strength"], edge["explanation"])
        assert step["reason"] and len(step["examples"]) == 2
        assert step["snapshot_review"]["source"] == "validation_2026_age8/edge_validation.json"


def test_scenarios_filters_and_search_limits_are_explicit(snapshots):
    for year, age, count in ((1990, 8, 6), (2026, 32, 9)):
        result = query_chains(snapshots[year][age], "Diagnosis Status", "Quality of Life")
        assert result["returned_count"] == count
        for route in result["paths"]:
            assert build_chain(snapshots[year][age], route)["scenario"] == result["scenario"]
    snapshot = snapshots[2026][8]
    missing = query_chains(snapshot, "Absent endpoint", "Quality of Life")
    assert missing["state"] == "missing_endpoints" and missing["total_count"] is None
    assert missing["missing_endpoints"] == ["Absent endpoint"]
    filtered = query_chains(snapshot, "Diagnosis Status", "Quality of Life", minimum_strength=1)
    assert filtered["state"] == "no_route" and filtered["complete"]
    limited = query_chains(snapshot, "Diagnosis Status", "Quality of Life", limit=1)
    assert not limited["complete"] and limited["total_count"] is None and limited["returned_count"] == 1


def test_build_rejects_other_snapshots_reversed_edges_and_excluded_routes(snapshots):
    snapshot = snapshots[2026][8]
    route = query_chains(snapshot, "Diagnosis Status", "Quality of Life")["paths"][-1]
    with pytest.raises(ValueError):
        build_chain(snapshots[2026][32], route)
    reversed_route = deepcopy(route)
    reversed_route["node_ids"].reverse()
    with pytest.raises(ValueError):
        build_chain(snapshot, reversed_route)
    with pytest.raises(ValueError, match="filters"):
        build_chain(snapshot, route, minimum_strength=1)
    with pytest.raises(ValueError, match="filters"):
        build_chain(snapshot, route, max_hops=1)


@pytest.mark.parametrize("options", [
    {"minimum_strength": float("nan")}, {"minimum_strength": 1.1},
    {"max_hops": True}, {"max_hops": 8}, {"limit": float("nan")},
    {"limit": 0}, {"timeout_seconds": float("nan")}, {"timeout_seconds": 0},
])
def test_invalid_filters_and_unbounded_search_settings_are_rejected(snapshots, options):
    with pytest.raises(ValueError):
        query_chains(snapshots[2026][8], "Diagnosis Status", "Quality of Life", **options)


@pytest.mark.parametrize("changes", [
    {"scenario": {"year": 1990, "age": 8, "fingerprint": "old"}},
    {"query_id": "previous-filter"}, {"chain_id": "other-route"},
    {"edge_id": "reversed-edge"}, {"step_index": True}, {"step_index": -1},
    {"step_index": 100}, {"step_index": "1"}, {"event_id": None},
    {"version": "old-component"},
])
def test_mismatched_events_cannot_change_active_story(chain, changes):
    state = {}
    apply_chain_selection(None, chain, state)
    assert not apply_chain_selection({**event_for(chain), **changes}, chain, state)
    assert state["chain_step"] == 0


def test_valid_events_deduplicate_and_filter_changes_reset_selection(snapshots, chain):
    state = {}
    event = event_for(chain)
    assert apply_chain_selection(event, chain, state)
    assert state["chain_step"] == 1
    assert not apply_chain_selection(event, chain, state)
    altered = deepcopy(chain)
    altered["query_id"] = "new-filter-query"
    assert not apply_chain_selection(event, altered, state)
    assert state["chain_step"] == 0
    assert not apply_chain_selection(event, chain, state)
    assert state["chain_step"] == 0
    assert apply_chain_selection(event_for(chain, event_id="new-arrow-click"), chain, state)
    assert state["chain_step"] == 1
    assert not apply_chain_selection([event], chain, state)


def test_preview_encodes_source_text_without_active_markup(chain):
    changed = deepcopy(chain)
    malicious = "</script><img src=x onerror=alert(1)>"
    changed["nodes"][0]["label"] = malicious
    rendered = chain_preview_html(changed)
    assert malicious not in rendered
    payload = rendered.split("const INITIAL_CHAIN = ", 1)[1].split(";\nconst byId", 1)[0]
    assert json.loads(payload)["nodes"][0]["label"] == malicious


def test_prototype_selection_and_scenario_changes(snapshots):
    current_event = None
    rendered = {}

    def component(**kwargs):
        rendered.update(kwargs)
        return current_event

    with patch("storytelling.chain_view.chain_component", side_effect=component):
        app = AppTest.from_file(str(ROOT / "Chain_Prototype.py"), default_timeout=45).run()
        assert not app.exception
        assert len(rendered["chain"]["nodes"]) > 3
        current_event = event_for(rendered["chain"], index=1)
        app.run()
        assert not app.exception and app.session_state["chain_step"] == 1
        assert rendered["chain"]["steps"][1]["reason"] in [item.value for item in app.markdown]
        app.selectbox(key="chain_age").set_value(32).run()
        assert not app.exception and app.session_state["chain_step"] == 0
        assert rendered["chain"]["scenario"]["age"] == 32
        app.selectbox(key="chain_age").set_value(8).run()
        assert not app.exception and app.session_state["chain_step"] == 0
        app.slider(key="chain_strength").set_value(1.0).run()
        assert not app.exception
        assert any("No directed route" in item.value for item in app.info)
        app.slider(key="chain_strength").set_value(0.0).run()
        app.selectbox(key="chain_end").set_value("Diagnosis Status").run()
        assert not app.exception
        assert any("different starting" in item.value for item in app.info)
