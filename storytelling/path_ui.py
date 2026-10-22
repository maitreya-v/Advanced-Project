"""Choose an isolated directed route, then inspect reasons and tiny stories."""
import json

import streamlit as st

from .data import ROOT
from .director import GenerationError, save_story
from .graph_selector import apply_node_selection, full_graph_html, graph_selector_component
from .path_player import path_player_html
from .path_story import baseline_path_story, generate_path_story, load_path_story, story_key
from .paths import attach_path_review, discover_routes, route_edges


@st.cache_data(show_spinner=False)
def cached_routes(snapshot, start, end, max_hops, minimum_strength):
    return discover_routes(snapshot, start, end, max_hops=max_hops, minimum_strength=minimum_strength)


def render_path_story(snapshots: dict) -> None:
    st.title("Explore the graph. Choose your story.")
    st.caption("Pick Start and End on the full graph, then follow a route: one reason and two tiny fictional stories per arrow.")
    with st.sidebar:
        st.header("Choose a path")
        years = sorted(snapshots)
        requested_year = st.query_params.get("year")
        default_year = next((index for index, value in enumerate(years) if str(value) == requested_year), len(years) - 1)
        year = st.selectbox("Story year", years, index=default_year, key="path_year")
        ages = sorted(snapshots[year])
        requested_age = st.query_params.get("age")
        default_age = next((index for index, value in enumerate(ages) if str(value) == requested_age), ages.index(8) if 8 in ages else 0)
        age = st.selectbox("Story age", ages, index=default_age, key="path_age")
        snapshot = snapshots[year][age]
        names = sorted(node["id"] for node in snapshot["nodes"])
        max_hops = st.slider("Maximum directed steps", 1, 7, 5, key="path_hops")
        with st.expander("Route filters"):
            minimum_strength = st.slider("Minimum authored edge strength", 0.0, 1.0, 0.0, 0.05, key="path_minimum")
            st.caption("This changes which routes are eligible. Strength is an authored model value.")
    start_key = f"path_start_{year}_{age}"
    end_key = f"path_end_{year}_{age}"
    st.session_state.setdefault(start_key, None)
    st.session_state.setdefault(end_key, None)
    overview_label = "1. Full graph and endpoints"
    story_label = "2. Routes and stories"
    if st.session_state.get("path_graph_scope") != snapshot["fingerprint"]:
        st.session_state["path_graph_scope"] = snapshot["fingerprint"]
        st.session_state["path_workflow_tab"] = overview_label
    if "path_pending_tab" in st.session_state:
        st.session_state["path_workflow_tab"] = st.session_state.pop("path_pending_tab")
    overview_tab, story_tab = st.tabs([overview_label, story_label], key="path_workflow_tab", on_change="rerun")
    with overview_tab:
        st.caption(f"{year} · Age {age} · Full graph: {len(snapshot['nodes'])} nodes and {len(snapshot['edges'])} directed edges")
        st.markdown("**Click a node to set Start, then click another node to set End.** Use the Set Start / Set End buttons to change either endpoint.")
        selection = graph_selector_component(
            html=full_graph_html(snapshot), start=st.session_state[start_key], end=st.session_state[end_key],
            height=700, key="story-graph-" + snapshot["fingerprint"], default=None,
        )
        if apply_node_selection(selection, snapshot, st.session_state, start_key, end_key):
            st.rerun()
        start_column, end_column = st.columns(2)
        start = start_column.selectbox("Start concept", names, index=None, placeholder="Click a node or choose here", key=start_key)
        end = end_column.selectbox("End concept", names, index=None, placeholder="Click a node or choose here", key=end_key)
        if start == end and start is not None:
            st.info("Choose different starting and ending concepts.")
        signature = (snapshot["fingerprint"], start, end, max_hops, minimum_strength)
        if st.button("Find directed routes", type="primary", width="stretch", disabled=start is None or end is None or start == end):
            st.session_state["path_requested_query"] = signature
            st.session_state["path_pending_tab"] = story_label
            st.rerun()
    with story_tab:
        if start is None or end is None or st.session_state.get("path_requested_query") != signature:
            st.info("Choose Start and End on the Full graph tab, then click Find directed routes. Changing the endpoints or filters starts a new query.")
            return
        render_route_stories(snapshot, start, end, max_hops, minimum_strength)


