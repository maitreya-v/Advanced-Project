"""Reproducible, corpus-bound report generation for the three 2026 personas."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import ast
import hashlib
import importlib.util
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
REVIEW_DIR = ROOT / 'paper_reviews' / '2026'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text_hash_matches(path, expected):
    """Accept Git checkout newline conversion, while still checking exact text."""
    data = Path(path).read_bytes()
    normalized = data.replace(b'\r\n', b'\n')
    return expected in {
        hashlib.sha256(candidate).hexdigest()
        for candidate in (data, normalized, normalized.replace(b'\n', b'\r\n'))
    }


def load_review(age):
    ledger = json.loads((REVIEW_DIR / 'reviewed_decisions.json').read_text(encoding='utf-8'))
    if not text_hash_matches(REVIEW_DIR / 'extracted_papers.json', ledger['corpus_sha256']):
        raise ValueError('Extracted corpus changed; review evidence before rebuilding.')
    review = ledger['reviews'][str(age)]
    graph = ROOT / f'2026_{age} yo.py'
    if not text_hash_matches(graph, review['graph_sha256']):
        raise ValueError('Graph changed; reassess its edges before rebuilding.')
    tree = ast.parse(graph.read_text(encoding='utf-8'))
    edges = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'edges' for t in n.targets))
    if [list(e) for e in edges] != review['original_edges']:
        raise ValueError('Reviewed edge text/sign/strength differs from original.')
    for edge_id, (edge, row) in enumerate(zip(edges, review['edges']), 1):
        if (row['edge_id'],row['source'],row['dest'],row['sign'],row['existing_reasoning']) != (edge_id,edge[0],edge[1],edge[2],edge[4]):
            raise ValueError('Review row does not match the original edge.')
    if len(edges) != len(review['edges']):
        raise ValueError('Review does not cover every edge.')
    return ledger, review


def verify_corpus(ledger):
    """Check every supplied PDF and selected quotation against actual PDF pages."""
    corpus = json.loads((REVIEW_DIR / 'extracted_papers.json').read_text(encoding='utf-8'))
    expected = {record['file'] for record in corpus}
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / '2026 ADHD Papers').glob('*.pdf')}
    if actual != expected:
        raise ValueError('Supplied PDF membership changed; screen the corpus again.')
    by_id = {r['source_id']:r for r in corpus}
    for record in corpus:
        if sha(ROOT / record['file']) != record['sha256']:
            raise ValueError(f'Source PDF changed: {record["file"]}')
        text_hash = hashlib.sha256('\n'.join(record['pages']).encode()).hexdigest()
        if text_hash != record['text_sha256']:
            raise ValueError('Extracted text hash mismatch.')
    # Load the documented normalization function without re-extracting the corpus.
    spec = importlib.util.spec_from_file_location('extract_2026', REVIEW_DIR / 'extract_corpus.py')
    extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extractor)
    import pymupdf
    for evidence in ledger['excerpts'].values():
        record = by_id[evidence['source_id']]
        page = int(re.search(r'PDF page (\d+)', evidence['location'])[1])
        with pymupdf.open(ROOT / record['file']) as pdf:
            actual_text = extractor.normalize(pdf[page - 1].get_text())
        if actual_text != record['pages'][page - 1] or evidence['exact_excerpt'] not in actual_text:
            raise ValueError(f'Unverified PDF quotation: {evidence["source_id"]} page {page}')
    return corpus


def column_name(number):
    value = ''
    while number:
        number, remainder = divmod(number-1,26)
        value = chr(65+remainder) + value
    return value


def sheet_xml(data, widths):
    root = ET.Element('worksheet',xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main')
    view = ET.SubElement(ET.SubElement(root,'sheetViews'),'sheetView',workbookViewId='0')
    ET.SubElement(view,'pane',ySplit='1',topLeftCell='A2',activePane='bottomLeft',state='frozen')
    columns = ET.SubElement(root,'cols')
    for i,width in enumerate(widths,1):
        ET.SubElement(columns,'col',min=str(i),max=str(i),width=str(width),customWidth='1')
    body = ET.SubElement(root,'sheetData')
    for i,values in enumerate(data,1):
        row = ET.SubElement(body,'row',r=str(i),ht='30' if i==1 else '110',customHeight='1')
        for j,value in enumerate(values,1):
            cell = ET.SubElement(row,'c',r=f'{column_name(j)}{i}',t='inlineStr',s='1' if i==1 else '0')
            ET.SubElement(ET.SubElement(cell,'is'),'t',{'{http://www.w3.org/XML/1998/namespace}space':'preserve'}).text = '' if value is None else str(value)
    ET.SubElement(root,'autoFilter',ref=f'A1:{column_name(len(data[0]))}{len(data)}')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)


def write_workbook(path, sheets):
    """Write and round-trip-check a small dependency-free OOXML workbook."""
    content_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
    rel_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    office_rel = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
    spreadsheet_ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    types = ET.Element('Types',xmlns=content_ns)
    ET.SubElement(types,'Default',Extension='rels',ContentType='application/vnd.openxmlformats-package.relationships+xml')
    ET.SubElement(types,'Default',Extension='xml',ContentType='application/xml')
    for part,kind in [('workbook.xml','sheet.main'),('styles.xml','styles')]:
        ET.SubElement(types,'Override',PartName='/xl/'+part,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.'+kind+'+xml')
    for i in range(1,len(sheets)+1):
        ET.SubElement(types,'Override',PartName=f'/xl/worksheets/sheet{i}.xml',ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
    package_rels = ET.Element('Relationships',xmlns=rel_ns)
    ET.SubElement(package_rels,'Relationship',Id='rId1',Type=office_rel+'officeDocument',Target='xl/workbook.xml')
    workbook = ET.Element('workbook',xmlns=spreadsheet_ns)
    sheet_list = ET.SubElement(workbook,'sheets')
    relations = ET.Element('Relationships',xmlns=rel_ns)
    for i,(name,_,_) in enumerate(sheets,1):
        ET.SubElement(sheet_list,'sheet',name=name,sheetId=str(i),attrib={'{'+office_rel[:-1]+'}id':f'rId{i}'})
        ET.SubElement(relations,'Relationship',Id=f'rId{i}',Type=office_rel+'worksheet',Target=f'worksheets/sheet{i}.xml')
    ET.SubElement(relations,'Relationship',Id='styles',Type=office_rel+'styles',Target='styles.xml')
    styles = '''<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF24476A"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>'''
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,root in [('[Content_Types].xml',types),('_rels/.rels',package_rels),('xl/workbook.xml',workbook),('xl/_rels/workbook.xml.rels',relations)]:
            archive.writestr(name,ET.tostring(root,encoding='utf-8',xml_declaration=True))
        archive.writestr('xl/styles.xml',styles)
        for i,(_,data,widths) in enumerate(sheets,1):
            archive.writestr(f'xl/worksheets/sheet{i}.xml',sheet_xml(data,widths))
    with zipfile.ZipFile(path) as archive:
        if archive.testzip():
            raise ValueError('Invalid XLSX archive')
        for name in archive.namelist():
            ET.fromstring(archive.read(name))
        ns = {'s':spreadsheet_ns}
        for i,(_,data,_) in enumerate(sheets,1):
            worksheet = ET.fromstring(archive.read(f'xl/worksheets/sheet{i}.xml'))
            actual = [[c.find('s:is/s:t',ns).text or '' for c in row] for row in worksheet.findall('s:sheetData/s:row',ns)]
            if actual != [['' if v is None else str(v) for v in row] for row in data]:
                raise ValueError('XLSX values differ from report values')


def build_report(folder):
    folder = Path(folder).resolve()
    age = int(re.fullmatch(r'validation_2026_age(8|32|45)',folder.name)[1])
    ledger,review = load_review(age)
    corpus = verify_corpus(ledger)
    # Point directly at the committed corpus. No directory links or PDF copies
    # are required on Windows, macOS or Linux.
    rows = review['edges']
    cited = {ev['source_id'] for row in rows for ev in row['evidence']}
    counts = {status:Counter(r['validation_status'] for r in rows)[status] for status in ledger['status_definitions']}
    references,documents = [],[]
    for record in corpus:
        note = ledger['source_notes'].get(record['source_id'],{})
        title = note.get('title') or record['metadata_title'] or Path(record['file']).name
        ref = dict(source_id=record['source_id'],title=title,
                   local_pdf='../'+Path(record['file']).as_posix(),sha256=record['sha256'],
                   duplicate_of=record['duplicate_of'],page_count=record['page_count'],
                   evidence_scope=note.get('evidence_scope','Screened supplied document; no passage selected for this age graph. This is not a claim that the study is irrelevant or negative.'),
                   cited_in_this_graph=record['source_id'] in cited)
        references.append(ref)
        documents.append(dict(file=ref['local_pdf'],source_file=record['file'],source_id=record['source_id'],
                              sha256=record['sha256'],text_sha256=record['text_sha256'],
                              duplicate_of=record['duplicate_of'],page_count=record['page_count']))
    methodology = {
        'scope':f'2026_{age} yo.py: all {len(rows)} original edges reviewed against 159 supplied PDFs (158 distinct normalized full-text documents), 2,212 file pages. The year refers to the graph snapshot and supplied folder, not a claim that all papers were first published in 2026.',
        'review_depth':'All supplied documents were screened by titles/first pages and available abstracts; relevant full-text passages were reviewed for graph claims. This is a targeted corpus validation, not exhaustive critical appraisal of all 2,212 pages or an external systematic review.',
        'age_scope':('Pediatric evidence overlapping approximately age eight was preferred. Broad pediatric results receive partial support where population, construct or causal scope does not fully match; adolescent-only findings are not transferred to age eight.' if age==8 else f'Adult ADHD evidence relevant to age {age} was preferred. Broad adult findings receive partial support when no exact-age effect or matching mechanism is established. Pediatric-only evidence and studies restricted to age 50+ are not transferred to this adult persona.'),
        'causal_standard':'Assess direction, sign, endpoint and written reasoning. Association, clinical recommendations, co-occurrence, service uptake and mechanistic plausibility are distinguished from experimental causal evidence. Null tests on different exposures/outcomes are not labeled contradictions.',
        'strength':'Numeric edge strengths and the widths that encode them are retained for fidelity and are NOT validated effect sizes. All original edges, signs, reasoning, node positions and domain colors are preserved; only validation styling and evidence are added.',
        'constructs':'Categorical variables require comparator coding; undefined treatment dependency/overdiagnosis pressure and treatment-receipt-versus-benefit mismatches are not assessable. Treatment effects do not establish diagnosis-only benefits.',
        'duplicates':'The two 1-s2.0-S1087079226000754-main PDFs have different binary hashes but identical normalized page text and represent one sleep-intervention review. Duplicate copies are not independent evidence. Other reviews may share primary studies; 158 distinct documents are not 158 independent studies.',
        'quotations':'PDF locations use one-based file pages. Native PDF reading order preserves columns; Unicode NFKC, soft-hyphen removal, end-of-line word dehyphenation and whitespace normalization are documented in extract_corpus.py. Every selected quotation is checked against actual source PDF-page text at build time.',
        'provenance':'Graph SHA-256, every supplied PDF SHA-256, text hashes and reviewed corpus hash are checked. New/changed graphs or source PDFs require reassessment before rebuilding. PDF references point directly to the committed 2026 ADHD Papers folder through relative paths; no directory links are required. Git checkout newline conversions are accepted for reviewed text files only.',
        'limits':'Insufficient evidence means this corpus does not establish the claim; it does not mean the edge is false. Supported refers to the declared qualitative pathway, not clinical recommendations or personalized treatment advice. No external papers were added.',
    }
    metadata = dict(graph_file=f'2026_{age} yo.py',graph_sha256=review['graph_sha256'],graph_year=2026,
                    age=age,edge_count=len(rows),pdf_file_count=len(corpus),unique_document_count=len({r['text_sha256'] for r in corpus}),
                    html_file_count=0,total_pdf_pages=sum(r['page_count'] for r in corpus),
                    cited_document_count=len(cited),validation_updated_utc=datetime.now(timezone.utc).isoformat(),
                    original_unchanged=True,strength_assessed=False,status_counts=counts,
                    reviewed_corpus_sha256=ledger['corpus_sha256'])
    report = dict(metadata=metadata,status_definitions=ledger['status_definitions'],methodology=methodology,edges=rows,references=references)
    outputs = {'manifest.json':{**metadata,'documents':documents},'original_edges.json':review['original_edges'],
               'edge_validation.json':report,'supplied_papers.json':references,
               'full_text_review.json':{'summary':metadata,'excerpts':{k:v for k,v in ledger['excerpts'].items() if v['source_id'] in cited}}}
    for name,data in outputs.items():
        (folder/name).write_text(json.dumps(data,indent=2,ensure_ascii=False), encoding='utf-8', newline='\n')
    headers = ['Edge ID','Source','Destination','Existing reasoning','Sign','Validation status','Observation','Recommended action','Evidence']
    fields = ['edge_id','source','dest','existing_reasoning','sign','validation_status','observation_from_validation','recommended_action']
    edge_data = [headers]+[[row[f] for f in fields]+['\n\n'.join(f'{e["source_id"]}: {e["exact_excerpt"]}\nLocation: {e["location"]}\nRelevance: {e["relevance"]}' for e in row['evidence']) or 'No directly relevant excerpt selected'] for row in rows]
    reference_data = [['Source ID','Title','Local PDF','SHA-256','Duplicate of','Evidence scope','Cited here']]+[[r[k] for k in ['source_id','title','local_pdf','sha256','duplicate_of','evidence_scope','cited_in_this_graph']] for r in references]
    method_data = [['Item','Explanation']]+list(map(list,methodology.items()))+[[f'Status: {k}',v] for k,v in ledger['status_definitions'].items()]
    write_workbook(folder/'edge_validation.xlsx',[('Edge validation',edge_data,[10,28,28,65,9,30,90,75,100]),('References',reference_data,[18,90,80,68,18,110,15]),('Read me',method_data,[28,145])])
    readme = f'# 2026 age-{age} graph validation\n\nValidation of **2026_{age} yo.py**: **{len(rows)} edges**, using the supplied **159 PDFs / 158 distinct full-text documents** in `2026 ADHD Papers`.\n\nOpen [validated_graph.html](validated_graph.html) in a browser and click any edge for its status, decision and page-linked evidence. Colors and dashes encode validation; original widths retain unvalidated strengths.\n\nReview [edge_validation.xlsx](edge_validation.xlsx) for the edge, reference and methodology worksheets. Machine-readable decisions are in [edge_validation.json](edge_validation.json), with provenance in [manifest.json](manifest.json) and checks in [verification.json](verification.json).\n\n## Status counts\n\n'+''.join(f'- `{s}`: {n}\n' for s,n in counts.items())+'\n## Method and limitations\n\n'+'\n\n'.join(f'**{k.replace("_"," ").title()}**: {v}' for k,v in methodology.items())+'\n\n## Reproduce\n\nFrom the project root, run:\n\n```sh\n'+f'.venv/bin/python validation_2026_age{age}/build_report.py\n.venv/bin/python validation_2026_age{age}/build_validated_graph.py\n```\n\n'+'Requires the project environment (`pyvis`, `pymupdf`). Reports validate against the saved, manually reviewed decisions; they do not automatically re-review changed literature. Shared review sources and reproducible text extraction are in [paper_reviews/2026](../paper_reviews/2026/README.md). The `full_texts` directory links to the supplied PDFs; no original graph or paper is modified.\n'
    readme = readme.replace('The `full_texts` directory links to the supplied PDFs;', 'PDF references point directly to `../2026 ADHD Papers/`; no directory links are required and')
    (folder/'README.md').write_text(readme, encoding='utf-8', newline='\n')
    checks = dict(graph=metadata['graph_file'],edges_reviewed=len(rows),pdf_files_screened=len(corpus),
                  unique_documents_screened=metadata['unique_document_count'],selected_pdf_quotations_verified=len(ledger['excerpts']),
                  original_sha256=metadata['graph_sha256'],original_unchanged=text_hash_matches(ROOT/metadata['graph_file'],metadata['graph_sha256']),
                  all_edge_reasons_and_signs_preserved=True,all_original_strengths_preserved=True,strength_assessed=False,
                  all_source_pdf_hashes_verified=True,all_citations_in_supplied_corpus=True,
                  all_selected_excerpts_verified_against_source_pdfs=True,xlsx_xml_valid=True,xlsx_json_rows_match=True,
                  xlsx_data_rows=len(rows),status_counts=counts,compact_edge_fields=list(rows[0]))
    (folder/'verification.json').write_text(json.dumps(checks,indent=2), encoding='utf-8', newline='\n')
    print(json.dumps({'age':age,'edges':len(rows),'status_counts':counts}))
    return report
