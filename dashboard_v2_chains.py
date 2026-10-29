"""Horizontal chains and saved routes for the compact dashboard panels."""
import re

import streamlit as st

from storytelling import chain_store, chain_view
from storytelling.chain_core import apply_chain_selection, build_chain, query_chains
from storytelling.chain_ui import render_record_downloads, render_save_controls, render_saved_library
from storytelling.data import load_snapshots
from storytelling.scenario_comparison import compare_scenarios


@st.cache_data(show_spinner=False, max_entries=4)
def load_chain_snapshots(source_signature):
    # Use canonical records, not the dashboard's presentation/validation IDs.
    return load_snapshots()


@st.cache_data(show_spinner=False, max_entries=48)
def find_chains(snapshot, start, end, max_hops, minimum_strength):
    return query_chains(snapshot, start, end, max_hops=max_hops, minimum_strength=minimum_strength)


def validation_edge_for_step(chain, step, snapshot):
    """Resolve by scenario and endpoints; chain IDs differ from report IDs."""
    if (chain["scenario"]["year"], chain["scenario"]["age"]) != (snapshot["year"], snapshot["age"]):
        return None
    return next((edge["id"] for edge in snapshot["edges"]
                 if (edge["from"], edge["to"]) == (step["source"], step["target"])), None)


def _focus_chain_details():
    st.session_state["v2_detail_source"] = "chain"
    st.session_state["snapshot_tabs"] = st.session_state["v2_step_detail_mode"]


def _focus_scenario(side):
    st.session_state["v2_chain_pending_side"] = side
    _focus_chain_details()


def _scenario_controls(snapshots, year, age):
    settings = st.session_state.get("v2_comparison_settings", {})
    columns = st.columns(4)
    scopes = {}
    for index, side in enumerate(("a", "b")):
        year_key, age_key = f"v2_chain_year_{side}", f"v2_chain_age_{side}"
        st.session_state.setdefault(year_key, settings.get(year_key, year if side == "a" else max(snapshots)))
        selected_year = columns[index * 2].selectbox(f"Year {side.upper()}", sorted(snapshots), key=year_key)
        ages = sorted(snapshots[selected_year])
        st.session_state.setdefault(age_key, settings.get(age_key, age if side == "a" else 32))
        if st.session_state[age_key] not in ages:
            st.session_state[age_key] = ages[0]
        selected_age = columns[index * 2 + 1].selectbox(f"Age {side.upper()}", ages, key=age_key)
        settings.update({year_key: selected_year, age_key: selected_age})
        scopes[side.upper()] = snapshots[selected_year][selected_age]
    st.session_state["v2_comparison_settings"] = settings
    return scopes


def _route_for_scenario(snapshot, side, start, end, hops, minimum_strength, settings):
    result = find_chains(snapshot, start, end, hops, minimum_strength)
    chain = None
    if result["paths"]:
        routes = {route["path_id"]: route for route in result["paths"]}
        route_key, query_key = f"v2_chain_route_{side.lower()}", f"query_{side.lower()}"
        default = next((route for route in result["paths"]
                        if len(route["node_ids"]) > 3 and "Medication Treatment" in route["node_ids"]), result["paths"][0])
        saved_route = settings.get(route_key) if settings.get(query_key) == result["query_id"] else None
        preferred = saved_route if saved_route in routes else default["path_id"]
        # Scope route widgets to their query, so old dropdown events cannot
        # restore a route from different endpoints or filters.
        widget_key = route_key + "_" + result["query_id"]
        preferred = st.session_state.get(widget_key, preferred)
        route_id = st.selectbox(f"Route {side}", list(routes), key=widget_key, index=list(routes).index(preferred),
                                format_func=lambda key: f"{routes[key]['hop_count']} steps · " + " → ".join(routes[key]["node_ids"]),
                                on_change=_focus_scenario, args=(side,))
        settings.update({route_key: route_id, query_key: result["query_id"]})
        chain = build_chain(snapshot, routes[route_id], max_hops=hops, minimum_strength=minimum_strength)
    return chain, result


