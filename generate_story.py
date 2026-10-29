"""Generate and save a demo story with local Qwen (or a labeled rule baseline)."""
import argparse
from pathlib import Path

from storytelling.analysis import THEMES
from storytelling.data import ROOT, load_snapshots
from storytelling.director import LocalOllama, baseline_story, generate_story, save_story


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-year", type=int, default=2010)
    parser.add_argument("--to-year", type=int, default=2026)
    parser.add_argument("--age", type=int, default=8)
    parser.add_argument("--to-age", type=int, help="For an age comparison, keep both years equal.")
    parser.add_argument("--theme", choices=list(THEMES), default="Treatment and access")
    parser.add_argument("--question", default="")
    parser.add_argument("--model", choices=["qwen3:8b", "qwen3:4b"], default="qwen3:8b")
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "stories")
    args = parser.parse_args()
    snapshots = load_snapshots()
    before = snapshots[args.from_year][args.age]
    after = snapshots[args.to_year][args.to_age or args.age]
    if args.baseline:
        story = baseline_story(before, after, args.theme, args.question)
    else:
        story = generate_story(before, after, args.theme, args.question, LocalOllama(model=args.model))
    path = save_story(story, args.output_dir)
    print(f"Saved {story['origin']} story to {path}")
    print(f"{len(story['scenes'])} scenes; {story['elapsed_seconds']} seconds; {len(story['trace'])} tool calls")
    for scene in story["scenes"]:
        print(f"\n{scene['title']}\n{scene['narration']}")


if __name__ == "__main__":
    main()
