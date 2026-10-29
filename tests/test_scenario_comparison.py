"""Scenario comparisons are directional, complete and independent of route filters."""
from copy import deepcopy

from storytelling.data import load_snapshots
from storytelling.scenario_comparison import compare_scenarios


def snapshot(year, age, nodes, edges):
    return {'year': year, 'age': age, 'fingerprint': f'{year}-{age}',
            'nodes': [{'id': node} for node in nodes],
            'edges': [{'id': str(index), 'from': a, 'to': b, 'sign': sign, 'strength': strength}
                      for index, (a, b, sign, strength) in enumerate(edges)]}


def test_simultaneous_sign_and_strength_changes_reversals_and_isolated_nodes():
    a = snapshot(2026, 45, ['X', 'Y', 'Old isolated'], [('X', 'Y', '+', .7), ('Y', 'X', '-', .2)])
    b = snapshot(1970, 8, ['X', 'Y', 'New isolated'], [('X', 'Y', '-', .4), ('Y', 'New isolated', '+', .8)])
    original = deepcopy((a, b))
    changes = compare_scenarios(a, b)
    assert changes['added_nodes'] == ['New isolated']
    assert changes['removed_nodes'] == ['Old isolated']
    assert [(row['source'], row['target']) for row in changes['added_edges']] == [('Y', 'New isolated')]
    assert [(row['source'], row['target']) for row in changes['removed_edges']] == [('Y', 'X')]
    assert changes['sign_changes'] == changes['strength_changes']
    assert changes['sign_changes'][0] == {'source': 'X', 'target': 'Y', 'sign_a': '+', 'sign_b': '-',
                                         'strength_a': .7, 'strength_b': .4, 'delta': -.3}
    assert (a, b) == original
    reverse = compare_scenarios(b, a)
    assert reverse['strength_changes'][0]['delta'] == .3
    assert reverse['added_nodes'] == changes['removed_nodes']
    assert reverse['removed_nodes'] == changes['added_nodes']
    same = compare_scenarios(a, a)
    assert len(same['unchanged_edges']) == 2
    assert not any(same[key] for key in ('added_nodes', 'removed_nodes', 'added_edges', 'removed_edges', 'sign_changes', 'strength_changes'))


def test_reversed_direction_is_a_removal_and_an_addition_and_small_roundoff_is_unchanged():
    a = snapshot(1970, 8, ['X', 'Y', 'Z'], [('X', 'Y', '+', .5), ('Y', 'Z', '+', .2)])
    b = snapshot(2026, 32, ['X', 'Y', 'Z'], [('Y', 'X', '+', .5), ('Y', 'Z', '+', .20000000001)])
    changes = compare_scenarios(a, b)
    assert changes['added_edges'][0]['source'] == 'Y'
    assert changes['removed_edges'][0]['source'] == 'X'
    assert changes['unchanged_edges'][0]['source'] == 'Y'
    assert not changes['strength_changes']


def test_all_144_real_scenario_pairs_allow_arbitrary_year_age_combinations():
    snapshots = [item for ages in load_snapshots().values() for item in ages.values()]
    assert len(snapshots) == 12
    for a in snapshots:
        for b in snapshots:
            changes = compare_scenarios(a, b)
            added, removed = len(changes['added_edges']), len(changes['removed_edges'])
            assert len(a['edges']) - removed + added == len(b['edges'])
            assert len(a['nodes']) - len(changes['removed_nodes']) + len(changes['added_nodes']) == len(b['nodes'])
            changed = {(row['source'], row['target']) for key in ('sign_changes', 'strength_changes') for row in changes[key]}
            assert len(a['edges']) - removed == len(changed) + len(changes['unchanged_edges'])
