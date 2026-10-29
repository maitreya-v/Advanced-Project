import json
from pathlib import Path
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

from storytelling.data import load_snapshots
from storytelling.graph_selector import apply_node_selection, full_graph_html
from storytelling.path_story import baseline_path_story

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def snapshot():
    return load_snapshots()[2026][8]


def test_selector_embeds_the_complete_graph_and_escapes_script_text(snapshot):
    graph = dict(snapshot)
    graph["nodes"] = [dict(node) for node in snapshot["nodes"]]
    graph["nodes"][0]["label"] = "</script><script>alert('bad')</script>"
    rendered = full_graph_html(graph)
    payload = json.loads(rendered.split("const GRAPH = ", 1)[1].split(";\nconst byId", 1)[0])
    assert len(payload["nodes"]) == 48 and len(payload["edges"]) == 68
    assert payload["nodes"][0]["label"] == graph["nodes"][0]["label"]
    assert graph["nodes"][0]["label"] not in rendered
    assert "/* VIS_LIBRARY */" not in rendered


def test_validated_clicks_set_and_clear_endpoints_without_replaying_events(snapshot):
    state = {"start": None, "end": None}
    selection = {"fingerprint": snapshot["fingerprint"], "role": "start", "node_id": "Stigma", "event_id": "click-1"}
    assert apply_node_selection(selection, snapshot, state, "start", "end")
    assert state["start"] == "Stigma" and state["end"] is None
    assert not apply_node_selection(selection, snapshot, state, "start", "end")
    selection.update(role="end", node_id="Quality of Life", event_id="click-2")
    assert apply_node_selection(selection, snapshot, state, "start", "end")
    assert state["end"] == "Quality of Life"
    selection.update(role="clear", event_id="click-3")
    assert apply_node_selection(selection, snapshot, state, "start", "end")
    assert state["start"] is None and state["end"] is None


@pytest.mark.parametrize("changes", [
    {"fingerprint": "another-scenario"}, {"node_id": "Unknown"},
    {"node_id": {"forged": True}}, {"role": "execute"}, {"event_id": None},
])
def test_stale_and_invalid_clicks_cannot_change_selection(snapshot, changes):
    state = {"start": None, "end": None}
    event = {"fingerprint": snapshot["fingerprint"], "role": "start", "node_id": "Stigma", "event_id": "event-1", **changes}
    assert not apply_node_selection(event, snapshot, state, "start", "end")
    assert state == {"start": None, "end": None}


def test_graph_clicks_drive_route_discovery_and_on_demand_generation(snapshot):
    selection = None

    def component(**kwargs):
        return selection

    with patch("storytelling.path_ui.graph_selector_component", side_effect=component), \
         patch("storytelling.path_ui.generate_path_story", side_effect=baseline_path_story) as generate:
        app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=45).run()
        app.radio[0].set_value("Path story").run()
        assert not app.exception
        assert next(item for item in app.button if item.label == "Find directed routes").disabled
        selection = {"fingerprint": snapshot["fingerprint"], "role": "start", "node_id": "Stigma", "event_id": "start-click"}
        app.run()
        assert not app.exception
        assert next(item for item in app.selectbox if item.label == "Start concept").value == "Stigma"
        selection = {"fingerprint": snapshot["fingerprint"], "role": "end", "node_id": "Quality of Life", "event_id": "end-click"}
        app.run()
        assert not app.exception
        next(item for item in app.button if item.label == "Find directed routes").click().run()
        assert not app.exception
        assert app.session_state["path_workflow_tab"] == "2. Routes and stories"
        assert any("9 routes found" in str(item.value) for item in app.caption)
        generate.assert_not_called()
        next(item for item in app.button if item.label == "Generate story for this path").click().run()
        assert not app.exception
        generate.assert_called_once()
        selected_route = generate.call_args.args[1]
        assert selected_route["node_ids"][0] == "Stigma"
        assert selected_route["node_ids"][-1] == "Quality of Life"
        assert len(selected_route["edge_ids"]) == len(selected_route["node_ids"]) - 1
        next(item for item in app.selectbox if item.label == "End concept").set_value("Diagnosis Status").run()
        assert not app.exception
        assert not any(item.label == "Select a complete route" for item in app.selectbox)


def test_direct_link_opens_full_graph_with_requested_scenario():
    app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=45)
    app.query_params.update(workspace="path", year="2010", age="32")
    app.run()
    assert not app.exception
    assert app.radio[0].value == "Path story"
    assert next(item for item in app.selectbox if item.label == "Story year").value == 2010
    assert next(item for item in app.selectbox if item.label == "Story age").value == 32
    assert next(item for item in app.selectbox if item.label == "Start concept").value is None
    assert not any(item.label == "Select a complete route" for item in app.selectbox)
