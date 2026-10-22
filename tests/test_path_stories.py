import copy
import json
from pathlib import Path

import networkx as nx
import pytest
from streamlit.testing.v1 import AppTest

from storytelling.data import load_snapshots, stable_id
from storytelling.director import GenerationError, save_story
from storytelling.path_player import path_player_html
from storytelling.path_story import (
    ReasoningDraft, baseline_path_story, generate_path_story, load_path_story,
    validate_draft, validate_path_story,
)
from storytelling.paths import attach_path_review, discover_routes, path_snapshot, route_edges

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def snapshot():
    return load_snapshots()[2026][8]


@pytest.fixture(scope="module")
def route(snapshot):
    result = discover_routes(snapshot, "Diagnosis Status", "Quality of Life")
    return next(item for item in result["paths"]
                if "Medication Treatment" in item["node_ids"] and "Symptom Severity" in item["node_ids"])


def synthetic_snapshot(pairs):
    return {
        "fingerprint": "synthetic", "year": 2026, "age": 8,
        "nodes": [{"id": name} for name in sorted(set(sum(([source, target] for source, target in pairs), [])) | {"Z"})],
        "edges": [{"id": stable_id(source, target), "from": source, "to": target, "strength": .5}
                  for source, target in pairs],
        "node_groups": {},
    }


def test_real_query_lists_all_eight_routes_including_direct_edge(snapshot):
    result = discover_routes(snapshot, "Diagnosis Status", "Quality of Life")
    assert result["complete"] and result["total_count"] == 8
    assert result["paths"][0]["node_ids"] == ["Diagnosis Status", "Quality of Life"]
    graph = nx.DiGraph((edge["from"], edge["to"]) for edge in snapshot["edges"])
    expected = {tuple(nodes) for nodes in nx.all_simple_paths(graph, "Diagnosis Status", "Quality of Life", cutoff=5)}
    assert {tuple(item["node_ids"]) for item in result["paths"]} == expected


def test_discovery_respects_direction_cycles_cutoff_and_filters():
    snapshot = synthetic_snapshot([("A", "B"), ("B", "A"), ("B", "C"), ("A", "C")])
    assert len(discover_routes(snapshot, "A", "C", max_hops=2)["paths"]) == 2
    assert len(discover_routes(snapshot, "A", "C", max_hops=1)["paths"]) == 1
    assert not discover_routes(snapshot, "C", "A")["reachable"]
    assert not discover_routes(snapshot, "A", "C", minimum_strength=.6)["paths"]
    assert not discover_routes(snapshot, "A", "Z")["paths"]
    bounded = discover_routes(synthetic_snapshot([("A", "B"), ("B", "C")]), "A", "C", max_hops=1)
    assert bounded["reachable"] and not bounded["paths"] and bounded["complete"]


def test_limits_do_not_claim_exhaustive_results():
    snapshot = synthetic_snapshot([("A", "B"), ("B", "D"), ("A", "C"), ("C", "D")])
    limited = discover_routes(snapshot, "A", "D", limit=1)
    assert limited["returned_count"] == 1 and not limited["complete"]
    assert limited["total_count"] is None and limited["stop_reason"] == "path_limit"
    exact = discover_routes(snapshot, "A", "D", limit=2)
    assert exact["complete"] and exact["total_count"] == 2
    ticks = iter([0, 2])
    timed = discover_routes(snapshot, "A", "D", clock=lambda: next(ticks))
    assert not timed["complete"] and timed["stop_reason"] == "time_limit"


@pytest.mark.parametrize("start,end,hops", [("A", "A", 3), ("missing", "B", 3), ("A", "B", 0), ("A", "B", 8)])
def test_invalid_queries_are_explicit(start, end, hops):
    with pytest.raises(ValueError):
        discover_routes(synthetic_snapshot([("A", "B")]), start, end, max_hops=hops)


