"""Artifact integrity and age-scope guards for the 2026 evidence review."""
from pathlib import Path
import importlib.util
import json
import re
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

import validation_2026_utils as validation

ROOT = Path(__file__).resolve().parent.parent


class Validation2026Tests(unittest.TestCase):
    def test_every_original_edge_and_node_survives_in_standalone_graph(self):
        for age, count in [(8,68),(32,74),(45,70)]:
            with self.subTest(age=age):
                folder = ROOT / f'validation_2026_age{age}'
                ledger, reviewed = validation.load_review(age)
                report = json.loads((folder/'edge_validation.json').read_text())
                graph = (folder/'validated_graph.html').read_text()
                spec = importlib.util.spec_from_file_location(f'graph_{age}', folder/'build_validated_graph.py')
                builder = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(builder)
                original = builder.capture_graph()
                nodes = json.loads(re.search(r'nodes = new vis.DataSet\((\[.*?\])\);', graph, re.S)[1])
                edges = json.loads(re.search(r'edges = new vis.DataSet\((\[.*?\])\);', graph, re.S)[1])
                evidence = json.loads(re.search(r'const validationEvidence = (\{.*?\});\n', graph, re.S)[1])
                self.assertEqual(report['edges'],reviewed['edges'])
                self.assertEqual(len(edges),count)
                self.assertEqual(len(evidence),count)
                self.assertEqual({n['id'] for n in nodes},{n['id'] for n in original.nodes})
                by_node = {n['id']:n for n in nodes}
                for node in original.nodes:
                    for key,value in node.items():
                        self.assertEqual(by_node[node['id']][key],value)
                for before,after,decision in zip(original.edges,edges,report['edges']):
                    self.assertEqual((after['from'],after['to']),(decision['source'],decision['dest']))
                    for key in before.keys()-{'id','color','dashes','title'}:
                        self.assertEqual(before[key],after[key])
                    self.assertTrue(after['title'].startswith(before['title']))
                    style = builder.STATUS_STYLES[decision['validation_status']]
                    self.assertEqual((after['color'],after['dashes']),(style['color'],style['dashes']))
                self.assertIn('unvalidated original strengths',graph)
                self.assertFalse(report['metadata']['strength_assessed'])

    def test_every_pdf_link_and_quotation_has_valid_source_and_page(self):
        for age in (8,32,45):
            folder = ROOT / f'validation_2026_age{age}'
            report = json.loads((folder/'edge_validation.json').read_text())
            refs = {ref['source_id']:ref for ref in report['references']}
            corpus = {r['source_id']:r for r in json.loads((ROOT/'paper_reviews/2026/extracted_papers.json').read_text())}
            for row in report['edges']:
                for evidence in row['evidence']:
                    source = refs[evidence['source_id']]
                    path = (folder/source['local_pdf']).resolve()
                    self.assertTrue(path.is_file())
                    self.assertEqual(path.parent,ROOT/'2026 ADHD Papers')
                    self.assertEqual(validation.sha(path),source['sha256'])
                    page = int(re.search(r'PDF page (\d+)',evidence['location'])[1])
                    self.assertIn(evidence['exact_excerpt'],corpus[evidence['source_id']]['pages'][page-1])
            graph = (folder/'validated_graph.html').read_text()
            payload = json.loads(re.search(r'const validationEvidence = (\{.*?\});\n',graph,re.S)[1])
            for item in payload.values():
                for evidence in item['evidence']:
                    url = urlsplit(evidence['local_file'])
                    self.assertTrue((folder/unquote(url.path)).is_file())
                    self.assertRegex(url.fragment,r'^page=\d+$')

    def test_duplicate_is_counted_once_and_not_used_as_independent_evidence(self):
        ledger,_ = validation.load_review(8)
        corpus = json.loads((ROOT/'paper_reviews/2026/extracted_papers.json').read_text())
        self.assertEqual(len(corpus),159)
        self.assertEqual(sum(r['page_count'] for r in corpus),2212)
        duplicates = {r['source_id'] for r in corpus if r['duplicate_of']}
        self.assertEqual(duplicates,{'PDF_037'})
        self.assertEqual(len({r['text_sha256'] for r in corpus}),158)
        self.assertFalse(duplicates & {e['source_id'] for e in ledger['excerpts'].values()})

    def test_adult_digital_and_remote_work_effects_are_not_inferred_from_child_studies(self):
        for age in (32,45):
            _,review = validation.load_review(age)
            rows = {(r['source'],r['dest']):r for r in review['edges']}
            for source,dest in [('Digital Therapeutics','Symptom Severity'),('Remote Work Flexibility','Functional Impairment'),('Telehealth Treatment','Treatment Access')]:
                self.assertEqual(rows[(source,dest)]['validation_status'],'insufficient_evidence')
            self.assertEqual(rows[('Treatment Adherence','Medication Treatment')]['validation_status'],'not_assessable')
            self.assertEqual(rows[('Diagnosis Status','Quality of Life')]['validation_status'],'insufficient_evidence')

    def test_changed_inputs_require_reassessment(self):
        real_check = validation.text_hash_matches
        with patch.object(validation,'text_hash_matches',side_effect=lambda path, expected: False if Path(path).name=='2026_8 yo.py' else real_check(path, expected)):
            with self.assertRaisesRegex(ValueError,'Graph changed'):
                validation.load_review(8)
        with patch.object(validation,'text_hash_matches',return_value=False):
            with self.assertRaisesRegex(ValueError,'Extracted corpus changed'):
                validation.load_review(8)


if __name__ == '__main__':
    unittest.main()
