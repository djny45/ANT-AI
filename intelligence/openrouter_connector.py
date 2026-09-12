"""OpenRouter model connector for the unified ANT intelligence core.

Uses OpenRouter's OpenAI-compatible chat-completions endpoint without adding a
new Python dependency. Secrets are read only from environment variables.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Callable


class OpenRouterConnector:
    """Hosted model runtime used by one ANT intelligence execution."""

    DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
    DEFAULT_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str | None = None, timeout: float | None = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.url = os.getenv("OPENROUTER_URL", self.DEFAULT_URL).rstrip("/")
        self.timeout = timeout or float(os.getenv("OPENROUTER_TIMEOUT", "60"))
        self.default_model = os.getenv("OPENROUTER_MODEL", self.DEFAULT_MODEL)

    def configured(self) -> bool:
        return bool(self.api_key)

    def health(self) -> bool:
        """Return whether the connector has credentials configured.

        This intentionally avoids a paid/free probe request.
        """
        return self.configured()

    def _request(self, messages: list[dict[str, Any]], model: str, tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
                "X-Title": os.getenv("OPENROUTER_APP_NAME", "ANT AI"),
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        system: str | None = None,
    ) -> dict[str, Any]:
        selected_model = model or self.default_model
        started = time.perf_counter()

        if not self.api_key:
            return {
                "provider": "openrouter",
                "model": selected_model,
                "response": "",
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "done": False,
                "error": "OPENROUTER_API_KEY is not configured",
            }

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            data = self._request(messages, selected_model)
            choices = data.get("choices") or []
            content = ""
            if choices:
                message = choices[0].get("message") or {}
                content = message.get("content") or ""
            return {
                "provider": "openrouter",
                "model": selected_model,
                "response": content,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "done": bool(content),
            }
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            detail = str(exc)
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    detail = exc.read().decode("utf-8")[:1000]
                except OSError:
                    pass
            return {
                "provider": "openrouter",
                "model": selected_model,
                "response": "",
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "done": False,
                "error": detail,
            }

    def generate_with_tools(
        self,
        prompt: str,
        model: str | None,
        tools: list[dict[str, Any]],
        tool_executor: Callable[[str, dict[str, Any]], dict[str, Any]],
        system: str | None = None,
        max_tool_calls: int = 6,
    ) -> dict[str, Any]:
        """Run a bounded tool-calling loop and return the final model response."""
        selected_model = model or self.default_model
        started = time.perf_counter()
        if not self.api_key:
            return {
                "provider": "openrouter",
                "model": selected_model,
                "response": "",
                "tool_calls": 0,
                "latency_ms": 0.0,
                "done": False,
                "error": "OPENROUTER_API_KEY is not configured",
            }

        messages: list[dict[str, Any]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        calls = 0

        try:
            while True:
                data = self._request(messages, selected_model, tools=tools)
                choices = data.get("choices") or []
                if not choices:
                    raise ValueError("OpenRouter returned no choices")
                message = choices[0].get("message") or {}
                tool_calls = message.get("tool_calls") or []
                if not tool_calls:
                    content = message.get("content") or ""
                    return {
                        "provider": "openrouter",
                        "model": selected_model,
                        "response": content,
                        "tool_calls": calls,
                        "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                        "done": bool(content),
                    }

                if calls + len(tool_calls) > max_tool_calls:
                    return {
                        "provider": "openrouter",
                        "model": selected_model,
                        "response": message.get("content") or "Tool-call limit reached before final response.",
                        "tool_calls": calls,
                        "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                        "done": False,
                        "error": "sandbox tool-call limit reached",
                    }

                messages.append(message)
                for call in tool_calls:
                    function = call.get("function") or {}
                    name = str(function.get("name", ""))
                    raw_arguments = function.get("arguments") or "{}"
                    arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
                    result = tool_executor(name, arguments)
                    calls += 1
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.get("id", f"tool-{calls}"),
                        "content": json.dumps(result, ensure_ascii=False),
                    })
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
            detail = str(exc)
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    detail = exc.read().decode("utf-8")[:1000]
                except OSError:
                    pass
            return {
                "provider": "openrouter",
                "model": selected_model,
                "response": "",
                "tool_calls": calls,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "done": False,
                "error": detail,
            }