def test_isolated_graph_contains_exact_route_and_preserves_width(snapshot, route):
    isolated = path_snapshot(snapshot, route)
    assert {node["id"] for node in isolated["nodes"]} == set(route["node_ids"])
    assert [edge["id"] for edge in isolated["edges"]] == route["edge_ids"]
    assert len(isolated["nodes"]) == 6 and len(isolated["edges"]) == 5
    originals = {edge["id"]: edge for edge in snapshot["edges"]}
    assert all(edge["width"] == originals[edge["id"]]["width"] for edge in isolated["edges"])
    isolated["nodes"][0]["label"] = "Changed"
    assert all(node["label"] != "Changed" for node in snapshot["nodes"])


def test_stale_or_reversed_routes_are_rejected(snapshot, route):
    invalid = copy.deepcopy(route)
    invalid["node_ids"].reverse()
    with pytest.raises(ValueError):
        route_edges(snapshot, invalid)
    invalid = copy.deepcopy(route)
    invalid["path_id"] = "p_stale"
    with pytest.raises(ValueError):
        route_edges(snapshot, invalid)


def test_baseline_explains_each_relationship_with_two_concise_examples(snapshot, route):
    story = baseline_path_story(snapshot, route)
    assert story["version"] == "edge-examples-v5"
    assert "fox" not in json.dumps(story)
    assert len(story["chapters"]) == 5
    assert [chapter["edge_id"] for chapter in story["chapters"]] == route["edge_ids"]
    assert all(chapter["relationship"]["explanation"] for chapter in story["chapters"])
    assert all(len(chapter["examples"]) == 2 for chapter in story["chapters"])
    assert all(chapter["reason"] for chapter in story["chapters"])
    assert "fictional" in story["fiction_note"].lower()
    validate_path_story(story, snapshot, route)


def test_baseline_covers_every_supported_relationship(subtests):
    for year, ages in load_snapshots().items():
        for age, graph in ages.items():
            for edge in graph["edges"]:
                with subtests.test(year=year, age=age, source=edge["from"], target=edge["to"]):
                    selected = discover_routes(graph, edge["from"], edge["to"], max_hops=1)["paths"][0]
                    story = baseline_path_story(graph, selected)
                    assert len(story["chapters"][0]["examples"]) == 2
                    validate_path_story(story, graph, selected)


def test_consecutive_generic_chapters_do_not_repeat_sentences(snapshot):
    selected = discover_routes(snapshot, "School Resources", "School Support Plan")["paths"][0]
    story = baseline_path_story(snapshot, selected)
    assert len(story["chapters"]) == 4
    validate_path_story(story, snapshot, selected)
    generic = discover_routes(snapshot, "Neighborhood Quality", "Diagnosis Status")["paths"][0]
    validate_path_story(baseline_path_story(snapshot, generic), snapshot, generic)


def test_review_adapter_preserves_stable_ids_and_rejects_stale_report(tmp_path):
    snapshot = load_snapshots()[2010][8]
    route = discover_routes(snapshot, "Diagnosis Status", "Quality of Life")["paths"][0]
    original = route_edges(snapshot, route)
    annotated = attach_path_review(snapshot, original)
    assert annotated[0]["id"] == original[0]["id"]
    assert "snapshot_review" not in original[0]
    assert annotated[0]["snapshot_review"]["strength_assessed"] is False
    folder = tmp_path / "validation_2010_age8"
    folder.mkdir()
    report = json.loads((ROOT / "validation_2010_age8" / "edge_validation.json").read_text())
    (folder / "edge_validation.json").write_text(json.dumps(report))
    (tmp_path / snapshot["file_name"]).write_text("changed source")
    with pytest.raises(ValueError, match="stale"):
        attach_path_review(snapshot, original, root=tmp_path)


