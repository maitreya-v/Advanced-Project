"""Small chain and persistence controls for the prototype or dashboard panels."""
from pathlib import Path

import streamlit as st

from . import chain_store as storage
from . import chain_view
from .chain_core import apply_chain_selection
from .chain_export import saved_chains_html


def render_chain(chain: dict, *, key: str = "chain") -> dict:
    apply_chain_selection(None, chain, st.session_state, key=key)
    event = chain_view.chain_component(chain=chain, selected_step=st.session_state[key + "_step"],
                                       key=key + "_preview", default=None)
    if apply_chain_selection(event, chain, st.session_state, key=key):
        st.rerun()
    step = chain["steps"][st.session_state[key + "_step"]]
    with st.container(border=True):
        st.markdown(f"**Step {step['index'] + 1} · {step['source']} → {step['target']}**")
        st.write(step["reason"])
        columns = st.columns(2)
        for index, example in enumerate(step["examples"]):
            columns[index].caption(f"Example {index + 1}")
            columns[index].write(example)
    st.caption(chain["fiction_note"])
    return step


def render_record_downloads(record: dict, snapshots: dict, *, key: str = "downloads") -> None:
    html_column, json_column = st.columns(2)
    html_column.download_button("Download playable HTML", saved_chains_html(record, snapshots=snapshots),
                                file_name=f"chains-{record['save_id']}.html", mime="text/html",
                                key=key + "_html", on_click="ignore", width="stretch")
    json_column.download_button("Download chain JSON", storage.saved_chains_json(record, snapshots=snapshots),
                                file_name=f"chains-{record['save_id']}.json", mime="application/json",
                                key=key + "_json", on_click="ignore", width="stretch")


def render_save_controls(chains: list[dict], snapshots: dict, *, directory: Path | None = None,
                         key: str = "chain_save") -> None:
    context = [(chain["query_id"], chain["chain_id"]) for chain in chains]
    if st.session_state.get(key + "_context") != context:
        st.session_state[key + "_context"] = context
        first = chains[0]
        prefix = "Comparison" if len(chains) == 2 else f"{first['scenario']['year']} · Age {first['scenario']['age']}"
        st.session_state[key + "_name"] = f"{prefix} · {first['node_ids'][0]} → {first['node_ids'][-1]}"[:160]
    name = st.text_input("Save as", key=key + "_name", max_chars=160)
    if not name.strip():
        st.caption("Enter a name to save or download this chain.")
        return
    try:
        record = storage.create_saved_chains(chains, name, snapshots=snapshots)
    except ValueError as error:
        st.error(str(error))
        return
    if st.button("Save chain" if len(chains) == 1 else "Save comparison", key=key + "_button", type="primary"):
        try:
            storage.save_chains(record, storage.DEFAULT_DIRECTORY if directory is None else directory,
                                snapshots=snapshots)
        except (OSError, ValueError) as error:
            st.error(f"This chain could not be saved: {error}. You can still download it below.")
        else:
            st.session_state["chain_saved_notice"] = f"Saved “{record['name']}”. Open it from Saved chains in the sidebar."
            st.session_state["chain_saved_latest"] = record["save_id"]
            st.rerun()
    render_record_downloads(record, snapshots, key=key)


def render_saved_library(snapshots: dict, *, directory: Path | None = None) -> dict | None:
    directory = storage.DEFAULT_DIRECTORY if directory is None else Path(directory)
    st.header("Saved chains")
    try:
        entries = storage.list_saved_chains(directory)
    except OSError as error:
        st.warning(f"Saved chains could not be listed: {error}")
        return None
    if not entries:
        st.caption("Save a route to keep it here across reloads.")
        return None
    choices = {entry["save_id"]: entry for entry in entries}
    latest = st.session_state.pop("chain_saved_latest", None)
    if latest in choices:
        st.session_state["chain_library_choice"] = latest
    selected = st.selectbox("Saved chain", list(choices), key="chain_library_choice",
                            format_func=lambda value: choices[value]["name"])
    st.caption(f"{len(entries)} saved {'item' if len(entries) == 1 else 'items'}")
    if st.button("Open saved chain", key="chain_library_open", width="stretch"):
        try:
            if choices[selected]["error"]:
                raise ValueError(choices[selected]["error"])
            return storage.load_saved_chains(directory / (selected + ".json"), snapshots=snapshots)
        except (OSError, ValueError) as error:
            st.error(f"This saved chain cannot be opened: {error}")
    return None
