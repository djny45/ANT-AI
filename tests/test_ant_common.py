from ant_common import (
    AuditTrail,
    KeywordStore,
    Registry,
    approval_result,
    keyword_filter,
    keyword_match,
    sha256_hex,
    utc_timestamp,
)


def test_utc_timestamp_is_iso_utc():
    assert utc_timestamp().endswith("+00:00")


def test_sha256_hex_is_stable():
    assert sha256_hex("secret") == sha256_hex("secret")
    assert sha256_hex("secret") != sha256_hex("other")
    assert len(sha256_hex("secret")) == 64


def test_audit_trail_records_and_copies_history():
    trail = AuditTrail()
    entry = trail.record(action="GRANT", agent="agent1")

    assert entry["action"] == "GRANT"
    assert entry["timestamp"]
    assert len(trail) == 1

    history = trail.history()
    history.clear()
    assert len(trail) == 1

    trail.clear()
    assert list(trail) == []


def test_approval_result_shape():
    denied = approval_result(False, agent="agent1")
    assert denied["approved"] is False
    assert denied["review_required"] is True
    assert denied["agent"] == "agent1"
    assert approval_result(True)["review_required"] is False


def test_registry_lifecycle():
    registry: Registry[str] = Registry()
    registry.register("a", "first")
    registry.register("b", "second")

    assert registry.get("a") == "first"
    assert registry.get("missing") is None
    assert registry.names() == ["a", "b"]
    assert registry.values() == ["first", "second"]
    assert "b" in registry
    assert len(registry) == 2
    assert registry.mapping["a"] == "first"

    registry.remove("a")
    registry.remove("a")
    assert registry.names() == ["b"]

    registry.clear()
    assert len(registry) == 0


def test_keyword_search_helpers():
    assert keyword_match("Hello World", "hello")
    assert not keyword_match("Hello", "bye")
    assert keyword_filter(["alpha", "beta"], "AL") == ["alpha"]
    assert keyword_filter([{"t": "alpha"}], "alpha", key=lambda i: i["t"]) == [{"t": "alpha"}]


def test_keyword_store_search():
    store = KeywordStore("content")
    store.add("Deploy the API", source="docs")
    store.add("Unrelated note")

    assert store.search("deploy") == [{"content": "Deploy the API", "source": "docs"}]
    assert len(store.all()) == 2

    store.clear()
    assert store.search("deploy") == []
