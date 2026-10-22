"""A self-contained scene player; playback needs no model or external CDN."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def player_html(story: dict, before: dict, after: dict) -> str:
    template = (ROOT / "storytelling" / "player.html").read_text(encoding="utf-8")
    vis = (ROOT / "lib" / "vis-9.1.2" / "vis-network.min.js").read_text(encoding="utf-8")
    payload = json.dumps({"story": story, "before": before, "after": after}, ensure_ascii=False)
    payload = payload.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return template.replace("/* VIS_LIBRARY */", vis).replace("/* STORY_DATA */", payload)
