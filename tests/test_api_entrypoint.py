import asyncio
import importlib


def test_vercel_api_entrypoint_imports_and_health():
    """The Vercel Python entrypoint must import cleanly and expose health."""
    module = importlib.import_module("api.chat")
    result = asyncio.run(module.health())

    assert result["status"] == "ok"
    assert result["service"] == "ant-ai-api"
    assert result["provider"] == "user-selected"
    assert result["version"] == "0.3.0"
    assert "sandbox" in result
    assert "sandbox_configured" in result
