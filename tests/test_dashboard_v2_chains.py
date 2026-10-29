"""A/B controls, step focus and evidence scope in the compact dashboard."""
from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

import dashboard_validation
from dashboard_v2_chains import validation_edge_for_step
from storytelling import chain_store, chain_view

ROOT = Path(__file__).resolve().parents[1]


def app():
    return AppTest.from_file(str(ROOT / 'Dashboard_2_0.py'), default_timeout=45)


def route_control(live, side):
    return next(widget for widget in live.selectbox if widget.label == 'Route ' + side)


def event_for(chain, index, event_id):
    return {key: chain[key] for key in ('version', 'scenario', 'chain_id', 'query_id')} | {
        'step_index': index, 'edge_id': chain['steps'][index]['edge_id'], 'event_id': event_id,
    }


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    chains, events = {}, {}

    def render(*, chain, key, **kwargs):
        side = kwargs['label'][-1]
        chains[side] = chain
        return events.get(side)

    component = Mock(side_effect=render)
    graph = Mock(return_value=None)
    popup = Mock(return_value=None)
    monkeypatch.setattr(chain_view, 'chain_component', component)
    monkeypatch.setattr(dashboard_validation, 'graph_component', graph)
    monkeypatch.setattr(dashboard_validation, 'popup_component', popup)
    monkeypatch.setattr(chain_store, 'DEFAULT_DIRECTORY', tmp_path)
    return chains, events, graph, popup


def test_independent_controls_allow_both_axes_reverse_order_and_identical_scenarios(workspace):
    chains, _, _, _ = workspace
    live = app().run()
    assert not live.exception
    live.selectbox(key='v2_chain_year_a').set_value(2026).run()
    live.selectbox(key='v2_chain_age_a').set_value(45).run()
    live.selectbox(key='v2_chain_year_b').set_value(1970).run()
    live.selectbox(key='v2_chain_age_b').set_value(8).run()
    assert not live.exception
    assert (chains['A']['scenario']['year'], chains['A']['scenario']['age']) == (2026, 45)
    assert (chains['B']['scenario']['year'], chains['B']['scenario']['age']) == (1970, 8)
    live.select_slider(key='v2_year').set_value(2010).run()
    live.select_slider(key='v2_age').set_value(32).run()
    assert live.selectbox(key='v2_chain_year_a').value == 2026
    assert live.selectbox(key='v2_chain_age_b').value == 8
    live.selectbox(key='v2_chain_year_b').set_value(2026).run()
    live.selectbox(key='v2_chain_age_b').set_value(45).run()
    live.session_state['snapshot_tabs'] = 'Changes'
    live.run()
    assert not live.exception
    assert all(' (0)' in item.value or '(0)' in item.value for item in live.markdown
               if any(label in item.value for label in ('Added nodes', 'Removed nodes', 'Added edges', 'Removed edges', 'Sign changes', 'Strength changes')))
    assert not live.dataframe


def test_each_side_keeps_its_step_and_validation_toggle_when_focus_changes(workspace):
    chains, events, graph, popup = workspace
    live = app().run()
    a, b = chains['A'], chains['B']
    events['B'] = event_for(b, 1, 'b-1')
    live.run()
    assert not live.exception
    assert live.radio(key='v2_chain_active').value == 'B'
    assert live.session_state['snapshot_tabs'] == 'Story'
    assert any(item.value == b['steps'][1]['reason'] for item in live.markdown)
    live.radio(key='v2_step_detail_mode').set_value('Validation').run()
    payload = popup.call_args.kwargs['payload']
    assert (payload['year'], payload['age']) == (2026, 32)
    assert payload['edge_title'] == f"{b['steps'][1]['source']} → {b['steps'][1]['target']}"
    events['A'] = event_for(a, 2, 'a-1')
    live.run()
    assert not live.exception
    assert live.radio(key='v2_chain_active').value == 'A'
    assert live.session_state['snapshot_tabs'] == 'Validation'
    assert (popup.call_args.kwargs['payload']['year'], popup.call_args.kwargs['payload']['age']) == (1970, 8)
    assert live.session_state['v2_chain_selection_b_step'] == 1
    graph.return_value = {'edge_id': 'validation-edge-1', 'sequence': 1}
    live.run()
    assert popup.call_args.kwargs['payload']['edge_title'] == 'Genetic Risk → ADHD'
    events['B'] = event_for(b, 2, 'b-2')
    live.run()
    assert live.session_state['snapshot_tabs'] == 'Validation'
    assert live.radio(key='v2_chain_active').value == 'B'
    assert (popup.call_args.kwargs['payload']['year'], popup.call_args.kwargs['payload']['age']) == (2026, 32)
    assert popup.call_args.kwargs['payload']['edge_title'] == f"{b['steps'][2]['source']} → {b['steps'][2]['target']}"
    live.radio(key='v2_step_detail_mode').set_value('Story').run()
    assert live.session_state['snapshot_tabs'] == 'Story'


