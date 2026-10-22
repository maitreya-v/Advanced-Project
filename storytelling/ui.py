"""Streamlit controls around a persistent in-frame scene player."""
import json

import streamlit as st

from .analysis import THEMES, fact_catalog, story_key
from .data import ROOT
from .director import GenerationError, LocalOllama, baseline_story, generate_story, load_story, save_story
from .player import player_html


def render_story_mode(snapshots: dict) -> None:
    st.markdown('<div style="font-size:11px;letter-spacing:2px;color:#50828b;font-weight:700">ADHD GRAPH STORIES</div>', unsafe_allow_html=True)
    st.title("Follow what changes.")
    st.caption("A guided view of the relationships in your model, with evidence behind every scene.")
    years = sorted(snapshots)
    with st.sidebar:
        st.header("Shape the story")
        axis = st.radio("Compare", ["Across years", "Across ages"])
        if axis == "Across years":
            ages = sorted(set.intersection(*(set(snapshots[y]) for y in years)))
            age = st.selectbox("Keep age fixed", ages, index=0)
            first = st.selectbox("From year", years[:-1], index=max(0, len(years)-2))
            later = [y for y in years if y > first]
            last = st.selectbox("To year", later, index=len(later)-1)
            before, after = snapshots[first][age], snapshots[last][age]
        else:
            year = st.selectbox("Keep year fixed", years, index=len(years)-1)
            ages = sorted(snapshots[year])
            first = st.selectbox("From age", ages[:-1])
            later = [a for a in ages if a > first]
            last = st.selectbox("To age", later)
            before, after = snapshots[year][first], snapshots[year][last]
            st.caption("Separate age scenarios, not a person's life history.")
        theme = st.selectbox("Focus", list(THEMES))
        st.divider()
        with st.expander("Local model setup"):
            st.caption("No API key or model usage charges. Live generation runs on the machine hosting this app.")
            st.code("ollama pull qwen3:8b\nollama serve", language="bash")
            if st.button("Check local model"):
                try:
                    if LocalOllama().available():
                        st.success("Qwen3 8B is ready.")
                    else:
                        st.warning("Ollama is running. Download qwen3:8b first.")
                except GenerationError as exc:
                    st.warning(str(exc))
    question = st.text_input(
        "What should this story explain?",
        placeholder="How do telehealth and treatment access change?",
        max_chars=500,
        key="story_question",
        help="Optional. Choose a comparison and focus in the sidebar, then generate a story about your question.",
    )
    action, alternative = st.columns(2)
    with action:
        generate = st.button("Generate a new story", type="primary", width="stretch")
    with alternative:
        baseline = st.button("Use rule-based story", width="stretch")
    st.caption("Generate on demand with local Qwen: one story with up to four scenes per request. No API charges. Generation may take a minute or more.")
    key = story_key(before, after, theme, question)
    cache_path = ROOT / "stories" / (key + ".json")
    state_key = "story_" + key
    if state_key not in st.session_state:
        if cache_path.exists():
            try:
                st.session_state[state_key] = load_story(cache_path, before, after, theme, question)
            except (ValueError, KeyError, OSError) as exc:
                st.warning(f"The saved story could not be reused: {exc}")
        if state_key not in st.session_state:
            st.session_state[state_key] = baseline_story(before, after, theme, question)
    if baseline:
        st.session_state[state_key] = baseline_story(before, after, theme, question)
    if generate:
        try:
            with st.spinner("Qwen is inspecting graph facts and directing your story…"):
                st.session_state[state_key] = generate_story(before, after, theme, question)
            st.success("Your local AI story is ready.")
        except (GenerationError, ValueError) as exc:
            st.error(str(exc))
    story = st.session_state[state_key]
    label = "Local Qwen" if story["origin"] == "local-qwen" else "Rule-based"
    st.caption(f"{before['year']} · age {before['age']} → {after['year']} · age {after['age']}  |  {label}  |  {len(story['scenes'])} scenes")
    player = player_html(story, before, after)
    st.iframe(player, height="content")
    left, middle, right = st.columns(3)
    with left:
        st.download_button("Download standalone story", player, file_name=f"graph-story-{key}.html", mime="text/html", width="stretch")
    with middle:
        st.download_button("Download story + evidence", json.dumps(story, indent=2, ensure_ascii=False), file_name=f"graph-story-{key}.json", mime="application/json", width="stretch")
    with right:
        if st.button("Save for demo playback", width="stretch"):
            try:
                save_story(story, ROOT / "stories")
                st.success("Saved. This story can now play without Ollama.")
            except OSError:
                st.error("This host cannot save files. Download the story instead.")
    with st.expander("Ranked graph facts and generation details"):
        facts = fact_catalog(before, after, theme, question)
        st.caption("Editorial priority, not evidence confidence. All changes are measured between the two selected snapshots.")
        st.dataframe([{"Fact": f["title"], "Change": f["kind"], "Priority": f["score"], "Why": f["rank_reason"]} for f in facts], hide_index=True, width="stretch")
        st.caption(story["validation"])
        if story["origin"] == "local-qwen":
            st.write(f"Generated locally in {story['elapsed_seconds']} seconds.")
            st.json(story["trace"], expanded=False)
