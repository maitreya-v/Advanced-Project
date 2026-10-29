"""Persistence checks use actual graph routes and fresh directories."""
from copy import deepcopy
import json
from html import unescape
import re

import pytest

from storytelling.chain_core import build_chain, query_chains
from storytelling.chain_store import (
    create_saved_chains, list_saved_chains, load_saved_chains,
    save_chains, saved_chains_json, validate_saved_chains,
)
from storytelling.data import load_snapshots
from storytelling.chain_export import saved_chains_html


@pytest.fixture(scope="module")
def snapshots():
    return load_snapshots()


def make_chain(snapshots, year=2026, age=8):
    snapshot = snapshots[year][age]
    route = query_chains(snapshot, "Diagnosis Status", "Quality of Life")["paths"][-1]
    return build_chain(snapshot, route)


def test_save_list_and_reopen_preserve_routes_text_and_filters(tmp_path, snapshots):
    chain = make_chain(snapshots)
    original = deepcopy(chain)
    record = create_saved_chains([chain], "Medication route", snapshots=snapshots)
    path = save_chains(record, tmp_path, snapshots=snapshots)
    chain["steps"][0]["reason"] = "Changed live story"
    reopened = load_saved_chains(path, snapshots=load_snapshots())
    assert reopened["chains"] == [original]
    assert list_saved_chains(tmp_path)[0]["name"] == "Medication route"
    assert json.loads(saved_chains_json(reopened, snapshots=snapshots)) == reopened
    before = path.read_bytes()
    repeat = create_saved_chains([original], "Medication route", snapshots=snapshots)
    assert repeat["save_id"] == record["save_id"]
    save_chains(repeat, tmp_path, snapshots=snapshots)
    assert path.read_bytes() == before
    assert list(tmp_path.glob("*.tmp")) == []


def test_future_comparison_saves_keep_two_independent_scenarios(tmp_path, snapshots):
    chains = [make_chain(snapshots, 1990, 8), make_chain(snapshots, 2026, 32)]
    record = create_saved_chains(chains, "Two scenarios", snapshots=snapshots)
    path = save_chains(record, tmp_path, snapshots=snapshots)
    loaded = load_saved_chains(path, snapshots=snapshots)
    assert [(c["scenario"]["year"], c["scenario"]["age"]) for c in loaded["chains"]] == [(1990, 8), (2026, 32)]
    assert [c["edge_ids"] for c in loaded["chains"]] == [c["edge_ids"] for c in chains]


def test_rehashed_forged_facts_and_changed_source_are_rejected(tmp_path, snapshots):
    chain = make_chain(snapshots)
    record = create_saved_chains([chain], "Original", snapshots=snapshots)
    altered = deepcopy(record)
    altered["chains"][0]["steps"][0]["strength"] = 0.12345
    with pytest.raises(ValueError, match="contents"):
        validate_saved_chains(altered, snapshots)
    with pytest.raises(ValueError, match="facts"):
        create_saved_chains(altered["chains"], "Rehashed forgery", snapshots=snapshots)
    changed_sources = deepcopy(snapshots)
    changed_sources[2026][8]["fingerprint"] = "new-source-fingerprint"
    path = save_chains(record, tmp_path, snapshots=snapshots)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="changed source"):
        load_saved_chains(path, snapshots=changed_sources)
    assert path.read_bytes() == before


def test_bad_records_remain_visible_without_hiding_valid_saves(tmp_path, snapshots):
    record = create_saved_chains([make_chain(snapshots)], "Good record", snapshots=snapshots)
    save_chains(record, tmp_path, snapshots=snapshots)
    corrupt = tmp_path / ("f" * 24 + ".json")
    corrupt.write_text("broken JSON")
    (tmp_path / "unrelated.json").write_text("{}")
    entries = list_saved_chains(tmp_path)
    assert len(entries) == 2 and sum(entry["error"] is not None for entry in entries) == 1
    with pytest.raises(ValueError, match="readable"):
        load_saved_chains(corrupt, snapshots=snapshots)
    with pytest.raises(ValueError):
        create_saved_chains([make_chain(snapshots)], " ", snapshots=snapshots)
    with pytest.raises(ValueError):
        create_saved_chains([], "Empty", snapshots=snapshots)


def test_write_failure_leaves_no_partial_record(tmp_path, snapshots, monkeypatch):
    record = create_saved_chains([make_chain(snapshots)], "Atomic save", snapshots=snapshots)

    def fail_replace(*args):
        raise OSError("No space left")

    monkeypatch.setattr("storytelling.chain_store.os.replace", fail_replace)
    with pytest.raises(OSError, match="space"):
        save_chains(record, tmp_path, snapshots=snapshots)
    assert list(tmp_path.iterdir()) == []


def test_offline_export_contains_each_exact_chain_and_escapes_labels(snapshots):
    chains = [make_chain(snapshots, 1990, 8), make_chain(snapshots, 2026, 32)]
    record = create_saved_chains(chains, '<img src=x onerror="alert(1)">', snapshots=snapshots)
    exported = saved_chains_html(record, snapshots=snapshots)
    assert record["name"] not in exported
    sources = re.findall(r'srcdoc="([^"]+)"', exported)
    assert len(sources) == 2
    for expected, source in zip(chains, sources):
        document = unescape(source)
        payload = document.split("const INITIAL_CHAIN = ", 1)[1].split(";\nconst byId", 1)[0]
        assert json.loads(payload) == expected
        assert 'id="reading"' in document
        assert "https://" not in document and "<script src=" not in document
