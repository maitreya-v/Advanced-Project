import copy
import json
from pathlib import Path

import pytest

from storytelling.analysis import compare, fact_catalog, story_key
from storytelling.data import ROOT, literals, load_evidence_registry, load_snapshots, stable_id
from storytelling.director import (
    GenerationError, LocalOllama, SceneDraft, StoryDraft, baseline_story,
    generate_story, load_story, save_story, validate_draft,
)
from storytelling.player import player_html
from storytelling.evaluation import (
    CONDITIONS, assigned_condition, case_snapshots, evaluation_cases,
    quiz_for_case, records_csv, score_answers,
)


@pytest.fixture(scope="module")
def snapshots():
    return load_snapshots()


def test_snapshot_loading_never_executes_source(tmp_path):
    path = tmp_path / "sample.py"
    path.write_text("raise RuntimeError('must not execute')\nnode_groups={'A':'core'}\nedges=[]")
    assert literals(path)["node_groups"] == {"A": "core"}


def test_all_snapshots_have_valid_stable_records(snapshots):
    assert sum(len(s) for s in snapshots.values()) == 12
    assert len(snapshots[2010][8]["edges"]) == 58
    assert len(snapshots[2026][8]["edges"]) == 68
    for ages in snapshots.values():
        for snapshot in ages.values():
            ids = {n["id"] for n in snapshot["nodes"]}
            for e in snapshot["edges"]:
                assert {e["from"], e["to"]} <= ids
                assert e["id"] == stable_id(e["from"], e["to"])


def test_evidence_registry_is_attached_without_changing_story_fingerprints(snapshots):
    registry = load_evidence_registry()
    assert registry
    telehealth = stable_id("Telehealth Treatment", "Treatment Access")
    edge = next(e for e in snapshots[2026][8]["edges"] if e["id"] == telehealth)
    assert edge["citations"][0]["url"] == "https://pubmed.ncbi.nlm.nih.gov/25791143/"
    assert "not edge-validated" in edge["evidence_quality"]
    unreviewed = next(e for e in snapshots[2026][8]["edges"] if e["id"] not in registry)
    assert unreviewed["evidence_quality"] == "Not yet reviewed"
    assert not unreviewed["citations"]
    assert snapshots[2010][8]["fingerprint"] == "254f46fd7f4a165bf5710fc994c7caa10cbe6ce291a69cb0d4800458a6ba89a8"


def test_comparison_counts_and_restructured_path(snapshots):
    before, after = snapshots[2010][8], snapshots[2026][8]
    changes = compare(before, after)
    assert (len(changes["added"]), len(changes["removed"]), len(changes["changed"]), len(changes["unchanged"])) == (14, 4, 47, 7)
    facts = fact_catalog(before, after, "Treatment and access")
    fact = next(f for f in facts if f["kind"] == "restructured" and f["before_edges"][0]["to"] == "Medication Treatment")
    assert [(e["from"], e["to"]) for e in fact["after_edges"]] == [
        ("Diagnosis Status", "Treatment Access"), ("Treatment Access", "Medication Treatment")]
    assert "not proof" in fact["claim"]


def test_negative_magnitude_decrease_is_weakened_and_sign_flip_is_separate(snapshots):
    a, b = snapshots[2010][8], copy.deepcopy(snapshots[2026][8])
    stigma = stable_id("Stigma", "Diagnosis Status")
    f = next(f for f in fact_catalog(a, b, "All changes") if f["after_edges"] and f["after_edges"][0]["id"] == stigma)
    assert f["kind"] == "weakened"
    next(e for e in b["edges"] if e["id"] == stigma)["sign"] = "+"
    f = next(f for f in fact_catalog(a, b, "All changes") if f["after_edges"] and f["after_edges"][0]["id"] == stigma)
    assert f["kind"] == "sign_changed"


def test_axes_are_not_mixed(snapshots):
    with pytest.raises(ValueError, match="Hold age or year"):
        compare(snapshots[2010][8], snapshots[2026][32])
    with pytest.raises(ValueError, match="different snapshots"):
        compare(snapshots[2010][8], snapshots[2010][8])
    assert compare(snapshots[2026][8], snapshots[2026][32])["mode"] == "age"


