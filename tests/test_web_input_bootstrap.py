from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_legacy_engine_uses_current_dom_ids_and_guards_missing_elements():
    script = (ROOT / "website" / "assets" / "ant-engine.js").read_text(encoding="utf-8")

    assert "getElementById('command-input')" in script
    assert "getElementById('send-btn')" in script
    assert "getElementById('antInput')" not in script
    assert "getElementById('send')" not in script
    assert "getElementById('antSphere')" not in script
    assert "if (!input || !send) return;" in script


def test_website_controller_and_markup_use_the_same_input_ids():
    html = (ROOT / "website" / "index.html").read_text(encoding="utf-8")
    controller = (ROOT / "website" / "assets" / "ant-main-event-controller.js").read_text(
        encoding="utf-8"
    )

    assert 'id="command-input"' in html
    assert 'id="send-btn"' in html
    assert "querySelector('#command-input')" in controller
    assert "querySelector('#send-btn')" in controller