def test_endpoints_refresh_only_the_edited_chain_and_select_its_evidence(workspace):
    chains, events, _, popup = workspace
    live = app().run()
    original_b = chains['B']
    events['B'] = event_for(original_b, 2, 'keep-b-step')
    live.run()
    live.selectbox(key='v2_chain_start_a').set_value('Genetic Risk').run()
    assert not live.exception
    assert chains['A']['node_ids'][0] == 'Genetic Risk'
    assert chains['A']['node_ids'][-1] == 'Quality of Life'
    assert chains['B'] == original_b
    assert live.session_state['v2_chain_selection_b_step'] == 2
    assert live.radio(key='v2_chain_active').value == 'A'
    live.selectbox(key='v2_chain_end_a').set_value('Symptom Severity').run()
    assert not live.exception
    assert chains['A']['node_ids'] == ['Genetic Risk', 'ADHD', 'Symptom Severity']
    original_a = chains['A']
    live.radio(key='v2_step_detail_mode').set_value('Validation').run()
    assert (popup.call_args.kwargs['payload']['year'], popup.call_args.kwargs['payload']['age']) == (1970, 8)
    assert popup.call_args.kwargs['payload']['edge_title'] == 'Genetic Risk → ADHD'
    live.selectbox(key='v2_chain_start_b').set_value('Treatment Access').run()
    live.selectbox(key='v2_chain_end_b').set_value('Functional Impairment').run()
    assert not live.exception
    assert chains['A'] == original_a
    assert chains['B']['node_ids'][0] == 'Treatment Access'
    assert chains['B']['node_ids'][-1] == 'Functional Impairment'
    assert live.radio(key='v2_chain_active').value == 'B'
    assert live.session_state['v2_chain_selection_b_step'] == 0
    assert live.session_state['snapshot_tabs'] == 'Validation'
    assert (popup.call_args.kwargs['payload']['year'], popup.call_args.kwargs['payload']['age']) == (2026, 32)
    assert popup.call_args.kwargs['payload']['edge_title'] == f"{chains['B']['steps'][0]['source']} → {chains['B']['steps'][0]['target']}"


def test_invalid_or_disconnected_endpoints_do_not_remove_the_other_chain(workspace):
    chains, _, _, popup = workspace
    live = app().run()
    original_b = chains['B']
    live.selectbox(key='v2_chain_end_a').set_value('Diagnosis Status').run()
    assert not live.exception
    assert any('Scenario A: Choose different starting' in item.value for item in live.info)
    assert live.session_state['v2_chain_selection_a_context'] is None
    assert chains['B'] == original_b
    live.radio(key='v2_chain_active').set_value('B').run()
    live.radio(key='v2_step_detail_mode').set_value('Validation').run()
    assert (popup.call_args.kwargs['payload']['year'], popup.call_args.kwargs['payload']['age']) == (2026, 32)
    live.selectbox(key='v2_chain_start_a').set_value('Quality of Life').run()
    live.selectbox(key='v2_chain_end_a').set_value('Genetic Risk').run()
    assert not live.exception
    assert any('Scenario A: No directed route from Quality of Life → Genetic Risk' in item.value for item in live.info)
    assert chains['B'] == original_b
    live.selectbox(key='v2_chain_start_a').set_value('Genetic Risk').run()
    live.selectbox(key='v2_chain_end_a').set_value('Symptom Severity').run()
    assert not live.exception
    assert chains['A']['node_ids'] == ['Genetic Risk', 'ADHD', 'Symptom Severity']
    assert chains['B'] == original_b


