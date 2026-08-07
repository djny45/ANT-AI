from security.input_validator import InputValidator


def test_validate_and_sanitize():
    v = InputValidator()
    assert v.validate_string("hello")
    assert not v.validate_string("<script>alert(1)</script>")
    # length check: use a small max_length to force failure
    assert not v.validate_string("a" * 2000, max_length=1000)
    # sanitize
    assert v.sanitize_string('<b>bold</b>') == '&lt;b&gt;bold&lt;/b&gt;'
