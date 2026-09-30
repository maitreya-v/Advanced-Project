"""Verify workbook totals, mutually exclusive access counts and paper deduplication."""
import unittest
from dashboard_corpus import corpus_counts


class CorpusTests(unittest.TestCase):
    def test_workbook_counts_and_validation_usage(self):
        expected = {
            1970: (13, 5, 0, 0, 0, 4, 4, 0),
            1990: (200, 35, 32, 0, 32, 29, 4, 25),
            2010: (1294, 56, 54, 12, 42, 39, 24, 15),
            2026: (1339, 183, 183, 85, 98, None, 0, 0),
        }
        keys = ('total', 'selected', 'accessible', 'full_text', 'abstract_only', 'reviewed', 'reviewed_pdf', 'reviewed_abstract')
        for year, values in expected.items():
            with self.subTest(year=year):
                counts = corpus_counts(year)
                self.assertEqual(tuple(counts[key] for key in keys), values)
                self.assertEqual(counts['accessible'], counts['full_text'] + counts['abstract_only'])
                if counts['reviewed'] is not None:
                    self.assertEqual(counts['reviewed'], counts['reviewed_pdf'] + counts['reviewed_abstract'])

    def test_unlisted_year_is_not_zero_papers(self):
        self.assertIsNone(corpus_counts(2000))
