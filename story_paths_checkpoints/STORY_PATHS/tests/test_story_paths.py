import unittest

from story_paths import discover_stories, highlight_path, shortest_routes, story_paragraph


def snapshot(edges):
    return {'nodes': [{'id': n} for n in 'ABCDE'],
            'edges': [{'from': a, 'to': b, 'color': 'green'} for a, b in edges]}


class StoryPathsTests(unittest.TestCase):
    def test_narrative_uses_original_explanation_and_historical_peers(self):
        old = snapshot([('A', 'B'), ('B', 'D')])
        new = snapshot([('A', 'C'), ('C', 'D')])
        old.update(year=1990, age=8)
        new.update(year=2026, age=8)
        old['edges'][0]['title'] = 'Effect: Negative\nWhy: A can reduce B.\nStrength: 0.5'
        paragraph = story_paragraph(discover_stories(old, new)[0], old, new, 5)
        self.assertIn('a child aged 8', paragraph)
        self.assertIn('A can reduce B', paragraph)
        self.assertIn('1990', paragraph)
        self.assertIn('2026', paragraph)
        self.assertNotIn('antagonist', paragraph)
        self.assertNotIn('turning point', paragraph)
        self.assertNotIn('Imagine', paragraph)

    def test_direction_cycles_and_cutoff(self):
        graph = snapshot([('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'D')])
        routes = shortest_routes(graph, 2)
        self.assertEqual(routes['A', 'C'], ('A', 'B', 'C'))
        self.assertNotIn(('A', 'D'), routes)
        self.assertNotIn(('C', 'A'), routes)

    def test_changed_route_and_unchanged_graph(self):
        old = snapshot([('A', 'B'), ('B', 'D')])
        new = snapshot([('A', 'C'), ('C', 'D')])
        story = discover_stories(old, new)[0]
        self.assertEqual(story['kind'], 'Changed route')
        self.assertEqual(story['earlier'], ('A', 'B', 'D'))
        self.assertEqual(story['later'], ('A', 'C', 'D'))
        self.assertEqual(discover_stories(old, old), [])

    def test_new_bounded_route(self):
        old = snapshot([])
        new = snapshot([('A', 'B'), ('B', 'D')])
        self.assertEqual(discover_stories(old, new)[0]['kind'], 'New bounded route')

    def test_highlighting_preserves_source_and_evidence_color(self):
        original = snapshot([('A', 'B'), ('B', 'C')])
        highlighted = highlight_path(original, ('A', 'B'))
        self.assertEqual(highlighted['edges'][0]['color'], 'green')
        self.assertEqual(highlighted['edges'][0]['width'], 5)
        self.assertNotIn('width', original['edges'][0])


if __name__ == '__main__':
    unittest.main()