def _explore_chains(scopes, snapshots, minimum_strength, route_controls):
    settings = st.session_state.get("v2_chain_settings", {})
    concepts = sorted({node["id"] for ages in snapshots.values()
                       for snapshot in ages.values() for node in snapshot["nodes"]})
    chains, results = {}, {}
    with route_controls.popover("Choose routes", width="stretch"):
        # Popover widgets mount in the browser when opened. Supply their real
        # defaults in the widget proto instead of relying on a one-time state
        # update emitted while the popover was still closed.
        hops = st.selectbox("Max steps", range(1, 8), key="v2_chain_hops",
                            index=st.session_state.get("v2_chain_hops", settings.get("hops", 5)) - 1)
        settings["hops"] = hops
        columns = st.columns(len(scopes))
        for column, (side, snapshot) in zip(columns, scopes.items()):
            with column:
                st.markdown(f"**Scenario {side}**")
                start_key, end_key = f"v2_chain_start_{side.lower()}", f"v2_chain_end_{side.lower()}"
                # Migrate the previous shared endpoint controls on first use.
                start_default = st.session_state.get(start_key, settings.get(f"start_{side.lower()}", settings.get("start", "Diagnosis Status")))
                end_default = st.session_state.get(end_key, settings.get(f"end_{side.lower()}", settings.get("end", "Quality of Life")))
                start = st.selectbox(f"Start {side}", concepts, key=start_key, index=concepts.index(start_default),
                                     on_change=_focus_scenario, args=(side,))
                end = st.selectbox(f"End {side}", concepts, key=end_key, index=concepts.index(end_default),
                                   on_change=_focus_scenario, args=(side,))
                settings.update({f"start_{side.lower()}": start, f"end_{side.lower()}": end})
                if start == end:
                    results[side] = {"state": "same_endpoints", "complete": True}
                else:
                    chains[side], results[side] = _route_for_scenario(snapshot, side, start, end, hops, minimum_strength, settings)
    st.session_state["v2_chain_settings"] = settings
    st.caption(f"Minimum chain strength {minimum_strength:.2f} · Choose start and end points separately for A and B")
    return chains, results


def _route_message(side, result):
    if result is None:
        return
    if result["state"] == "same_endpoints":
        st.info(f"Scenario {side}: Choose different starting and ending concepts.")
        return
    if result["state"] == "missing_endpoints":
        st.info(f"Scenario {side} does not contain: " + ", ".join(result["missing_endpoints"]) + ". Choose other endpoints or another scenario.")
    elif not result["paths"]:
        query = result["query"]
        route = f"{query['start']} → {query['end']}"
        st.info(f"Scenario {side}: No directed route from {route} within {query['max_hops']} steps. Increase Max steps or lower minimum strength." if result["reachable"]
                else f"Scenario {side}: No directed route from {route} with minimum strength {query['minimum_strength']:.2f}. Choose other endpoints or lower minimum strength.")
    if result["state"] != "missing_endpoints" and not result["complete"]:
        st.warning(f"Scenario {side}: Search reached its limit. Showing {result['returned_count']} routes found so far; others may exist.")


def _comparison_summary(changes):
    if changes is None:
        return
    counts = [(f"+{len(changes['added_nodes'])} / −{len(changes['removed_nodes'])}", "Nodes"),
              (f"+{len(changes['added_edges'])} / −{len(changes['removed_edges'])}", "Edges"),
              (str(len(changes["sign_changes"])), "Signs"),
              (str(len(changes["strength_changes"])), "Strengths")]
    st.html('<div class="v2-change-counts" title="Scenario changes from A to B">' + ''.join(
        f'<div><b>{count}</b><span>{label}</span></div>' for count, label in counts
    ) + '</div>')


