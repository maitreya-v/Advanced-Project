"""Exercise saving and opening with genuinely fresh app sessions."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

from storytelling import chain_store

ROOT = Path(__file__).resolve().parents[1]


def app():
    return AppTest.from_file(str(ROOT / "Chain_Prototype.py"), default_timeout=45)


def test_library_survives_new_sessions_and_saved_views_preserve_live_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(chain_store, "DEFAULT_DIRECTORY", tmp_path)
    live = app().run()
    assert not live.exception
    live.text_input(key="chain_save_name").set_value("My saved route").run()
    live.button(key="chain_save_button").click().run()
    assert not live.exception
    entries = chain_store.list_saved_chains(tmp_path)
    assert len(entries) == 1 and entries[0]["name"] == "My saved route"
    saved_id = entries[0]["save_id"]
    saved = chain_store.load_saved_chains(tmp_path / (saved_id + ".json"))
    live.selectbox(key="chain_age").set_value(32).run()
    live.button(key="chain_library_open").click().run()
    assert not live.exception and live.radio(key="chain_mode").value == "Saved chains"
    assert chain_store.load_saved_chains(tmp_path / (saved_id + ".json")) == saved
    assert live.query_params["saved_chain"] == [saved_id]
    live.radio(key="chain_mode").set_value("Explore chains").run()
    assert not live.exception and live.selectbox(key="chain_age").value == 32
    fresh = app()
    fresh.query_params["saved_chain"] = saved_id
    fresh.run()
    assert not fresh.exception and fresh.radio(key="chain_mode").value == "Saved chains"
    assert fresh.selectbox(key="chain_library_choice").value == saved_id
    assert any(item.value == "My saved route" for item in fresh.subheader)


def test_read_only_save_failure_keeps_downloads_available(tmp_path, monkeypatch):
    monkeypatch.setattr(chain_store, "DEFAULT_DIRECTORY", tmp_path)

    def cannot_save(*args, **kwargs):
        raise OSError("Read-only folder")

    monkeypatch.setattr(chain_store, "save_chains", cannot_save)
    live = app().run()
    live.button(key="chain_save_button").click().run()
    assert not live.exception
    assert any("still download" in error.value for error in live.error)
    assert len(live.get("download_button")) == 2
    assert list(tmp_path.iterdir()) == []
