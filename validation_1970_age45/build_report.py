"""Build age-specific 1970 validation outputs; never execute or modify the graph."""
from pathlib import Path
import ast, collections, hashlib, json, sys, zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
sys.dont_write_bytecode = True
from fulltext_review import REVIEW
BASE = Path(__file__).resolve().parent
GRAPH = BASE.parent / '1970_45 yo.py'
GRAPH_1990 = BASE.parent / '1990_8 yo.py'
before_1990 = hashlib.sha256(GRAPH_1990.read_bytes()).hexdigest()
source_bytes = GRAPH.read_bytes()
original_hash = hashlib.sha256(source_bytes).hexdigest()
tree = ast.parse(source_bytes.decode('utf-8-sig'))
edges = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='edges' for t in n.targets))
rows = REVIEW['edges']
refs = REVIEW['references']
definitions = REVIEW['status_definitions']
assert len(rows)==len(edges)==37
for r,e in zip(rows,edges):
    assert (r['source'],r['dest'],r['sign'],r['existing_reasoning']) == (e[0],e[1],e[2],e[4]), 'Graph changed: reassess affected edge before rebuilding.'
    assert len(r)==9 and r['validation_status'] in definitions
allowed = {p['pmid'] for p in refs}
assert allowed == {'5538099','5523436','5491539','4950109'}
assert all(e['pmid'] in allowed for r in rows for e in r['evidence'])
for d in REVIEW['documents']:
    assert hashlib.sha256((BASE/d['file']).read_bytes()).hexdigest()==d['sha256']
counts = {s:sum(r['validation_status']==s for r in rows) for s in definitions}
now = datetime.now(timezone.utc).isoformat()
manifest = {'graph_file':str(GRAPH),'graph_sha256':original_hash,'graph_year':1970,'age':45,'edge_count':37,'paper_count':4,'reference_pmids':sorted(allowed),'validation_updated_utc':now,'documents':REVIEW['documents']}
methods = [
 ('Scope','1970_45 yo.py, 37 edges, using only four supplied papers (PMIDs 5538099, 5523436, 5491539, 4950109). Review direction, sign and reasoning; strength excluded.'),
 ('Result','No adult edge receives causal support from these four pediatric/animal papers. Relevant pediatric statements are retained as context, not transferred as adult findings. Undefined signs/endpoints are not_assessable; other adult claims have insufficient_evidence. Missing support is not disproof.'),
 ('Historical scope','The references and graph concern 1970. Historical MBD/hyperkinesis populations do not automatically equal the modern ADHD node. Clinical statements are distinguished from experimental results. No automatic penalty for a 1990 mismatch is applied.'),
 ('Age scope','Schain ages 7-13; Obler approximately 7-12; Wikler initial eligibility 5-15. None studies adult patients aged 45. Family histories mentioning relatives are not adult outcome studies. Childhood age trends are not used to contradict adult severity or impairment claims.'),
 ('Source completeness','Schain, Obler and Geller supplied articles are complete. Brain_function.pdf contains printed pp. 634-643; pp. 644-645 are absent. The preceding article fragment on p. 634 is excluded.'),
 ('Evidence limits','Schain supplies clinical management statements and observational cases. Wikler is cross-sectional and reports drug-free results. Obler tests phobia desensitization, an intervention absent from this graph. Geller is an infant-rat lesion experiment, not human ADHD evidence.'),
 ('Status standard','Only the six status_definitions values are allowed. Contextual associations become insufficient_evidence; undefined categorical signs/endpoints become not_assessable; clinical or narrower support becomes partially_supported. Contradicted does not imply a proven reversed causal edge.'),
 ('Status counts',json.dumps(counts)),
 ('Evidence format','Each edge has 9 fields. Evidence contains PMID, exact_excerpt, location (PDF/printed page and section), relevance. Shared references provide citations and URLs. Empty evidence means no directly relevant passage found; no missing evidence is invented.'),
 ('Excerpt transcription','Line wrapping and end-of-line hyphenation normalized; quotations from the four supplied PDFs, with page locations. No title-only excerpts used as causal evidence.'),
 ('Original preservation','Neither original graph modified. Original 1970 SHA-256: '+original_hash),
 ('Source isolation','Only the four PDFs copied into this age folder are used. No additional bibliography records or adult studies were introduced. Earlier validation folders are untouched.'),
 ('Reproduce','Run python validation_1970_age45/build_report.py. The reviewed judgments are stored in fulltext_review.py and checked against the actual 1970 source on every run.')
]
metadata = dict(manifest, original_unchanged=True,strength_assessed=False,status_counts=counts)
result = {'metadata':metadata,'status_definitions':definitions,'methodology':dict(methods),'edges':rows,'references':refs}
outputs = ['manifest.json','original_edges.json','edge_validation.json','edge_validation.xlsx','README.md','verification.json','full_text_review.json','supplied_papers.json']
# Separate age-specific outputs are created on the first run and overwritten on subsequent runs.
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'original_edges.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'edge_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'supplied_papers.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'graph':'1970_45 yo.py','edge_count':37,'updated_utc':now,'status_counts':counts,'partial_support_edges':[],'contradicted_edges':[],'documents':REVIEW['documents'],'complete_articles':3,'incomplete_articles':1}
(BASE/'full_text_review.json').write_text(json.dumps({'summary':summary,'excerpts':REVIEW['excerpts']},ensure_ascii=False,indent=2),encoding='utf-8')
def col(n):
    s=''
    while n:
        n,r=divmod(n-1,26); s=chr(65+r)+s
    return s

