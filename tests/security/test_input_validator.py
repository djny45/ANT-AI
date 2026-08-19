from security.input_validator import InputValidator


def test_validate_and_sanitize():
    v = InputValidator()
    assert v.validate_string("hello")
    assert not v.validate_string("<script>alert(1)</script>")
    # length check: use a small max_length to force failure
    assert not v.validate_string("a" * 2000, max_length=1000)
    # sanitize
    assert v.sanitize_string('<b>bold</b>') == '&lt;b&gt;bold&lt;/b&gt;'


def test_validate_string_rejects_sql_injection_and_non_strings():
    v = InputValidator()

    assert not v.validate_string("admin' OR 1=1")
    assert not v.validate_string("DROP TABLE users")
    assert not v.validate_string("anything --")
    assert v.validate_string("SELECT name FROM users")
    assert not v.validate_string(42)


def test_validate_input_walks_nested_dicts_and_lists():
    v = InputValidator()
    valid = {
        "message": "hello",
        "items": ["ordinary text", {"description": "SELECT name FROM users"}],
    }
    invalid_dict = {"outer": {"message": "<script>alert(1)</script>"}}
    invalid_list = {"outer": ["safe", {"message": "UNION 1=1"}]}
    invalid_list_string = {"outer": ["safe", "admin OR 1=1"]}

    assert v.validate_input(valid)
    assert not v.validate_input(invalid_dict)
    assert not v.validate_input(invalid_list)
    assert not v.validate_input(invalid_list_string)