def test_query_changes_reject_stale_events_and_filters_preserve_full_comparison(workspace):
    chains, events, _, _ = workspace
    live = app().run()
    events['A'] = event_for(chains['A'], 2, 'a-old')
    events['B'] = event_for(chains['B'], 1, 'b-old')
    live.run()
    live.selectbox(key='v2_chain_year_b').set_value(1990).run()
    assert not live.exception
    assert live.session_state['v2_chain_selection_b_step'] == 0
    assert live.session_state['v2_chain_selection_a_step'] == 2
    live.session_state['snapshot_tabs'] = 'Changes'
    live.run()
    tables = [frame.value.copy() for frame in live.dataframe]
    assert tables
    live.slider(key='v2_strength').set_value(1.0).run()
    live.session_state['snapshot_tabs'] = 'Changes'
    live.run()
    assert not live.exception
    assert any('No directed route' in item.value for item in live.info)
    assert len(tables) == len(live.dataframe)
    for expected, current in zip(tables, live.dataframe):
        assert expected.equals(current.value)
    live.slider(key='v2_strength').set_value(0.0).run()
    assert live.session_state['v2_chain_selection_a_step'] == 0
    assert live.session_state['v2_chain_selection_b_step'] == 0
    live.selectbox(key='v2_chain_end_a').set_value('Diagnosis Status').run()
    assert not live.exception
    assert any('different starting' in item.value for item in live.info)
    live.selectbox(key='v2_chain_end_a').set_value('Quality of Life').run()
    live.selectbox(key='v2_chain_year_b').set_value(2026).run()
    live.selectbox(key='v2_chain_start_a').set_value('Digital Therapeutics').run()
    live.selectbox(key='v2_chain_start_b').set_value('Digital Therapeutics').run()
    assert not live.exception
    assert any('Scenario A does not contain' in item.value for item in live.info)
    live.radio(key='v2_chain_active').set_value('B').run()
    assert not live.exception
    assert chains['B']['node_ids'][0] == 'Digital Therapeutics'
    live.radio(key='v2_chain_active').set_value('A').run()
    assert not live.exception
    assert live.session_state['snapshot_tabs'] == 'Info'


