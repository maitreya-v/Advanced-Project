"""Check the separate compact dashboard and its validation selection lifecycle."""
from pathlib import Path
import unittest
from unittest.mock import patch

import dashboard_validation
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class DashboardV2Tests(unittest.TestCase):
    def test_all_year_age_snapshots_and_strength_filter(self):
        app = AppTest.from_file(str(ROOT / 'Dashboard_2_0.py'), default_timeout=60).run()
        self.assertFalse(app.exception, [e.message for e in app.exception])
        for year in (1970, 1990, 2010, 2026):
            app.select_slider(key='v2_year').set_value(year).run()
            for age in (8, 32, 45):
                with self.subTest(year=year, age=age):
                    app.select_slider(key='v2_age').set_value(age).run()
                    self.assertFalse(app.exception, [e.message for e in app.exception])
                    self.assertEqual([tab.label for tab in app.tabs], ['Info', 'Edges', 'Groups', 'Legend', 'Validation'])
                    self.assertIsNone(app.session_state['v2_selected_edge'])
        app.slider(key='v2_strength').set_value(1.0).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state['v2_context'], (2026, 45, 1.0))

    def test_click_tabs_close_and_snapshot_change(self):
        selection = {'edge_id': 'validation-edge-1', 'sequence': 1}
        with patch.object(dashboard_validation, 'graph_component', return_value=selection), \
             patch.object(dashboard_validation, 'popup_component', return_value={'reference_index': 0}) as popup:
            app = AppTest.from_file(str(ROOT / 'Dashboard_2_0.py'), default_timeout=60).run()
            self.assertFalse(app.exception, [e.message for e in app.exception])
            self.assertEqual(app.session_state['snapshot_tabs'], 'Validation')
            self.assertTrue(popup.call_args.kwargs['payload']['evidence'])
            app.session_state['snapshot_tabs'] = 'Legend'
            popup.reset_mock()
            app.run()
            self.assertEqual(app.session_state['snapshot_tabs'], 'Legend')
            popup.assert_not_called()
            selection['sequence'] += 1
            app.run()
            self.assertEqual(app.session_state['snapshot_tabs'], 'Validation')
            popup.return_value = {'closed': True}
            app.run()
            self.assertEqual(app.session_state['snapshot_tabs'], 'Info')
            popup.return_value = None
            app.select_slider(key='v2_year').set_value(2026).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state['snapshot_tabs'], 'Validation')
            self.assertEqual(app.session_state['v2_selected_edge'], 'validation-edge-1')
            self.assertEqual(popup.call_args.kwargs['payload']['year'], 2026)
            # Filter out every edge: stale component events must not reopen a panel.
            with patch.object(dashboard_validation, 'graph_component', return_value=None):
                app.slider(key='v2_strength').set_value(1.0).run()
                self.assertIsNone(app.session_state['v2_selected_edge'])
                self.assertEqual(app.session_state['snapshot_tabs'], 'Info')


if __name__ == '__main__':
    unittest.main()
