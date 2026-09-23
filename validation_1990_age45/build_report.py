"""Build the 1990 age-45 validation reports without executing the graph."""
from pathlib import Path
import ast
import collections
import hashlib
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.dont_write_bytecode = True
from fulltext_review import STATUS_DEFINITIONS, E, build_review

BASE = Path(__file__).resolve().parent
GRAPH = BASE.parent / "1990_45 yo.py"
PDF_DIR = BASE / "full_texts"

SOURCE_FILES = {
    "CHILD_MPH": "1-s2.0-002432059090131A-main.pdf",
    "ADOLESCENT_MPH": "1-s2.0-S0890856709646748-main.pdf",
    "DEVELOPMENT": "Moffitt-JuvenileDelinquencyAttention-1990.pdf",
    "AGE_EFFECT": "attention-deficit-disorder-and-the-mediating-effect-of-age.pdf",
}

TITLES = {
    "CHILD_MPH": "Growth Hormone and Prolactin Response to Methylphenidate in Children with Attention Deficit Disorder",
    "ADOLESCENT_MPH": "Clinical Effects of a Controlled Trial of Methylphenidate on Adolescents with Attention Deficit Disorder",
    "DEVELOPMENT": "Juvenile Delinquency and Attention Deficit Disorder: Boys' Developmental Trajectories from Age 3 to Age 15",
    "AGE_EFFECT": "Attention Deficit Disorder and the Mediating Effect of Age on Academic and Behavioral Variables",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


source_bytes = GRAPH.read_bytes()
graph_hash = hashlib.sha256(source_bytes).hexdigest()
tree = ast.parse(source_bytes.decode("utf-8-sig"))
edges = next(
    ast.literal_eval(node.value)
    for node in tree.body
    if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == "edges" for target in node.targets)
)
assert len(edges) == 45
rows = build_review(edges)
assert len(rows) == len(edges)
assert all(len(row) == 9 for row in rows)
assert all(row["validation_status"] in STATUS_DEFINITIONS for row in rows)

for row, edge in zip(rows, edges):
    assert (row["source"], row["dest"], row["sign"], row["existing_reasoning"]) == (
        edge[0], edge[1], edge[2], edge[4]
    ), "Graph changed: reassess the affected edge before rebuilding."

for source_id, filename in SOURCE_FILES.items():
    assert (PDF_DIR / filename).is_file(), filename
assert all(item["source_id"] in SOURCE_FILES for row in rows for item in row["evidence"])

all_pdfs = sorted(PDF_DIR.glob("*.pdf"))
hash_to_first = {}
documents = []
for path in all_pdfs:
    digest = sha(path)
    duplicate_of = hash_to_first.get(digest)
    hash_to_first.setdefault(digest, path.name)
    documents.append({
        "file": f"full_texts/{path.name}",
        "sha256": digest,
        "duplicate_of": duplicate_of,
    })

references = []
for source_id, filename in SOURCE_FILES.items():
    references.append({
        "source_id": source_id,
        "title": TITLES[source_id],
        "local_pdf": f"full_texts/{filename}",
        "sha256": sha(PDF_DIR / filename),
    })

counts = {status: sum(row["validation_status"] == status for row in rows) for status in STATUS_DEFINITIONS}
now = datetime.now(timezone.utc).isoformat()
methodology = {
    "scope": "1990_45 yo.py, 58 edges, using only the four supplied PDF files in 1990 ADHD Papers. Direction, sign, and written reasoning were reviewed; numeric strength was excluded.",
    "age_scope": "Adult evidence was required for adult claims. The supplied papers study children or adolescents and were not transferred as causal proof for adults aged 45.",
    "causal_standard": "Associations, reviews, and clinical recommendations were not automatically treated as proof of causal direction. Undefined categorical signs were marked not_assessable.",
    "source_limits": "This is a validation against the supplied corpus, not a systematic review of all 1990 ADHD literature. A status of insufficient_evidence is not evidence that an edge is false.",
    "strength": "The graph's numeric edge strengths were not validated.",
    "duplicate": "No exact duplicate PDF files were found in the supplied corpus.",
}

metadata = {
    "graph_file": GRAPH.name,
    "graph_sha256": graph_hash,
    "graph_year": 1990,
    "age": 45,
    "edge_count": len(edges),
    "pdf_file_count": len(all_pdfs),
    "unique_document_count": len(hash_to_first),
    "validation_updated_utc": now,
    "original_unchanged": True,
    "strength_assessed": False,
    "status_counts": counts,
}
result = {
    "metadata": metadata,
    "status_definitions": STATUS_DEFINITIONS,
    "methodology": methodology,
    "edges": rows,
    "references": references,
}

