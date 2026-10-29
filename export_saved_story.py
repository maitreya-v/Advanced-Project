"""Export a checked saved story as a self-contained HTML file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from storytelling.data import load_snapshots
from storytelling.director import load_story
from storytelling.player import player_html
from storytelling.path_player import path_player_html
from storytelling.path_story import load_path_story, validate_legacy_path_story


def export_saved_story(story_path: Path, output_path: Path) -> Path:
    snapshots = load_snapshots()
    saved = json.loads(story_path.read_text(encoding="utf-8"))
    if saved.get("mode") == "path":
        snapshot = snapshots[saved["snapshot"]["year"]][saved["snapshot"]["age"]]
        route = saved["route"]
        if saved.get("version") in {"character-path-v3", "edge-reasoning-v4"}:
            validate_legacy_path_story(saved, snapshot, route)
            story = saved
        else:
            story = load_path_story(story_path, snapshot, route, saved.get("question", ""))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(path_player_html(story, snapshot, route), encoding="utf-8")
        return output_path
    before = snapshots[saved["before"]["year"]][saved["before"]["age"]]
    after = snapshots[saved["after"]["year"]][saved["after"]["age"]]
    story = load_story(story_path, before, after, saved["theme"], saved.get("question", ""))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(player_html(story, before, after), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("story", type=Path, help="Saved story JSON")
    parser.add_argument("output", type=Path, help="Destination HTML")
    args = parser.parse_args()
    print(f"Exported {export_saved_story(args.story, args.output)}")


if __name__ == "__main__":
    main()
