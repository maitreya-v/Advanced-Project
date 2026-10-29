"""New review metadata must not weaken validation of archived source facts."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from storytelling.data import load_snapshots
from storytelling.path_story import validate_legacy_path_story
from storytelling.paths import attach_path_review, route_edges

ROOT = Path(__file__).resolve().parents[1]


def rekey(story):
    payload = [story["version"], story["route"]["path_id"], story.get("question", "").strip(),
               [chapter["relationship"] for chapter in story["chapters"]]]
    if story["version"] == "edge-reasoning-v4":
        payload.insert(1, story["library_hash"])
    story["key"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:24]


@pytest.fixture(params=["75d0e79eac337061d3389189.json", "1afc9b88b3a0f84138cb2dd1.json"])
def archived(request):
    story = json.loads((ROOT / "stories" / request.param).read_text(encoding="utf-8"))
    return story, load_snapshots()[2026][8]


@pytest.mark.parametrize("field,value", [
    ("strength", .12345), ("sign", "+forged"), ("explanation", "Invented source mechanism"),
    ("from", "Wrong direction"),
])
def test_rehashing_legacy_records_cannot_hide_altered_graph_facts(archived, field, value):
    story, snapshot = archived
    validate_legacy_path_story(story, snapshot, story["route"])
    forged = deepcopy(story)
    forged["chapters"][0]["relationship"][field] = value
    rekey(forged)
    with pytest.raises(ValueError, match="altered"):
        validate_legacy_path_story(forged, snapshot, forged["route"])


def test_reviews_that_were_actually_saved_remain_strict(archived):
    story, snapshot = archived
    edges = attach_path_review(snapshot, route_edges(snapshot, story["route"]))
    for chapter, edge in zip(story["chapters"], edges):
        chapter["relationship"] = edge
    rekey(story)
    validate_legacy_path_story(story, snapshot, story["route"])
    story["chapters"][0]["relationship"]["snapshot_review"]["status"] = "forged review"
    rekey(story)
    with pytest.raises(ValueError, match="altered"):
        validate_legacy_path_story(story, snapshot, story["route"])


def test_legacy_key_and_scenario_are_still_checked(archived):
    story, snapshot = archived
    story["key"] = "wrong-cache-key"
    with pytest.raises(ValueError, match="evidence or settings"):
        validate_legacy_path_story(story, snapshot, story["route"])
    story["snapshot"]["fingerprint"] = "another-source"
    with pytest.raises(ValueError, match="different snapshot"):
        validate_legacy_path_story(story, snapshot, story["route"])