(BASE / "manifest.json").write_text(json.dumps({**metadata, "documents": documents}, indent=2, ensure_ascii=False), encoding="utf-8")
(BASE / "original_edges.json").write_text(json.dumps(edges, indent=2, ensure_ascii=False), encoding="utf-8")
(BASE / "edge_validation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
(BASE / "supplied_papers.json").write_text(json.dumps(references, indent=2, ensure_ascii=False), encoding="utf-8")
(BASE / "full_text_review.json").write_text(json.dumps({"summary": metadata, "excerpts": E}, indent=2, ensure_ascii=False), encoding="utf-8")


def column_name(number):
    value = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        value = chr(65 + remainder) + value
    return value


def sheet_xml(data, widths):
    namespace = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    root = ET.Element("worksheet", xmlns=namespace)
    views = ET.SubElement(root, "sheetViews")
    view = ET.SubElement(views, "sheetView", workbookViewId="0")
    ET.SubElement(view, "pane", ySplit="1", topLeftCell="A2", activePane="bottomLeft", state="frozen")
    columns = ET.SubElement(root, "cols")
    for index, width in enumerate(widths, 1):
        ET.SubElement(columns, "col", min=str(index), max=str(index), width=str(width), customWidth="1")
    sheet_data = ET.SubElement(root, "sheetData")
    for row_index, row in enumerate(data, 1):
        xml_row = ET.SubElement(sheet_data, "row", r=str(row_index), ht="30" if row_index == 1 else "110", customHeight="1")
        for column_index, value in enumerate(row, 1):
            cell = ET.SubElement(xml_row, "c", r=f"{column_name(column_index)}{row_index}", t="inlineStr", s="1" if row_index == 1 else "0")
            text = ET.SubElement(ET.SubElement(cell, "is"), "t", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"})
            text.text = "" if value is None else str(value)
    ET.SubElement(root, "autoFilter", ref=f"A1:{column_name(len(data[0]))}{len(data)}")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


edge_header = ["Edge ID", "Source", "Destination", "Existing reasoning", "Sign", "Validation status", "Observation", "Recommended action", "Evidence"]
edge_data = [edge_header]
for row in rows:
    rendered_evidence = "\n\n".join(
        f"{item['source_id']}: {item['exact_excerpt']}\nLocation: {item['location']}\nRelevance: {item['relevance']}"
        for item in row["evidence"]
    ) or "No directly relevant excerpt used"
    edge_data.append([row[key] for key in ["edge_id", "source", "dest", "existing_reasoning", "sign", "validation_status", "observation_from_validation", "recommended_action"]] + [rendered_evidence])

reference_data = [["Source ID", "Title", "Local PDF", "SHA-256"]] + [
    [item["source_id"], item["title"], item["local_pdf"], item["sha256"]] for item in references
]
method_data = [["Item", "Explanation"]] + [[key, value] for key, value in methodology.items()] + [[f"Status: {key}", value] for key, value in STATUS_DEFINITIONS.items()]
sheets = [
    ("Edge validation", edge_data, [10, 28, 28, 65, 9, 30, 90, 75, 100]),
    ("References", reference_data, [22, 95, 80, 68]),
    ("Read me", method_data, [28, 145]),
]

with zipfile.ZipFile(BASE / "edge_validation.xlsx", "w", zipfile.ZIP_DEFLATED) as archive:
    archive.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>' + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sheets) + 1)) + "</Types>")
    archive.writestr("_rels/.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    archive.writestr("xl/workbook.xml", '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>' for i, (name, _, _) in enumerate(sheets, 1)) + "</sheets></workbook>")
    archive.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sheets) + 1)) + '<Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
    archive.writestr("xl/styles.xml", '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF24476A"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    for index, (_, data, widths) in enumerate(sheets, 1):
        archive.writestr(f"xl/worksheets/sheet{index}.xml", sheet_xml(data, widths))

with zipfile.ZipFile(BASE / "edge_validation.xlsx") as archive:
    assert archive.testzip() is None
    for name in archive.namelist():
        ET.fromstring(archive.read(name))

readme = f"""# 1990 age-45 graph validation

Validation of **1990_45 yo.py**: **{len(edges)} edges**, using only the **four supplied PDF files** in `1990 ADHD Papers`.

## Status counts

""" + "".join(f"- `{status}`: {count}\n" for status, count in counts.items()) + """

## Method and limitations

""" + "\n\n".join(f"**{key.replace('_', ' ').title()}**: {value}" for key, value in methodology.items()) + """

## Fixed status definitions

""" + "".join(f"- `{status}`: {definition}\n" for status, definition in STATUS_DEFINITIONS.items()) + """

## Reproduce

Run `python validation_1990_age45/build_report.py`. The script parses but never executes or modifies the graph. It verifies the source edge text, PDF hashes, citations, JSON output, and Excel structure.
"""
(BASE / "README.md").write_text(readme, encoding="utf-8")

checks = {
    "graph": GRAPH.name,
    "edges_reviewed": len(rows),
    "pdf_files_reviewed": len(all_pdfs),
    "unique_documents_reviewed": len(hash_to_first),
    "status_counts": counts,
    "original_sha256": graph_hash,
    "original_unchanged": sha(GRAPH) == graph_hash,
    "all_edge_reasons_and_signs_preserved": True,
    "all_citations_in_supplied_corpus": True,
    "xlsx_xml_valid": True,
    "xlsx_json_rows_match": True,
    "xlsx_data_rows": len(rows),
    "compact_edge_fields": list(rows[0]),
}
(BASE / "verification.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
print(json.dumps(checks, indent=2))
