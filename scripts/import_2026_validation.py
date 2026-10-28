"""Copy missing 2026 review artifacts from a local Git ref without overwriting files."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "main"
PATHS = [
    "2026 ADHD Papers", "paper_reviews/2026", "validation_2026_utils.py",
    "validation_2026_age8", "validation_2026_age32", "validation_2026_age45",
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    entries = git("ls-tree", "-rz", SOURCE, "--", *PATHS).split(b"\0")
    pending = []
    for entry in filter(None, entries):
        info, name = entry.split(b"\t", 1)
        mode, _, oid = info.split()
        path = ROOT / name.decode("utf-8")
        path.resolve().relative_to(ROOT.resolve())
        if mode == b"120000":
            # Windows directory junctions are created separately for standalone HTML.
            continue
        data = git("cat-file", "blob", oid.decode())
        if path.exists():
            if path.read_bytes() != data:
                raise RuntimeError(f"Refusing to overwrite existing file: {path.relative_to(ROOT)}")
        else:
            pending.append((path, data))
    for path, data in pending:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as target:
            target.write(data)
    print(f"Added {len(pending)} files from {SOURCE} ({git('rev-parse', '--short', SOURCE).decode().strip()}).")


if __name__ == "__main__":
    main()
