"""Parse saved PubMed abstracts and apply explicitly reviewed edge updates."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent


class PubMedParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.metadata = {}
        self.abstract_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        active = (self.stack[-1][1] if self.stack else False) or self.is_abstract(attrs)
        if tag == 'meta' and attrs.get('name', '').startswith('citation_'):
            self.metadata[attrs['name']] = attrs.get('content', '')
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, active))

    def is_abstract(self, attrs):
        return attrs.get('id') == 'eng-abstract'

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][1] and data.strip():
            self.abstract_parts.append(data.strip())


class PublisherParser(PubMedParser):
    def is_abstract(self, attrs):
        return bool({'abstract', 'c-ckc-abstract'} & set(attrs.get('class', '').split()))


def publisher_record(path, year):
    parser = PublisherParser()
    raw = path.read_text(encoding='utf-8-sig')
    parser.feed(raw)
    abstract = ' '.join(' '.join(parser.abstract_parts).split())
    if path.name.startswith('Bipolar Symptoms'):
        abstract = abstract.removeprefix('Article Abstract ').split(' Submitted:', 1)[0]
        assert 'content="20100115"' in raw
        title = 'Bipolar Symptoms in Adult Attention-Deficit/Hyperactivity Disorder: A Cross-Sectional Study of 510 Clinically Diagnosed Patients and 417 Population-Based Controls'
        source_id = 'BIPOLAR_ADULT'
        authors = 'Ole Bernt Fasmer; Anne Halmøy; Helene Halleland; Margaretha Dramsdahl; Per Bergsholm; Jan Haavik'
        date, journal, doi = '2010-01-15', 'J Clin Psychiatry 71(1):48–57', '10.4088/JCP.08m04722ora'
        url = 'https://www.psychiatrist.com/jcp/bipolar-symptoms-adult-attention-deficit-hyperactivity/'
        fragment = 'article-tabs'
        note = 'Publisher abstract only; full text is gated. Visible article date and journal citation are 2010; exported citation text contains conflicting 2024 website metadata and is not used as publication year. Encoding artifacts in the saved abstract are preserved.'
    elif path.name.endswith('ClinicalKey.html'):
        abstract = abstract.removeprefix('Abstract ')
        assert 'Copyright © 2010 Elsevier Ireland Ltd' in raw
        title = 'Quantitative MR analysis of caudate abnormalities in pediatric ADHD: Proposal for a diagnostic test'
        source_id = 'CAUDATE_HTML'
        authors = 'Joan Carles Soliva; Jordi Fauquet; Anna Bielsa; Mariana Rovira; Susanna Carmona; Josep Antoni Ramos-Quiroga; Joseph Hilferty; Antoni Bulbena; Miquel Casas; Oscar Vilarroya'
        date, journal, doi = '2010-06-30', 'Psychiatry Research: Neuroimaging 182(3):238–243', '10.1016/j.pscychresns.2010.01.013'
        url = 'https://doi.org/' + doi
        fragment = 'hl0000502'
        note = 'Publisher abstract extracted; full article is also present in the saved HTML. Same study as the supplied CAUDATE_MRI PDF, not independent additional evidence.'
    else:
        raise ValueError(f'Unsupported publisher HTML: {path.name}')
    assert year == 2010 and abstract
    return {'source_id': source_id, 'pmid': None, 'title': title, 'authors': authors,
            'publication_date': date, 'publication_year': year, 'journal': journal,
            'url': url, 'doi': doi, 'file': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'abstract': abstract, 'abstract_available': True, 'abstract_truncated': False,
            'abstract_fragment': fragment, 'duplicate_of': None, 'evidence_scope': note}


def parse_corpus(year=1990):
    records = []
    seen = {}
    for path in sorted((ROOT / f'{year} ADHD Papers').glob('*.html')):
        parser = PubMedParser()
        parser.feed(path.read_text(encoding='utf-8-sig'))
        meta = parser.metadata
        if not meta.get('citation_pmid'):
            records.append(publisher_record(path, year))
            continue
        date = meta.get('citation_date', '')
        match = re.search(r'\b(\d{4})\b', date)
        if not match or int(match.group(1)) != year:
            raise ValueError(f'Publication year does not match {year}: {path.name}: {date}')
        pmid = meta['citation_pmid']
        abstract = ' '.join(' '.join(parser.abstract_parts).split())
        record = {
            'source_id': f'PMID_{pmid}', 'pmid': pmid,
            'title': meta['citation_title'], 'authors': meta.get('citation_authors', ''),
            'publication_date': date, 'publication_year': year,
            'journal': meta.get('citation_journal_title', ''),
            'url': meta.get('citation_abstract_html_url') or f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',
            'doi': meta.get('citation_doi', ''),
            'file': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'abstract': abstract, 'abstract_available': bool(abstract),
            'abstract_truncated': 'ABSTRACT TRUNCATED' in abstract,
            'abstract_fragment': 'eng-abstract',
            'duplicate_of': seen.get(pmid),
            'evidence_scope': 'Saved PubMed abstract only; the full article was not supplied as HTML. Study details and exact-age effects not reported in the abstract remain unverified.',
        }
        seen.setdefault(pmid, record['file'])
        records.append(record)
    if year == 2010:
        same_studies = {'PMID_20410711': 'AGE_SEX', 'CAUDATE_HTML': 'CAUDATE_MRI'}
        for record in records:
            record['same_study_as_pdf_source_id'] = same_studies.get(record['source_id'])
    return records


def html_references(records):
    return [{
        'source_id': record['source_id'], 'title': record['title'],
        'citation': f"{record['authors']} {record['title']}. {record['journal']}. {record['publication_date']}." + (f" PMID {record['pmid']}." if record['pmid'] else ''),
        'url': record['url'], 'doi': record['doi'],
        'abstract_fragment': record.get('abstract_fragment', 'eng-abstract'),
        'local_html': '../' + record['file'],
        'sha256': record['sha256'], 'evidence_scope': record['evidence_scope'],
    } for record in records if not record['duplicate_of']]


def apply_html_review(rows, age, excerpts, year=1990):
    review = json.loads((ROOT / f'paper_reviews/{year}/review_updates.json').read_text())
    records = {record['source_id']: record for record in parse_corpus(year)}
    assert {key: value['sha256'] for key, value in records.items()} == review['source_hashes'], 'HTML corpus changed: review new evidence before rebuilding.'
    for update in review['ages'][str(age)]:
        row = rows[update['edge_id'] - 1]
        assert (row['source'], row['dest'], row['sign'], row['existing_reasoning']) == tuple(update[key] for key in ['source', 'dest', 'sign', 'existing_reasoning']), 'Graph claim changed: reassess before rebuilding.'
        for item in update['evidence']:
            assert item['exact_excerpt'] in records[item['source_id']]['abstract'], 'Excerpt does not match saved abstract.'
            excerpts[f"html_{age}_{row['edge_id']}_{len(excerpts)}"] = item
        row.update({key: update[key] for key in ['validation_status', 'observation_from_validation', 'recommended_action']})
        row['evidence'].extend(update['evidence'])
    return rows