def sheet_xml(data, widths):
    ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    root=ET.Element('worksheet',xmlns=ns)
    views=ET.SubElement(root,'sheetViews'); view=ET.SubElement(views,'sheetView',workbookViewId='0')
    ET.SubElement(view,'pane',ySplit='1',topLeftCell='A2',activePane='bottomLeft',state='frozen')
    cols=ET.SubElement(root,'cols')
    for i,w in enumerate(widths,1): ET.SubElement(cols,'col',min=str(i),max=str(i),width=str(w),customWidth='1')
    sd=ET.SubElement(root,'sheetData')
    for i,row in enumerate(data,1):
        r=ET.SubElement(sd,'row',r=str(i),ht='30' if i==1 else '110',customHeight='1')
        for j,value in enumerate(row,1):
            c=ET.SubElement(r,'c',r=f'{col(j)}{i}',t='inlineStr',s='1' if i==1 else '0')
            t=ET.SubElement(ET.SubElement(c,'is'),'t',{'{http://www.w3.org/XML/1998/namespace}space':'preserve'})
            t.text=str(value) if value is not None else ''
    ET.SubElement(root,'autoFilter',ref=f'A1:{col(len(data[0]))}{len(data)}')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)


edge_header=['Edge ID','Source','Dest','Existing reasoning','Sign','Validation status','Observation from validation','Recommended action','Evidence (PMID, exact excerpt, location, relevance)']
edge_data=[edge_header]
for r in rows:
    edge_data.append([r[k] for k in ['edge_id','source','dest','existing_reasoning','sign','validation_status','observation_from_validation','recommended_action']]+['\n\n'.join(f"PMID {e['pmid']}: {e['exact_excerpt']}\nLocation: {e['location']}\nRelevance: {e['relevance']}" for e in r['evidence']) or 'No directly relevant excerpt available'])
ref_data=[['PMID','Citation','URL','DOI','Local PDF','Scope']]+[[r.get(k) for k in ['pmid','citation','url','doi','local_pdf','evidence_scope']] for r in refs]
excerpt_data=[['Excerpt ID','PMID','Exact excerpt','Location','Interpretation']]+[[q[k] for k in ['id','pmid','exact_excerpt','location','interpretation']] for q in REVIEW['excerpts']]
sheets=[('Edge validation',edge_data,[10,28,28,65,9,30,90,75,100]),('References',ref_data,[15,85,50,40,45,95]),('Content excerpts',excerpt_data,[25,15,90,70,90]),('Read me',[['Item','Explanation']]+methods+[('Status: '+k,v) for k,v in definitions.items()],[25,145])]
with zipfile.ZipFile(BASE/'edge_validation.xlsx','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'+''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,len(sheets)+1))+'</Types>')
    z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    z.writestr('xl/workbook.xml','<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+''.join(f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>' for i,(name,_,_) in enumerate(sheets,1))+'</sheets></workbook>')
    z.writestr('xl/_rels/workbook.xml.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1))+'<Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
    z.writestr('xl/styles.xml','<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF24476A"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    for i,(_,data,widths) in enumerate(sheets,1): z.writestr(f'xl/worksheets/sheet{i}.xml',sheet_xml(data,widths))

with zipfile.ZipFile(BASE/'edge_validation.xlsx') as z:
    assert z.testzip() is None
    for name in z.namelist(): ET.fromstring(z.read(name))
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    xml_rows=sheet.findall('m:sheetData/m:row',ns)
    assert len(xml_rows)==38
    for row,r in zip(xml_rows[1:],rows):
        values=[''.join(c.itertext()) for c in row]
        assert values[1:6]==[r['source'],r['dest'],r['existing_reasoning'],r['sign'],r['validation_status']]
assert hashlib.sha256(GRAPH.read_bytes()).hexdigest()==original_hash
assert hashlib.sha256(GRAPH_1990.read_bytes()).hexdigest()==before_1990
readme='# 1970 age-45 graph validation\n\nExisting reports replaced using the correct **1970_45 yo.py** graph: **37 edges**, **four supplied references only**.\n\n'
readme+='## Status counts\n\n'+''.join(f'- `{s}`: {n}\n' for s,n in counts.items())
readme+='\n## Method and limitations\n\n'+'\n\n'.join('**'+k+'**: '+v for k,v in methods)
readme+='\n\n## Fixed status definitions\n\n'+''.join(f'- `{k}`: {v}\n' for k,v in definitions.items())
(BASE/'README.md').write_text(readme,encoding='utf-8')
checks={'graph':'1970_45 yo.py','edges_reviewed':37,'references_reviewed':4,'status_counts':counts,'original_sha256':original_hash,'original_unchanged':True,'graph_1990_unchanged':True,'all_edge_reasons_and_signs_preserved':True,'xlsx_xml_valid':True,'xlsx_json_rows_match':True,'xlsx_data_rows':37,'all_citations_in_four_paper_corpus':True,'compact_edge_fields':list(rows[0])}
(BASE/'verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
