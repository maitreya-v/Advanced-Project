"""Integration checks for validated snapshots and the dashboard selection flow."""
from pathlib import Path
from unittest.mock import patch
import ast
import json
import re
import unittest

import dashboard_validation
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent


def dashboard_functions():
    """Load the graph loader/renderer without running the dashboard UI."""
    tree = ast.parse((ROOT / "Dashboard.py").read_text())
    definitions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    namespace = {}
    exec("from pathlib import Path\nimport re, html, base64, time\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport streamlit as st\nfrom pyvis.network import Network\nfrom dashboard_validation import inject_edge_selection", namespace)
    namespace.update(BASE_DIR=ROOT, HELPER_NODE_IDS={"LEGEND_NODE", "PERSONA_DESC", "PERIOD_NODE", "Persona", "PERSONA_NODE"})
    exec(compile(ast.Module(body=definitions, type_ignores=[]), "Dashboard.py", "exec"), namespace)
    return namespace


class DashboardValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.functions = dashboard_functions()

    def test_all_validated_snapshots_preserve_layout_and_match_standalone_styles(self):
        for year in [1970, 1990, 2010]:
            for age in [8, 32, 45]:
                with self.subTest(year=year, age=age):
                    original = self.functions["load_snapshot_from_script"](ROOT / f"{year}_{age} yo.py")
                    snapshot = dashboard_validation.attach_validation(original)
                    self.assertEqual(snapshot["nodes"], original["nodes"])
                    for key in original.keys() - {"edges"}:
                        self.assertEqual(snapshot[key], original[key])
                    graph = (ROOT / f"validation_{year}_age{age}/validated_graph.html").read_text(encoding="utf-8")
                    standalone = json.loads(re.search(r"edges = new vis.DataSet\((\[.*?\])\);", graph, re.S).group(1))
                    self.assertEqual(len(snapshot["edges"]), len(standalone))
                    for source, annotated, saved in zip(original["edges"], snapshot["edges"], standalone):
                        self.assertEqual(annotated["color"], saved["color"])
                        self.assertEqual(annotated["dashes"], saved["dashes"])
                        for key in source.keys() - {"id", "color", "dashes", "title"}:
                            self.assertEqual(annotated[key], source[key])
                        self.assertTrue(annotated["title"].startswith(source.get("title", "")))

    def test_strength_filter_and_background_survive_validation(self):
        original = self.functions["load_snapshot_from_script"](ROOT / "2010_8 yo.py")
        snapshot = dashboard_validation.attach_validation(original)
        expected = [(edge["from"], edge["to"]) for edge in original["edges"]
                    if self.functions["extract_strength_from_title"](edge.get("title", "")) >= 0.7]
        rendered = self.functions["build_network_html"](snapshot, 0.7, 600)
        edges = json.loads(re.search(r"edges = new vis.DataSet\((\[.*?\])\);", rendered, re.S).group(1))
        self.assertEqual([(edge["from"], edge["to"]) for edge in edges], expected)
        self.assertIn('network.on("beforeDrawing"', rendered)
        self.assertIn("dashboard-validation-edge", rendered)
        self.assertEqual(rendered, self.functions["build_network_html"](snapshot, 0.7, 600))

    def test_2026_snapshots_remain_unannotated(self):
        for age in [8, 32, 45]:
            snapshot = self.functions["load_snapshot_from_script"](ROOT / f"2026_{age} yo.py")
            self.assertIs(dashboard_validation.attach_validation(snapshot), snapshot)
            self.assertNotIn("validation", snapshot)

    def test_dashboard_renders_every_year_and_age(self):
        app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=60).run()
        for year in [1970, 1990, 2010, 2026]:
            app.select_slider[0].set_value(year).run()
            for age in [8, 32, 45]:
                with self.subTest(year=year, age=age):
                    app.select_slider[1].set_value(age).run()
                    self.assertFalse(app.exception, [item.message for item in app.exception])
                    self.assertEqual([tab.label for tab in app.tabs], ["Snapshot explorer", "Info", "Edges", "Groups", "Legend", "Validation", "Story paths"])

    def test_edge_selection_opens_panel_and_allows_other_tabs(self):
        selection = {"edge_id": "validation-edge-40", "sequence": 1}
        with patch.object(dashboard_validation, "graph_component", return_value=selection), \
             patch.object(dashboard_validation, "popup_component", return_value={"reference_index": 0}) as popup:
            app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=60).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state["snapshot_tabs"], "Validation")
            payload = popup.call_args.kwargs["payload"]
            self.assertEqual(payload["edge_title"], "Medication Treatment → Symptom Severity")
            self.assertTrue(payload["evidence"])
            self.assertEqual(len(app.get("download_button")), 0)
            self.assertRegex(payload["evidence"][0]["pdf_url"], r"^references/[a-f0-9]{64}\.pdf#page=\d+$")
            app.session_state["snapshot_tabs"] = "Info"
            popup.reset_mock()
            app.run()
            self.assertEqual(app.session_state["snapshot_tabs"], "Info")
            popup.assert_not_called()
            selection.update(edge_id="validation-edge-1", sequence=2)
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state["snapshot_tabs"], "Validation")
            self.assertEqual(popup.call_args.kwargs["payload"]["edge_title"], "Genetic Risk → ADHD")
            popup.return_value = {"closed": True}
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state["snapshot_tabs"], "Info")
            self.assertEqual(app.session_state["validation_panel_generation"], 1)
            popup.return_value = None
            app.session_state["snapshot_tabs"] = "Validation"
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state["snapshot_tabs"], "Validation")


if __name__ == "__main__":
    unittest.main()
