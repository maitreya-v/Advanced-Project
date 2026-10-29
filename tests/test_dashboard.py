from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_defaults_and_both_comparison_modes():
    app = AppTest.from_file(str(ROOT / "Dashboard.py"), default_timeout=30).run()
    assert not app.exception
    app.radio[0].set_value("Story mode").run()
    assert not app.exception
    assert next(s for s in app.selectbox if s.label == "From year").value == 2010
    assert any("Local Qwen" in str(c.value) for c in app.caption)
    app.radio[1].set_value("Across ages").run()
    assert not app.exception
    assert any("Separate age scenarios" in str(c.value) for c in app.caption)
    app.radio[0].set_value("Explore graph").run()
    assert not app.exception
    app.radio[0].set_value("Evaluation lab").run()
    assert not app.exception
    assert any("24-case" in str(c.value) for c in app.caption)