def render_chain_workspace(snapshots, year, age, minimum_strength):
    """Render independent A/B routes and return their comparison and active step."""
    title, route_controls, library = st.columns([2, 1, 1])
    title.html('<div class="v2-section"><h2>Story chains</h2></div>')
    notice = st.session_state.pop("chain_saved_notice", None)
    if notice:
        st.success(notice.replace("in the sidebar", "above"))
    with library.popover("Saved chains", width="stretch"):
        opened = render_saved_library(snapshots)
    if opened is not None:
        st.session_state["v2_chain_open_id"] = opened["save_id"]
        st.session_state["v2_chain_mode"] = "Saved chains"
        st.query_params["saved_chain"] = opened["save_id"]
    elif "v2_chain_mode" not in st.session_state:
        requested = st.query_params.get("saved_chain", "")
        valid_id = bool(re.fullmatch(r"[a-f0-9]{24}", requested))
        st.session_state["v2_chain_mode"] = "Saved chains" if valid_id else "Explore chains"
        if valid_id:
            st.session_state["v2_chain_open_id"] = requested
    mode = st.radio("Chain view", ["Explore chains", "Saved chains"], key="v2_chain_mode",
                    horizontal=True, label_visibility="collapsed")
    record, chains, scopes, results = None, {}, {}, {}
    try:
        if mode == "Saved chains":
            saved_id = st.session_state.get("v2_chain_open_id", "")
            if not re.fullmatch(r"[a-f0-9]{24}", saved_id):
                st.info("Choose a chain under Saved chains above, then click Open saved chain.")
                return {"selection": None, "comparison": None}
            record = chain_store.load_saved_chains(chain_store.DEFAULT_DIRECTORY / (saved_id + ".json"), snapshots=snapshots)
            st.markdown(f"**{record['name']}**")
            st.caption("Saved view · Keeps its original scenario and filters independently of the graph controls")
            chains = dict(zip(("A", "B"), record["chains"]))
            scopes = {side: snapshots[chain["scenario"]["year"]][chain["scenario"]["age"]] for side, chain in chains.items()}
        else:
            st.query_params.pop("saved_chain", None)
            scopes = _scenario_controls(snapshots, year, age)
            chains, results = _explore_chains(scopes, snapshots, minimum_strength, route_controls)
    except (OSError, ValueError) as error:
        st.error(f"This chain cannot be opened: {error}")
        return {"selection": None, "comparison": None}
    changes = compare_scenarios(scopes["A"], scopes["B"]) if "B" in scopes else None
    _comparison_summary(changes)
    pending_side = st.session_state.pop("v2_chain_pending_side", None)
    if pending_side in scopes:
        st.session_state["v2_chain_active"] = pending_side
    if st.session_state.get("v2_chain_active") not in scopes:
        st.session_state["v2_chain_active"] = "A"
    st.session_state.setdefault("v2_step_detail_mode", "Story")
    active_control, mode_control = st.columns(2)
    side = active_control.radio("Selected scenario", list(scopes), key="v2_chain_active", horizontal=True,
                                format_func=lambda value: f"Scenario {value}", on_change=_focus_chain_details, label_visibility="collapsed")
    mode_control.radio("Step details", ["Story", "Validation"], key="v2_step_detail_mode",
                       horizontal=True, on_change=_focus_chain_details, label_visibility="collapsed")
    for chain_side in scopes:
        candidate = chains.get(chain_side)
        key = "v2_chain_selection_" + chain_side.lower()
        if candidate is None:
            st.session_state[key + "_context"] = None
            st.session_state[key + "_step"] = 0
            _route_message(chain_side, results.get(chain_side))
            continue
        apply_chain_selection(None, candidate, st.session_state, key=key)
        event = chain_view.chain_component(
            chain=candidate, selected_step=st.session_state[key + "_step"],
            key=f"v2_chain_preview_{chain_side.lower()}_{candidate['query_id']}_{candidate['chain_id']}", compact=True, comparison=True,
            label="Scenario " + chain_side, active=side == chain_side, default=None,
        )
        if apply_chain_selection(event, candidate, st.session_state, key=key):
            st.session_state["v2_chain_pending_side"] = chain_side
            st.session_state["v2_chain_pending_selection"] = (chain_side, candidate["query_id"], candidate["chain_id"])
            st.rerun()
        result = results.get(chain_side)
        if result and not result["complete"]:
            _route_message(chain_side, result)
    available = [chain for chain in chains.values() if chain is not None]
    if available:
        with st.expander("Download saved chains" if record else "Save or download comparison"):
            if record:
                render_record_downloads(record, snapshots, key="v2_saved_downloads")
            else:
                render_save_controls(available, snapshots, key="v2_chain_save")
    chain = chains.get(side)
    if chain is None:
        st.session_state["v2_displayed_chain"] = None
        return {"selection": None, "comparison": changes}
    context = (mode, record["save_id"] if record else None, side, chain["query_id"], chain["chain_id"])
    previous = st.session_state.get("v2_displayed_chain")
    pending = st.session_state.pop("v2_chain_pending_selection", None)
    changed = ((previous is not None and previous != context) or (previous is None and record is not None)
               or pending == (side, chain["query_id"], chain["chain_id"]))
    st.session_state["v2_displayed_chain"] = context
    step = chain["steps"][st.session_state[f"v2_chain_selection_{side.lower()}_step"]]
    return {"selection": {"chain": chain, "step": step, "changed": changed, "saved": record is not None, "side": side},
            "comparison": changes}