def test_saved_story_is_rechecked_against_source(snapshots, tmp_path):
    a, b = snapshots[2010][8], snapshots[2026][8]
    story = baseline_story(a, b, "Treatment and access")
    path = save_story(story, tmp_path)
    assert load_story(path, a, b, "Treatment and access")["scenes"] == story["scenes"]
    different = copy.deepcopy(b)
    different["fingerprint"] = "changed"
    with pytest.raises(ValueError, match="different snapshots"):
        load_story(path, a, different, "Treatment and access")
    data = json.loads(path.read_text())
    data["scenes"][0]["fact"]["claim"] = "Injected fabricated evidence"
    path.write_text(json.dumps(data))
    assert "Injected" not in load_story(path, a, b, "Treatment and access")["scenes"][0]["fact"]["claim"]


def test_grounding_rejects_invented_ids_numbers_and_probability(snapshots):
    a, b = snapshots[2010][8], snapshots[2026][8]
    facts = fact_catalog(a, b, "All changes")
    for fact_id, narration in [("fake", "The model changed."), (facts[0]["id"], "The model has strength 0.123456."),
                               (facts[0]["id"], "The model proves a benefit."), (facts[0]["id"], "The model shows a more direct pathway."),
                               (facts[0]["id"], "The model shows a strong relationship.")]:
        draft = StoryDraft(title="Test", scenes=[SceneDraft(fact_id=fact_id, title="Test", narration=narration)])
        with pytest.raises(ValueError):
            validate_draft(draft, facts, a, b)


def test_grounding_rejects_scene_fact_mismatches(snapshots):
    a, b = snapshots[2010][8], snapshots[2026][8]
    facts = fact_catalog(a, b, "Treatment and access")
    medication = next(
        f for f in facts
        if f["kind"] == "restructured" and "Medication Treatment" in f["nodes"]
    )
    mismatched = StoryDraft(title="Test", scenes=[SceneDraft(
        fact_id=medication["id"],
        title="Treatment Access and School Accommodations",
        narration=(
            "The graph links Diagnosis Status to Treatment Access and then to "
            "School Accommodations. This structural comparison does not establish causal equivalence."
        ),
    )])
    with pytest.raises(ValueError, match="outside its selected fact"):
        validate_draft(mismatched, facts, a, b)


def test_grounding_requires_restructured_path_caveat(snapshots):
    a, b = snapshots[2010][8], snapshots[2026][8]
    facts = fact_catalog(a, b, "Treatment and access")
    medication = next(
        f for f in facts
        if f["kind"] == "restructured" and "Medication Treatment" in f["nodes"]
    )
    unsupported_equivalence = StoryDraft(title="Test", scenes=[SceneDraft(
        fact_id=medication["id"],
        title="Medication Treatment through Treatment Access",
        narration=(
            "The later graph replaces the Diagnosis Status to Medication Treatment edge "
            "with a path through Treatment Access."
        ),
    )])
    with pytest.raises(ValueError, match="causal equivalence"):
        validate_draft(unsupported_equivalence, facts, a, b)


def test_age_comparison_rejects_timeline_language(snapshots):
    a, b = snapshots[2026][8], snapshots[2026][32]
    facts = fact_catalog(a, b, "All changes")
    fact = next(f for f in facts if f["kind"] in {"added", "removed"})
    narration = (
        f"The earlier graph contains {fact['nodes'][0]} and {fact['nodes'][1]}, "
        "while the later snapshot differs. This describes the model."
    )
    draft = StoryDraft(title="Test", scenes=[SceneDraft(
        fact_id=fact["id"], title=fact["title"], narration=narration
    )])
    with pytest.raises(ValueError, match="separate age scenarios"):
        validate_draft(draft, facts, a, b)


def test_story_keeps_most_scenes_on_the_selected_focus(snapshots):
    a, b = snapshots[2026][8], snapshots[2026][32]
    facts = fact_catalog(a, b, "School and family")
    irrelevant = [f for f in facts if f["score_parts"]["relevance"] == 0][:4]
    assert len(irrelevant) == 4
    draft = StoryDraft(title="Off-topic story", scenes=[
        SceneDraft(fact_id=f["id"], title=f["title"], narration=f["claim"])
        for f in irrelevant
    ])
    with pytest.raises(ValueError, match="selected focus"):
        validate_draft(draft, facts, a, b, "School and family")