def test_saved_stories_reject_forged_relationships_and_other_routes(snapshot, route, tmp_path):
    story = baseline_path_story(snapshot, route)
    saved = save_story(story, tmp_path)
    assert load_path_story(saved, snapshot, route)["title"] == story["title"]
    invalid = copy.deepcopy(story)
    invalid["chapters"][0]["relationship"]["strength"] = .12345
    with pytest.raises(ValueError, match="altered"):
        validate_path_story(invalid, snapshot, route)
    other = discover_routes(snapshot, "Diagnosis Status", "Quality of Life")["paths"][0]
    with pytest.raises(ValueError, match="different route"):
        validate_path_story(story, snapshot, other)


def test_generation_uses_locked_route_and_repairs_wrong_order(snapshot, route):
    baseline = baseline_path_story(snapshot, route)
    draft = {"chapters": [{key: chapter[key] for key in ("edge_id", "examples")}
                           for chapter in baseline["chapters"] if chapter["status"] == "illustrative"]}

    class Client:
        def __init__(self):
            self.calls = 0

        def chat(self, messages, schema=None):
            self.calls += 1
            assert "fictional" in messages[0]["content"]
            assert schema["properties"]["chapters"]["minItems"] == 5
            result = copy.deepcopy(draft)
            if self.calls == 1:
                result["chapters"].reverse()
            return {"role": "assistant", "content": json.dumps(result)}

    client = Client()
    story = generate_path_story(snapshot, route, client=client)
    assert client.calls == 2 and story["origin"] == "local-qwen"
    assert [chapter["edge_id"] for chapter in story["chapters"]] == route["edge_ids"]


def test_generation_failure_does_not_change_baseline(snapshot, route):
    baseline = baseline_path_story(snapshot, route)

    class Client:
        def chat(self, messages, schema=None):
            return {"role": "assistant", "content": "{}"}

    with pytest.raises(GenerationError):
        generate_path_story(snapshot, route, client=Client())
    assert baseline["origin"] == "authored-reasoning"
    assert len(baseline["chapters"]) == 5


def test_rejects_unsupported_claims_but_allows_hypothetical_treatment_response(snapshot, route):
    story = baseline_path_story(snapshot, route)
    draft = ReasoningDraft(chapters=[{key: chapter[key] for key in ("edge_id", "reason", "examples", "status")}
                                    for chapter in story["chapters"]])
    for text in [" Treatment is 99 percent effective.", " The treatment guarantees a cure.",
                 " You should take medication.", " Take a dosage of 20 mg."]:
        changed = draft.model_copy(deep=True)
        changed.chapters[0].examples[0] += text
        with pytest.raises(ValueError):
            validate_draft(changed, snapshot, route)
    assert any("medication" in example and "fewer" in example
               for chapter in story["chapters"] for example in chapter["examples"])
    validate_draft(draft, snapshot, route)


def test_generation_checks_reject_changed_reasons_repetition_and_drift(snapshot, route):
    story = baseline_path_story(snapshot, route)
    draft = ReasoningDraft(chapters=[{key: chapter[key] for key in ("edge_id", "reason", "examples", "status")}
                                    for chapter in story["chapters"]])
    changed_reason = draft.model_copy(deep=True)
    changed_reason.chapters[0].reason = "An invented mechanism that reverses what the authored explanation says."
    with pytest.raises(ValueError, match="locked"):
        validate_draft(changed_reason, snapshot, route)
    repetitive = draft.model_copy(deep=True)
    repetitive.chapters[0].examples[1] = repetitive.chapters[0].examples[0]
    with pytest.raises(ValueError, match="distinct"):
        validate_draft(repetitive, snapshot, route)
    drifting = draft.model_copy(deep=True)
    drifting.chapters[2].examples[0] = "Mira draws a picture of a tree beside a river. She shows the drawing to her family after dinner."
    with pytest.raises(ValueError, match="mechanism"):
        validate_draft(drifting, snapshot, route)


