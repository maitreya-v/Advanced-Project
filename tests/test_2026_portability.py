"""Exercise 2026 evidence links in a directory tree without symlinks or junctions."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

import validation_2026_utils as validation

ROOT = Path(__file__).resolve().parents[1]


class Validation2026PortabilityTests(unittest.TestCase):
    def test_standalone_graphs_and_workbooks_in_fresh_directory_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            shutil.copytree(ROOT / '2026 ADHD Papers', checkout / '2026 ADHD Papers')
            for age, edge_count in ((8, 68), (32, 74), (45, 70)):
                with self.subTest(age=age):
                    source = ROOT / f'validation_2026_age{age}'
                    folder = checkout / source.name
                    folder.mkdir()
                    for name in ('edge_validation.json', 'supplied_papers.json', 'manifest.json',
                                 'edge_validation.xlsx', 'validated_graph.html'):
                        shutil.copyfile(source / name, folder / name)
                    self.assertFalse((folder / 'full_texts').exists())
                    self.assertFalse((source / 'full_texts').exists())
                    report = json.loads((folder / 'edge_validation.json').read_text(encoding='utf-8'))
                    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
                    supplied = json.loads((folder / 'supplied_papers.json').read_text(encoding='utf-8'))
                    self.assertEqual(report['references'], supplied)
                    self.assertEqual(len(report['edges']), edge_count)
                    for ref, document in zip(report['references'], manifest['documents']):
                        self.assertTrue(ref['local_pdf'].startswith('../2026 ADHD Papers/'))
                        self.assertEqual(ref['local_pdf'], document['file'])
                        pdf = (folder / ref['local_pdf']).resolve()
                        self.assertEqual(pdf.parent, checkout / '2026 ADHD Papers')
                        self.assertEqual(hashlib.sha256(pdf.read_bytes()).hexdigest(), ref['sha256'])
                    graph = (folder / 'validated_graph.html').read_text(encoding='utf-8')
                    self.assertNotIn('full_texts/', graph)
                    payload = json.loads(re.search(r'const validationEvidence = (\{.*?\});\n', graph, re.S)[1])
                    self.assertEqual(len(payload), edge_count)
                    for item in payload.values():
                        for evidence in item['evidence']:
                            url = urlsplit(evidence['local_file'])
                            self.assertEqual(url.scheme, '')
                            self.assertTrue(url.path.startswith('../2026%20ADHD%20Papers/'))
                            pdf = folder / unquote(url.path)
                            self.assertTrue(pdf.is_file(), evidence['local_file'])
                            self.assertRegex(url.fragment, r'^page=\d+$')
                    with ZipFile(folder / 'edge_validation.xlsx') as archive:
                        references = archive.read('xl/worksheets/sheet2.xml').decode('utf-8')
                        self.assertNotIn('full_texts/', references)
                        texts = {item.text for item in ET.fromstring(references).iter()
                                 if item.tag.endswith('}t')}
                        for ref in supplied:
                            # XML escapes some filename characters; inspect parsed cells.
                            self.assertIn(ref['local_pdf'], texts)

    def test_checkout_newlines_are_accepted_but_text_changes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'reviewed.py'
            original = 'title = "ADHD → Quality of Life"\nstrength = 0.7\n'.encode('utf-8')
            expected = hashlib.sha256(original).hexdigest()
            source.write_bytes(original.replace(b'\n', b'\r\n'))
            self.assertTrue(validation.text_hash_matches(source, expected))
            source.write_bytes(original.replace(b'0.7', b'0.8'))
            self.assertFalse(validation.text_hash_matches(source, expected))

    def test_source_corpus_hashes_and_selected_pdf_quotations(self):
        ledger, _ = validation.load_review(8)
        self.assertEqual(len(validation.verify_corpus(ledger)), 159)
        for age in (8, 32, 45):
            _, review = validation.load_review(age)
            report = json.loads((ROOT / f'validation_2026_age{age}' / 'edge_validation.json').read_text(encoding='utf-8'))
            self.assertEqual(report['edges'], review['edges'])


if __name__ == '__main__':
    unittest.main()
