import pytest

from ant_langgraph.tools import ToolRegistry, ToolSpec


def test_tool_registry_register_get_and_list():
    registry = ToolRegistry()
    spec = ToolSpec("search", "agent-a", "read", risk_level=25)

    registry.register(spec)

    assert registry.get("search") == spec
    assert registry.list() == [spec]


def test_tool_spec_risk_level_bounds():
    registry = ToolRegistry()

    registry.register(ToolSpec("zero", "agent", "read", risk_level=0))
    registry.register(ToolSpec("hundred", "agent", "read", risk_level=100))

    with pytest.raises(ValueError):
        registry.register(ToolSpec("low", "agent", "read", risk_level=-1))
    with pytest.raises(ValueError):
        registry.register(ToolSpec("high", "agent", "read", risk_level=101))


def test_tool_execute_passes_kwargs_to_handler():
    calls = []

    def handler(**kwargs):
        calls.append(kwargs)
        return {"ok": True}

    registry = ToolRegistry()
    registry.register(ToolSpec("search", "agent-a", "read", handler=handler))

    assert registry.execute("search", "agent-a", query="ants", limit=2) == {"ok": True}
    assert calls == [{"query": "ants", "limit": 2}]


def test_tool_execute_enforces_owner_and_handler():
    registry = ToolRegistry()
    registry.register(ToolSpec("owned", "agent-a", "read", handler=lambda: None))
    registry.register(ToolSpec("empty", "agent-a", "read"))

    with pytest.raises(PermissionError):
        registry.execute("owned", "agent-b")
    with pytest.raises(RuntimeError):
        registry.execute("empty", "agent-a")
    with pytest.raises(KeyError):
        registry.get("unknown")