def test_library_covers_all_signed_edges_and_distinguishes_causes(snapshot):
    from storytelling.reasoning_library import EXAMPLES

    keys = {f"{edge['from']}|{edge['to']}|{edge['sign']}"
            for ages in load_snapshots().values() for graph in ages.values() for edge in graph["edges"]}
    assert keys == set(EXAMPLES)
    medication = discover_routes(snapshot, "Medication Treatment", "Symptom Severity", max_hops=1)["paths"][0]
    sleep = discover_routes(snapshot, "Sleep Quality", "Symptom Severity", max_hops=1)["paths"][0]
    first = baseline_path_story(snapshot, medication)["chapters"][0]
    second = baseline_path_story(snapshot, sleep)["chapters"][0]
    assert first["reason"] != second["reason"] and first["examples"] != second["examples"]


def test_nutrition_edge_has_examples_without_review_gate_or_inherited_dna_claim(snapshot):
    selected = discover_routes(snapshot, "Early Life Nutrition", "Quality of Life")["paths"][0]
    story = baseline_path_story(snapshot, selected)
    assert story["chapters"][0]["status"] == "illustrative"
    assert len(story["chapters"][0]["examples"]) == 2
    assert "not a change in inherited DNA" in story["chapters"][0]["reason"]
    assert len(story["chapters"]) == selected["hop_count"]
    rendered = path_player_html(story, snapshot, selected)
    assert "Needs review" not in rendered
    assert "Examples withheld" not in rendered


def test_generation_includes_every_edge_and_keeps_their_reasons(snapshot):
    selected = discover_routes(snapshot, "Early Life Nutrition", "Quality of Life")["paths"][0]
    baseline = baseline_path_story(snapshot, selected)
    eligible = [chapter for chapter in baseline["chapters"] if chapter["status"] == "illustrative"]

    class Client:
        def chat(self, messages, schema=None):
            payload = json.loads(messages[1]["content"])
            assert len(payload["relationships"]) == len(eligible)
            assert baseline["chapters"][0]["edge_id"] in [edge["edge_id"] for edge in payload["relationships"]]
            assert len(eligible) == selected["hop_count"]
            return {"role": "assistant", "content": json.dumps({"chapters": [
                {key: chapter[key] for key in ("edge_id", "examples")} for chapter in eligible]})}

    generated = generate_path_story(snapshot, selected, client=Client())
    assert generated["chapters"][0] == baseline["chapters"][0]
    assert generated["origin"] == "local-qwen"


def test_single_nutrition_edge_can_generate_examples(snapshot):
    selected = discover_routes(snapshot, "Early Life Nutrition", "Genetic Risk", max_hops=1)["paths"][0]
    baseline = baseline_path_story(snapshot, selected)

    class Client:
        def chat(self, messages, schema=None):
            assert len(json.loads(messages[1]["content"])["relationships"]) == 1
            return {"role": "assistant", "content": json.dumps({"chapters": [
                {key: chapter[key] for key in ("edge_id", "examples")} for chapter in baseline["chapters"]]})}

    generated = generate_path_story(snapshot, selected, client=Client())
    assert len(generated["chapters"][0]["examples"]) == 2
    assert generated["origin"] == "local-qwen"


def test_adult_examples_use_adult_tasks():
    graph = load_snapshots()[2026][32]
    selected = discover_routes(graph, "Symptom Severity", "Functional Impairment", max_hops=1)["paths"][0]
    story = baseline_path_story(graph, selected)
    assert "work task" in story["chapters"][0]["examples"][0]
    assert "classroom assignment" not in json.dumps(story)