def test_rule_based_age_story_names_both_age_scenarios(snapshots):
    story = baseline_story(snapshots[2026][8], snapshots[2026][32], "All changes")
    for scene in story["scenes"]:
        assert "age 8 scenario" in scene["narration"].lower()
        assert "age 32 scenario" in scene["narration"].lower()


def test_story_has_deterministic_opening_and_closing(snapshots):
    story = baseline_story(snapshots[2010][8], snapshots[2026][8], "Treatment and access")
    assert story["opening"]["title"] == "Treatment and access: 2010 to 2026"
    assert "not proof of real-world historical change" in story["opening"]["narration"]
    assert story["closing"]["title"] == "What this story establishes—and what it does not"
    assert "do not validate" in story["closing"]["narration"]


def test_24_case_evaluation_suite_and_scoring(snapshots):
    cases = evaluation_cases()
    assert len(cases) == 24
    assert len({case["id"] for case in cases}) == 24
    for case in cases:
        a, b = case_snapshots(case, snapshots)
        assert compare(a, b)["mode"] == case["mode"]
    questions = quiz_for_case(cases[0], snapshots)
    answers = {question["id"]: question["correct"] for question in questions}
    assert score_answers(questions, answers) == 4
    answers[questions[0]["id"]] = next(option for option in questions[0]["options"] if option != questions[0]["correct"])
    assert score_answers(questions, answers) == 3
    assert "case_id" in records_csv([{"case_id": "case-01", "score": 4}])
    assigned = {assigned_condition(f"P{i:03d}", "case-01") for i in range(100)}
    assert assigned == set(CONDITIONS)


def test_local_only_model_connection():
    for host in ["https://api.example.com", "http://127.0.0.1.evil.test", "http://user:pass@localhost", "http://localhost/path"]:
        with pytest.raises(GenerationError):
            LocalOllama(base_url=host)
    with pytest.raises(GenerationError):
        LocalOllama(model="qwen3:cloud")


def test_generation_runs_tools_and_materializes_only_known_facts(snapshots):
    a, b = snapshots[2010][8], snapshots[2026][8]
    baseline = baseline_story(a, b, "Treatment and access")
    draft = {"title": "A graph story", "scenes": [{k: s[k] for k in ("fact_id", "title", "narration")} for s in baseline["scenes"]]}
    class FakeClient:
        def __init__(self):
            self.calls = 0
        def chat(self, messages, tools=None, schema=None):
            self.calls += 1
            if self.calls == 1:
                return {"role": "assistant", "tool_calls": [{"function": {"name": "get_ranked_changes", "arguments": {}}}]}
            if tools:
                return {"role": "assistant", "content": "Ready to write."}
            assert schema["$defs"]["SceneDraft"]["properties"]["fact_id"]["enum"]
            return {"role": "assistant", "content": json.dumps(draft)}
    result = generate_story(a, b, "Treatment and access", client=FakeClient())
    assert result["origin"] == "local-qwen"
    assert result["trace"][0]["tool"] == "get_ranked_changes"
    assert len(result["scenes"]) == 4


def test_standalone_html_escapes_payload(snapshots):
    a, b = snapshots[2010][8], snapshots[2026][8]
    story = baseline_story(a, b, "All changes")
    story["title"] = "</script><script>alert('bad')</script>"
    html = player_html(story, a, b)
    assert story["title"] not in html
    assert "\\u003c/script>" in html
    assert "/* STORY_DATA */" not in html
    assert 'src="https://' not in html
    assert "Inspect supporting relationships and citations" in html
    assert "What this story establishes" in html


def test_question_and_theme_invalidate_cache(snapshots):
    a, b = snapshots[2010][8], snapshots[2026][8]
    assert len({story_key(a, b, "All changes"), story_key(a, b, "All changes", "school"), story_key(a, b, "School and family")}) == 3
