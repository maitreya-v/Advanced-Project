"""Extract the supplied 2026 corpus with reproducible PDF page locations."""
from pathlib import Path
import hashlib
import json
import re
import pymupdf
import unicodedata

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]


def normalize(text):
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '')
    text = re.sub(r'(\w)-\n(?=\w)', r'\1', text)
    return re.sub(r"\s+", " ", text).strip()


def extract():
    records = []
    seen = {}
    for index, path in enumerate(sorted((ROOT / "2026 ADHD Papers").glob("*.pdf")), 1):
        with pymupdf.open(path) as pdf:
            # Native reading order preserves columns; geometric sorting interleaves
            # many journal abstracts with sidebars and corrupts quotations.
            pages = [normalize(page.get_text()) for page in pdf]
            metadata = pdf.metadata
        text_hash = hashlib.sha256("\n".join(pages).encode()).hexdigest()
        source_id = f"PDF_{index:03}"
        records.append({
            "source_id": source_id,
            "file": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "text_sha256": text_hash,
            "duplicate_of": seen.get(text_hash),
            "metadata_title": metadata.get("title", ""),
            "pages": pages,
            "page_count": len(pages),
            "extraction_empty": not any(pages),
        })
        seen.setdefault(text_hash, source_id)
    (BASE / "extracted_papers.json").write_text(json.dumps(records, indent=2, ensure_ascii=False))
    # First-page excerpts permit a systematic screen before reading relevant full-text pages.
    (BASE / "screening.txt").write_text("\n\n".join(
        f"{r['source_id']} | {Path(r['file']).name} | {r['page_count']} pages | duplicate={r['duplicate_of']}\n{r['pages'][0][:6500]}"
        for r in records
    ))
    print(f"Extracted {len(records)} PDFs, {sum(r['page_count'] for r in records)} pages; {sum(r['extraction_empty'] for r in records)} empty documents")


if __name__ == "__main__":
    extract()
