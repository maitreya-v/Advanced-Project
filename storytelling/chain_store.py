"""Versioned, immutable saved chains with source-checked reloads."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from .chain_core import CHAIN_VERSION, build_chain
from .data import ROOT, load_snapshots

SAVED_VERSION = "saved-chains-v1"
DEFAULT_DIRECTORY = ROOT / "saved_chains"


def _content(record: dict) -> dict:
    return {key: record[key] for key in ("version", "name", "chains")}


def _save_id(content: dict) -> str:
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:24]


def _check_envelope(record: dict) -> None:
    try:
        if not isinstance(record, dict) or set(record) != {"version", "save_id", "name", "created_at", "chains"}:
            raise ValueError("Unrecognized saved-chain record.")
        if record["version"] != SAVED_VERSION:
            raise ValueError("Unsupported saved-chain version.")
        if not isinstance(record["name"], str) or not 1 <= len(record["name"].strip()) <= 160:
            raise ValueError("Give the saved chain a name of one to 160 characters.")
        if not isinstance(record["chains"], list) or not 1 <= len(record["chains"]) <= 2:
            raise ValueError("Save one chain, or two separate chains for a comparison.")
        if not isinstance(record["save_id"], str) or not re.fullmatch(r"[a-f0-9]{24}", record["save_id"]):
            raise ValueError("Invalid saved-chain ID.")
        created = datetime.fromisoformat(record["created_at"])
        if created.tzinfo is None:
            raise ValueError("The saved timestamp needs a timezone.")
        if record["save_id"] != _save_id(_content(record)):
            raise ValueError("The saved chain's contents have changed.")
    except (KeyError, TypeError, OverflowError) as error:
        raise ValueError("Incomplete or invalid saved-chain record.") from error


def validate_saved_chains(record: dict, snapshots: dict | None = None) -> None:
    """Rebuild each route independently; never trust a checksum as source validation."""
    _check_envelope(record)
    snapshots = load_snapshots() if snapshots is None else snapshots
    for chain in record["chains"]:
        try:
            if chain["version"] != CHAIN_VERSION:
                raise ValueError("Unsupported chain format.")
            scope = chain["scenario"]
            snapshot = snapshots[scope["year"]][scope["age"]]
            if scope != {key: snapshot[key] for key in ("year", "age", "fingerprint")}:
                raise ValueError("The saved chain belongs to changed source data. The saved file is preserved.")
            route = {"path_id": chain["chain_id"], "node_ids": chain["node_ids"], "edge_ids": chain["edge_ids"]}
            expected = build_chain(snapshot, route, max_hops=chain["query"]["max_hops"],
                                   minimum_strength=chain["query"]["minimum_strength"])
            if chain != expected:
                raise ValueError("Saved chain facts or story text differ from the current source. The saved file is preserved.")
        except (KeyError, TypeError, IndexError) as error:
            raise ValueError("This saved chain has an unknown scenario or incomplete route.") from error


def create_saved_chains(chains: list[dict], name: str, *, snapshots: dict | None = None) -> dict:
    if not isinstance(name, str):
        raise ValueError("Give the saved chain a name.")
    record = {"version": SAVED_VERSION, "name": name.strip(), "chains": deepcopy(chains),
              "created_at": datetime.now(timezone.utc).isoformat()}
    record["save_id"] = _save_id(_content(record))
    validate_saved_chains(record, snapshots)
    return record


def saved_chains_json(record: dict, *, snapshots: dict | None = None) -> str:
    validate_saved_chains(record, snapshots)
    return json.dumps(record, indent=2, ensure_ascii=False) + "\n"


def load_saved_chains(path: Path, *, snapshots: dict | None = None) -> dict:
    try:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("This file is not a readable saved-chain JSON record.") from error
    validate_saved_chains(record, snapshots)
    return record


def save_chains(record: dict, directory: Path = DEFAULT_DIRECTORY, *, snapshots: dict | None = None) -> Path:
    """Write atomically. Identical repeat saves preserve the original file."""
    serialized = saved_chains_json(record, snapshots=snapshots)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / (record["save_id"] + ".json")
    if target.exists():
        existing = load_saved_chains(target, snapshots=snapshots)
        if _content(existing) != _content(record):
            raise ValueError("A different record already uses this saved-chain ID.")
        return target
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory,
                                         prefix=".chain-", suffix=".tmp", delete=False) as output:
            temporary = Path(output.name)
            output.write(serialized)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return target


def list_saved_chains(directory: Path = DEFAULT_DIRECTORY) -> list[dict]:
    """List metadata cheaply; malformed files remain visible as unavailable entries."""
    directory = Path(directory)
    if not directory.exists():
        return []
    entries = []
    for path in directory.glob("*.json"):
        if not re.fullmatch(r"[a-f0-9]{24}", path.stem):
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            _check_envelope(record)
            if record["save_id"] != path.stem:
                raise ValueError("The saved ID does not match its filename.")
            scopes = [chain["scenario"] for chain in record["chains"]]
            entries.append({"save_id": path.stem, "name": record["name"],
                            "created_at": record["created_at"], "scenarios": scopes, "error": None})
        except (OSError, ValueError, KeyError, TypeError) as error:
            entries.append({"save_id": path.stem, "name": "Unavailable saved chain",
                            "created_at": "", "scenarios": [], "error": str(error)})
    return sorted(entries, key=lambda entry: (entry["created_at"], entry["save_id"]), reverse=True)