def _open_step_validation():
    st.session_state["v2_detail_source"] = "chain"
    st.session_state["snapshot_tabs"] = "Validation"
    st.session_state["v2_step_detail_mode"] = "Validation"


def render_step_story(selection):
    if selection is None:
        st.caption("Choose a route in Story chains to read its steps here.")
        return
    chain, step = selection["chain"], selection["step"]
    st.markdown(f"**Step {step['index'] + 1} of {len(chain['steps'])} · {step['source']} → {step['target']}**")
    st.caption(f"Scenario {selection['side']} · {chain['scenario']['year']} · Age {chain['scenario']['age']} · {'Positive' if step['sign'] == '+' else 'Negative'} · Authored strength {step['strength']:.2f}")
    st.write(step["reason"])
    examples = st.columns(2)
    for index, example in enumerate(step["examples"]):
        examples[index].caption(f"Example {index + 1}")
        examples[index].write(example)
    st.caption(chain["fiction_note"])
    with st.expander("Original graph explanation"):
        st.write(step["explanation"])
    st.button("View step validation", key="v2_chain_validation", on_click=_open_step_validation)


def render_scenario_changes(changes):
    if changes is None:
        st.caption("Explore two scenarios to compare their nodes and relationships. This saved item contains one chain.")
        return
    a, b = changes["scenario_a"], changes["scenario_b"]
    st.markdown(f"**A: {a['year']} · Age {a['age']} → B: {b['year']} · Age {b['age']}**")
    st.caption("Changes compare the complete scenarios. Chain route and strength filters do not affect these counts. Strengths are authored model values.")
    for key, title in (("added_nodes", "Added nodes · Only in B"), ("removed_nodes", "Removed nodes · Only in A")):
        st.markdown(f"**{title} ({len(changes[key])})**")
        st.write(", ".join(changes[key]) if changes[key] else "None")
    for key, title in (("added_edges", "Added edges · Only in B"), ("removed_edges", "Removed edges · Only in A"),
                       ("sign_changes", "Sign changes"), ("strength_changes", "Strength changes")):
        st.markdown(f"**{title} ({len(changes[key])})**")
        if not changes[key]:
            st.caption("None")
            continue
        rows = [{"Relationship": f"{edge['source']} → {edge['target']}",
                 "Sign A": edge["sign_a"] or "—", "Sign B": edge["sign_b"] or "—",
                 "Strength A": edge["strength_a"], "Strength B": edge["strength_b"],
                 "Δ strength (B − A)": edge["delta"]} for edge in changes[key]]
        st.dataframe(rows, hide_index=True, width="stretch",
                     column_config={name: st.column_config.NumberColumn(format="%.2f")
                                    for name in ("Strength A", "Strength B", "Δ strength (B − A)")})