def test_negated_guarantee_is_not_mistaken_for_a_promise_and_names_stay_consistent(snapshot):
    selected = discover_routes(snapshot, "Genetic Risk", "ADHD", max_hops=1)["paths"][0]
    story = baseline_path_story(snapshot, selected)
    story["chapters"][0]["examples"][0] = "Mira inherits a combination of genetic variants associated with greater ADHD susceptibility. This increases a possible vulnerability but does not guarantee that ADHD will develop."
    validate_path_story(story, snapshot, selected)
    mixed = copy.deepcopy(story)
    mixed["chapters"][0]["examples"][0] = "Noah's mother has persistent attention difficulties, and Mira inherits a combination of genetic variants that may increase ADHD susceptibility."
    with pytest.raises(ValueError, match="protagonist"):
        validate_path_story(mixed, snapshot, selected)


def test_export_embeds_only_selected_graph_and_escapes_script_text(snapshot, route):
    story = baseline_path_story(snapshot, route)
    story["title"] = "</script><script>alert('test')</script>"
    exported = path_player_html(story, snapshot, route)
    payload = json.loads(exported.split("const DATA = ", 1)[1].split(";\nconst story", 1)[0])
    assert len(payload["graph"]["nodes"]) == 6 and len(payload["graph"]["edges"]) == 5
    assert payload["story"]["title"] == story["title"]
    assert story["title"] not in exported
    assert "/* VIS_LIBRARY */" not in exported
    assert "window.addEventListener('pagehide', pause)" in exported


def test_cli_export_handles_path_story(snapshot, route, tmp_path):
    from export_saved_story import export_saved_story

    saved = save_story(baseline_path_story(snapshot, route), tmp_path)
    output = export_saved_story(saved, tmp_path / "playable.html")
    assert output.is_file()
    assert "Only the selected path is shown" in output.read_text()


def test_legacy_story_can_still_export_but_cannot_be_reused_as_new_style(snapshot, tmp_path):
    from export_saved_story import export_saved_story

    for filename in ["75d0e79eac337061d3389189.json", "1afc9b88b3a0f84138cb2dd1.json"]:
        saved = ROOT / "stories" / filename
        legacy = json.loads(saved.read_text())
        with pytest.raises(ValueError, match="format"):
            load_path_story(saved, snapshot, legacy["route"])
        output = export_saved_story(saved, tmp_path / (filename + ".html"))
        assert output.is_file() and legacy["version"] in output.read_text()


def test_changed_library_sources_and_excess_example_length_are_rejected(snapshot, route):
    story = baseline_path_story(snapshot, route)
    stale = copy.deepcopy(story)
    stale["library_hash"] = "old-library"
    with pytest.raises(ValueError, match="outdated"):
        validate_path_story(stale, snapshot, route)
    forged = copy.deepcopy(story)
    forged["chapters"][2]["mechanism_sources"] = []
    with pytest.raises(ValueError, match="sources"):
        validate_path_story(forged, snapshot, route)
    long_example = copy.deepcopy(story)
    long_example["chapters"][0]["examples"][0] = "A very long example that does not stay concise " * 10
    with pytest.raises(ValueError, match="concise"):
        validate_path_story(long_example, snapshot, route)


def test_dashboard_path_selection_switching_and_no_path_state():
    app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=45).run()
    app.radio[0].set_value("Path story").run()
    assert not app.exception
    assert not any(item.label == "Select a complete route" for item in app.selectbox)
    next(item for item in app.selectbox if item.label == "Start concept").set_value("Diagnosis Status").run()
    next(item for item in app.selectbox if item.label == "End concept").set_value("Quality of Life").run()
    next(item for item in app.button if item.label == "Find directed routes").click().run()
    assert not app.exception
    selection = next(item for item in app.selectbox if item.label == "Select a complete route")
    assert len(selection.options) == 8
    assert any("8 routes found" in str(item.value) for item in app.caption)
    selection.select_index(0).run()
    assert not app.exception
    next(item for item in app.selectbox if item.label == "End concept").set_value("Diagnosis Status").run()
    assert not app.exception
    assert any("different starting" in str(item.value) for item in app.info)
    assert not any(item.label == "Select a complete route" for item in app.selectbox)