def test_saved_comparison_preserves_both_scenarios_and_restores_live_controls(workspace, tmp_path):
    chains, _, _, popup = workspace
    live = app().run()
    live.selectbox(key='v2_chain_start_a').set_value('Genetic Risk').run()
    live.selectbox(key='v2_chain_end_a').set_value('ADHD').run()
    live.selectbox(key='v2_chain_start_b').set_value('Treatment Access').run()
    live.selectbox(key='v2_chain_end_b').set_value('Functional Impairment').run()
    original = dict(chains)
    live.text_input(key='v2_chain_save_name').set_value('Dashboard comparison').run()
    live.button(key='v2_chain_save_button').click().run()
    assert not live.exception
    entries = chain_store.list_saved_chains(tmp_path)
    assert len(entries) == 1
    saved_id = entries[0]['save_id']
    saved = chain_store.load_saved_chains(tmp_path / (saved_id + '.json'))
    assert saved['chains'] == [original['A'], original['B']]
    live.selectbox(key='v2_chain_year_a').set_value(2010).run()
    live.selectbox(key='v2_chain_age_a').set_value(45).run()
    live.selectbox(key='v2_chain_year_b').set_value(1990).run()
    live.selectbox(key='v2_chain_age_b').set_value(8).run()
    route_ids = {side: route_control(live, side).value for side in ('A', 'B')}
    live.button(key='chain_library_open').click().run()
    assert not live.exception
    assert chains == original
    assert len(live.get('download_button')) == 2
    live.radio(key='v2_chain_active').set_value('B').run()
    live.radio(key='v2_step_detail_mode').set_value('Validation').run()
    assert (popup.call_args.kwargs['payload']['year'], popup.call_args.kwargs['payload']['age']) == (2026, 32)
    live.slider(key='v2_strength').set_value(1.0).run()
    assert chains == original
    assert popup.call_args.kwargs['payload']['age'] == 32
    live.slider(key='v2_strength').set_value(0.0).run()
    live.radio(key='v2_chain_mode').set_value('Explore chains').run()
    assert not live.exception
    assert live.selectbox(key='v2_chain_year_a').value == 2010
    assert live.selectbox(key='v2_chain_age_a').value == 45
    assert live.selectbox(key='v2_chain_year_b').value == 1990
    assert live.selectbox(key='v2_chain_start_a').value == 'Genetic Risk'
    assert live.selectbox(key='v2_chain_end_a').value == 'ADHD'
    assert live.selectbox(key='v2_chain_start_b').value == 'Treatment Access'
    assert live.selectbox(key='v2_chain_end_b').value == 'Functional Impairment'
    for side in ('A', 'B'):
        assert route_control(live, side).value == route_ids[side]
    fresh = app()
    fresh.query_params['saved_chain'] = saved_id
    fresh.run()
    assert not fresh.exception
    assert chains == original
    assert fresh.radio(key='v2_chain_mode').value == 'Saved chains'
    fresh.radio(key='v2_chain_active').set_value('B').run()
    fresh.radio(key='v2_step_detail_mode').set_value('Validation').run()
    assert popup.call_args.kwargs['payload']['age'] == 32


def test_single_chain_saves_and_bad_records_still_open_safely(workspace, tmp_path):
    chains, _, _, _ = workspace
    app().run()
    record = chain_store.create_saved_chains([chains['A']], 'Legacy single chain')
    chain_store.save_chains(record, tmp_path)
    fresh = app()
    fresh.query_params['saved_chain'] = record['save_id']
    fresh.run()
    assert not fresh.exception
    assert fresh.radio(key='v2_chain_active').options == ['Scenario A']
    broken = app()
    broken.query_params['saved_chain'] = '0' * 24
    broken.run()
    assert not broken.exception
    assert any('cannot be opened' in item.value for item in broken.error)


def test_failed_save_keeps_comparison_downloads_available(workspace, monkeypatch, tmp_path):
    def cannot_save(*args, **kwargs):
        raise OSError('Read-only folder')
    monkeypatch.setattr(chain_store, 'save_chains', cannot_save)
    live = app().run()
    live.button(key='v2_chain_save_button').click().run()
    assert not live.exception
    assert any('still download' in error.value for error in live.error)
    assert len(live.get('download_button')) == 2
    assert not list(tmp_path.iterdir())


def test_validation_mapping_requires_matching_scenario_and_endpoints():
    chain = {'scenario': {'year': 2026, 'age': 8}}
    step = {'source': 'Diagnosis Status', 'target': 'Quality of Life'}
    snapshot = {'year': 2026, 'age': 8, 'edges': [
        {'id': 'validation-edge-4', 'from': 'Quality of Life', 'to': 'Diagnosis Status'},
        {'id': 'validation-edge-9', 'from': 'Diagnosis Status', 'to': 'Quality of Life'},
    ]}
    assert validation_edge_for_step(chain, step, snapshot) == 'validation-edge-9'
    assert validation_edge_for_step(chain, step, snapshot | {'age': 32}) is None
    assert validation_edge_for_step(chain, step, snapshot | {'year': 1970}) is None
    assert validation_edge_for_step(chain, step, snapshot | {'edges': []}) is None
