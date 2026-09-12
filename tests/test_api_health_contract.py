import asyncio
import importlib


def test_vercel_health_contract_is_stable():
    """Keep the public health response safe and stable for deployment checks."""
    module = importlib.import_module("api.chat")
    result = asyncio.run(module.health())

    assert result["status"] == "ok"
    assert result["service"] == "ant-ai-api"
    assert result["provider"] == "openrouter"
    assert result["version"] == "0.2.1"
    assert result["sandbox"] in {"local-bounded", "remote"}
    assert isinstance(result["sandbox_configured"], bool)
    assert "api_key" not in result
    assert "token" not in result
