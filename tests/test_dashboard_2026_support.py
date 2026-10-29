"""Check imported 2026 evidence and exercise it in the combined dashboard."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import dashboard_corpus
import dashboard_validation
from streamlit.testing.v1 import AppTest
from test_dashboard_validation import dashboard_functions

ROOT = Path(__file__).resolve().parents[1]


class Dashboard2026Tests(unittest.TestCase):
    def test_all_212_edges_match_source_layout_and_standalone_validation(self):
        functions = dashboard_functions()
        for age, count in ((8, 68), (32, 74), (45, 70)):
            with self.subTest(age=age):
                original = functions["load_snapshot_from_script"](ROOT / f"2026_{age} yo.py")
                validated = dashboard_validation.attach_validation(original)
                self.assertEqual(original["nodes"], validated["nodes"])
                self.assertEqual(len(validated["edges"]), count)
                graph = (ROOT / f"validation_2026_age{age}/validated_graph.html").read_text(encoding="utf-8")
                saved = json.loads(re.search(r"edges = new vis.DataSet\((\[.*?\])\);", graph, re.S)[1])
                for before, after, standalone in zip(original["edges"], validated["edges"], saved):
                    for key in before.keys() - {"id", "color", "dashes", "title"}:
                        self.assertEqual(before[key], after[key])
                    self.assertEqual((after["color"], after["dashes"]), (standalone["color"], standalone["dashes"]))
                # Rendering keeps the fuzzy regions and click bridge at a nonzero filter.
                rendered = functions["build_network_html"](validated, 0.7, 600)
                self.assertIn('network.on("beforeDrawing"', rendered)
                self.assertIn("dashboard-validation-edge", rendered)

    def test_every_reference_matches_its_recorded_pdf_hash(self):
        checked = set()
        for age in (8, 32, 45):
            folder = ROOT / f"validation_2026_age{age}"
            report = json.loads((folder / "edge_validation.json").read_text(encoding="utf-8"))
            references = {ref["source_id"]: ref for ref in report["references"]}
            for ref in references.values():
                path = (folder / ref["local_pdf"]).resolve()
                path.relative_to(ROOT)
                if path not in checked:
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), ref["sha256"])
                    checked.add(path)
            for decision in report["edges"]:
                for evidence in decision["evidence"]:
                    self.assertIn(evidence["source_id"], references)
        self.assertEqual(len(checked), 159)
        counts = dashboard_corpus.corpus_counts(2026)
        self.assertEqual(counts["reviewed_pdf"], 158)
        self.assertEqual(counts["reviewed"], 158)

    def test_2026_edge_click_opens_validation_with_page_linked_pdf_for_each_age(self):
        with patch.object(dashboard_validation, "graph_component", return_value={"edge_id": "validation-edge-1", "sequence": 1}), \
             patch.object(dashboard_validation, "popup_component", return_value={"reference_index": 0}) as popup:
            app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=60).run()
            app.select_slider[0].set_value(2026).run()
            for age in (8, 32, 45):
                with self.subTest(age=age):
                    app.select_slider[1].set_value(age).run()
                    self.assertFalse(app.exception, [error.message for error in app.exception])
                    self.assertEqual(app.session_state["snapshot_tabs"], "Validation")
                    payload = popup.call_args.kwargs["payload"]
                    self.assertEqual((payload["year"], payload["age"]), (2026, age))
                    self.assertEqual(payload["edge_title"], "Genetic Risk → ADHD")
                    self.assertTrue(payload["evidence"])
                    self.assertRegex(payload["evidence"][0]["pdf_url"], r"^references/[a-f0-9]{64}\.pdf#page=\d+$")


if __name__ == "__main__":
    unittest.main()
