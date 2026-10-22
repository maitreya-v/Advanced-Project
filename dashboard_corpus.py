"""Year-level corpus counts from the workbook and validation reports."""
from pathlib import Path
from zipfile import ZipFile
import json
import hashlib
import html
import posixpath
import xml.etree.ElementTree as ET

import streamlit as st

ROOT = Path(__file__).resolve().parent
WORKBOOK = ROOT / "ADHD_Literature_Corpus_Batch1.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def workbook_rows(path):
    """Read cached XLSX cell values without an additional Excel dependency."""
    with ZipFile(path) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            strings = ["".join(node.itertext()) for node in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("m:si", NS)]
        relationships = {item.get("Id"): item.get("Target") for item in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))}
        result = {}
        for sheet in ET.fromstring(archive.read("xl/workbook.xml")).findall("m:sheets/m:sheet", NS):
            target = relationships[sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")]
            filename = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
            rows = []
            for row in ET.fromstring(archive.read(filename)).findall("m:sheetData/m:row", NS):
                values = {}
                for cell in row:
                    value = cell.find("m:v", NS)
                    inline = cell.find("m:is", NS)
                    text = value.text or "" if value is not None else "".join(inline.itertext()) if inline is not None else ""
                    if cell.get("t") == "s":
                        text = strings[int(text)]
                    values["".join(char for char in cell.get("r") if char.isalpha())] = text
                rows.append(values)
            result[sheet.get("name")] = rows
        return result


def corpus_counts(year, workbook=WORKBOOK, root=ROOT):
    sheets = workbook_rows(workbook)
    summary = sheets["Screening Summary"]
    column = next((key for key, value in summary[0].items() if value == str(year)), None)
    if column is None:
        return None
    total = next(int(row[column]) for row in summary[1:] if row["A"] == "Unique records after PMID dedup")
    catalog = sheets["Batch 1 Catalog"]
    headers = {value: key for key, value in catalog[0].items()}
    papers = {}
    for row in catalog[1:]:
        if row.get(headers["Publication year"]) == str(year):
            papers[row[headers["PMID"]]] = row
    full = {pmid for pmid, row in papers.items() if row.get(headers["Verified Open Access?"], "").lower() == "yes" or row.get(headers["PDF Availability Status"], "") == "PDF available via PMC (verified free full text)"}
    abstracts = {pmid for pmid, row in papers.items() if row.get(headers["Access level"], "").lower() == "abstract only"} - full
    # A year-level union stays the same when the user changes age.
    reviewed = {}
    has_reports = False
    for age in (8, 32, 45):
        folder = root / f"validation_{year}_age{age}"
        report_path = folder / "edge_validation.json"
        if not report_path.exists():
            continue
        has_reports = True
        for ref in json.loads(report_path.read_text())["references"]:
            # Alternate copies in the 2026 corpus share a canonical source ID.
            identity = ref.get("duplicate_of") or ref.get("pmid") or ref.get("source_id")
            # Alternate HTML/PDF formats identified in the 2010 review.
            if year == 2010:
                identity = {"PMID_20410711": "AGE_SEX", "CAUDATE_HTML": "CAUDATE_MRI"}.get(identity, identity)
            if ref.get("local_pdf") and (folder / ref["local_pdf"]).is_file():
                reviewed[identity] = "pdf"
            elif ref.get("local_html") and (folder / ref["local_html"]).is_file():
                reviewed.setdefault(identity, "abstract")
    return dict(total=total, selected=len(papers), accessible=len(full | abstracts), full_text=len(full), abstract_only=len(abstracts), reviewed=len(reviewed) if has_reports else None, reviewed_pdf=sum(value == "pdf" for value in reviewed.values()), reviewed_abstract=sum(value == "abstract" for value in reviewed.values()))


def workbook_viewer(path):
    """Build a browser-readable, escaped view of every workbook sheet."""
    sheets = workbook_rows(path)
    options = []
    sections = []
    for index, (name, rows) in enumerate(sheets.items()):
        options.append(f'<option value="sheet-{index}">{html.escape(name)}</option>')
        columns = sorted({column for row in rows for column in row}, key=lambda value: (len(value), value))
        table_rows = []
        for row_index, row in enumerate(rows):
            tag = "th" if row_index == 0 else "td"
            cells = "".join(f'<{tag}>{html.escape(row.get(column, ""))}</{tag}>' for column in columns)
            table_rows.append(f"<tr>{cells}</tr>")
        sections.append(f'<section id="sheet-{index}" {"hidden" if index else ""}><h2>{html.escape(name)}</h2><table>{"".join(table_rows)}</table></section>')
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ADHD Literature Corpus Batch1</title>
<style>
:root {color-scheme:light dark} body {font:14px/1.5 system-ui,sans-serif;margin:24px;background:Canvas;color:CanvasText}
header {position:sticky;top:0;background:Canvas;padding:12px 0;z-index:2;border-bottom:1px solid GrayText}
h1 {font-size:22px;margin:0 0 12px} h2 {font-size:18px} select {font:inherit;padding:8px;max-width:100%}
table {border-collapse:collapse} th,td {border:1px solid GrayText;padding:8px;min-width:100px;max-width:420px;vertical-align:top;white-space:pre-wrap;overflow-wrap:anywhere}
th {text-align:left;background:ButtonFace;color:ButtonText} [hidden] {display:none}
</style></head><body><header><h1>ADHD Literature Corpus Batch1</h1>
<label for="sheet">Sheet: </label><select id="sheet">""" + "".join(options) + """</select></header>""" + "".join(sections) + """
<script>document.getElementById('sheet').addEventListener('change',event=>{
 document.querySelectorAll('section').forEach(section=>section.hidden=section.id!==event.target.value);
 window.scrollTo(0,0);
});</script></body></html>"""


def render_corpus_counts(year):
    try:
        counts = corpus_counts(year)
    except (OSError, KeyError, ValueError):
        st.caption("Paper counts unavailable: check ADHD_Literature_Corpus_Batch1.xlsx.")
        return
    with st.container(border=True):
        st.markdown(f"**Paper corpus · {year}**")
        if counts is None:
            st.caption("This year is not listed in the workbook.")
            return
        st.markdown(
            f"PubMed records: **{counts['total']:,}**  \n"
            f"Batch 1 selected: **{counts['selected']:,}**"
        )
        if counts["reviewed"] is not None:
            st.markdown(f"Reviewed for validation: **{counts['reviewed']:,}**  \nPDFs: **{counts['reviewed_pdf']}** · Abstracts only: **{counts['reviewed_abstract']}**")
        else:
            st.caption("Validation usage has not been recorded for this year.")
        data = WORKBOOK.read_bytes()
        filename = "ADHD_Literature_Corpus_Batch1-" + hashlib.sha256(data).hexdigest()[:12] + ".html"
        assets = ROOT / "dashboard_validation_popup" / "references"
        assets.mkdir(exist_ok=True)
        target = assets / filename
        if not target.exists():
            target.write_text(workbook_viewer(WORKBOOK), encoding="utf-8")
        base_path = st.get_option("server.baseUrlPath").strip("/")
        url = "/" + (base_path + "/" if base_path else "") + "component/dashboard_validation.dashboard_validation_popup/references/" + filename
        st.markdown(f'Source: <a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">ADHD Literature Corpus Batch1</a>', unsafe_allow_html=True)
