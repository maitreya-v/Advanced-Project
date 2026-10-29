"""Export an isolated, ordered route with no external player dependencies."""
import json

from .data import ROOT
from .paths import path_snapshot


def path_player_html(story: dict, snapshot: dict, route: dict) -> str:
    from .path_story import validate_legacy_path_story, validate_path_story

    validator = validate_legacy_path_story if story.get("version") in {"character-path-v3", "edge-reasoning-v4"} else validate_path_story
    validator(story, snapshot, route)
    template = (ROOT / "storytelling" / "path_player.html").read_text(encoding="utf-8")
    library = (ROOT / "lib" / "vis-9.1.2" / "vis-network.min.js").read_text(encoding="utf-8")
    payload = json.dumps({"story": story, "graph": path_snapshot(snapshot, route)}, ensure_ascii=False)
    payload = payload.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return template.replace("/* VIS_LIBRARY */", library).replace("/* PATH_DATA */", payload)