def render_route_stories(snapshot: dict, start: str, end: str, max_hops: int, minimum_strength: float) -> None:
    year, age = snapshot["year"], snapshot["age"]
    if start == end:
        st.info("Choose different starting and ending concepts.")
        return
    result = cached_routes(snapshot, start, end, max_hops, minimum_strength)
    if not result["complete"]:
        reason = "the route limit" if result["stop_reason"] == "path_limit" else "the time limit"
        st.warning(f"Search reached {reason}. Showing {result['returned_count']} routes found so far; others may exist. Narrow the search for a complete list.")
    elif not result["paths"]:
        st.info(f"No directed route found within {max_hops} steps." if result["reachable"] else "The ending concept is not reachable from this start with the selected filters.")
    else:
        st.caption(f"{result['total_count']} routes found · {year} · Age {age} · Up to {max_hops} directed steps")
    if not result["paths"]:
        return
    paths = result["paths"]
    default = next((index for index, route in enumerate(paths)
                    if "Medication Treatment" in route["node_ids"] and "Symptom Severity" in route["node_ids"]), 0)
    choices = {route["path_id"]: route for route in paths}
    route_id = st.selectbox(
        "Select a complete route", list(choices), index=default,
        format_func=lambda value: f"{choices[value]['hop_count']} steps · " + " → ".join(choices[value]["node_ids"]),
        key=f"route_choice_{year}_{age}_{start}_{end}_{max_hops}_{minimum_strength}",
    )
    route = choices[route_id]
    st.caption("The player below isolates this route. Return to Full graph and endpoints to choose another start or end.")
    with st.expander("See every route option"):
        st.dataframe([{"Steps": item["hop_count"], "Route": " → ".join(item["node_ids"]),
                       "Domains": " → ".join(item["domains"])} for item in paths], hide_index=True, width="stretch")
    question = st.text_input("What should the examples bring into focus?", placeholder="For example: classroom tasks, work routines or practical barriers", max_chars=500, key="path_question")
    try:
        edges = attach_path_review(snapshot, route_edges(snapshot, route))
        key = story_key(snapshot, route, question, edges)
        state_key = "path_story_" + key
        if state_key not in st.session_state:
            saved = ROOT / "stories" / (key + ".json")
            if saved.exists():
                try:
                    st.session_state[state_key] = load_path_story(saved, snapshot, route, question)
                except (ValueError, KeyError, OSError) as error:
                    st.warning(f"The saved story could not be reused: {error}")
            if state_key not in st.session_state:
                st.session_state[state_key] = baseline_path_story(snapshot, route, question)
        generate_column, baseline_column = st.columns(2)
        generate = generate_column.button("Generate story for this path", type="primary", width="stretch")
        reset = baseline_column.button("Use authored reasons and examples", width="stretch")
        if reset:
            st.session_state[state_key] = baseline_path_story(snapshot, route, question)
        if generate:
            try:
                with st.spinner("Writing two concise examples for every arrow…"):
                    new_story = generate_path_story(snapshot, route, question)
                st.session_state[state_key] = new_story
                st.success("Your new examples are ready for every step.")
            except (GenerationError, ValueError) as error:
                st.error(str(error))
        story = st.session_state[state_key]
        st.caption("Each arrow has a reason and two fictional examples. Generate new examples locally without changing the selected graph.")
        player = path_player_html(story, snapshot, route)
    except (ValueError, KeyError, OSError) as error:
        st.error(f"This route could not be prepared with current source data: {error}")
        return
    st.iframe(player, height="content")
    download_column, json_column, save_column = st.columns(3)
    download_column.download_button("Download playable story", player, file_name=f"edge-stories-{key}.html", mime="text/html", width="stretch")
    json_column.download_button("Download story and graph facts", json.dumps(story, indent=2, ensure_ascii=False), file_name=f"edge-stories-{key}.json", mime="application/json", width="stretch")
    if save_column.button("Save this story", width="stretch"):
        try:
            save_story(story, ROOT / "stories")
            st.success("Saved for replay without the model.")
        except OSError:
            st.error("This host cannot save the story. Use the download instead.")
    with st.expander("Inspect the complete story and its relationships"):
        st.caption(story["fiction_note"])
        st.subheader(story["title"])
        st.write(story["opening"])
        for index, chapter in enumerate(story["chapters"], 1):
            st.markdown(f"**{index}. {chapter['title']}**")
            st.markdown("**Reason:**")
            st.write(chapter["reason"])
            for example_index, example in enumerate(chapter["examples"], 1):
                st.markdown(f"**Example {example_index}:**")
                st.write(example)
            edge = chapter["relationship"]
            st.caption(f"{edge['from']} → {edge['to']} · sign {edge['sign']} · authored strength {edge['strength']:.2f} · {edge['explanation']}")
        st.write(story["closing"])
        st.caption(story["validation"])
