"""Provider-agnostic model API connector.

ANT accepts user-supplied API credentials directly. Providers that expose the
OpenAI-compatible chat-completions contract work with a custom endpoint; a few
major native APIs have small protocol adapters here.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable


class ModelApiConnector:
    """Call a user-selected model provider with a user-supplied API key."""

    PROVIDER_DEFAULTS = {
        "openai": "https://api.openai.com/v1",
        "anthropic": "https://api.anthropic.com/v1",
        "google": "https://generativelanguage.googleapis.com/v1beta",
        "gemini": "https://generativelanguage.googleapis.com/v1beta",
        "groq": "https://api.groq.com/openai/v1",
        "mistral": "https://api.mistral.ai/v1",
        "deepseek": "https://api.deepseek.com/v1",
        "together": "https://api.together.xyz/v1",
        "fireworks": "https://api.fireworks.ai/inference/v1",
        "xai": "https://api.x.ai/v1",
        "perplexity": "https://api.perplexity.ai",
        "cerebras": "https://api.cerebras.ai/v1",
    }

    NATIVE_PROVIDERS = {"anthropic", "google", "gemini"}

    def __init__(self, api_key: str | None = None, provider: str = "custom", model: str = "", base_url: str | None = None, timeout: float | None = None):
        self.api_key = (api_key or "").strip()
        self.provider = (provider or "custom").strip().lower()
        self.default_model = (model or "").strip()
        configured_base = (base_url or "").strip()
        self.base_url = configured_base or self.PROVIDER_DEFAULTS.get(self.provider, "")
        self.timeout = timeout or float(os.getenv("ANT_MODEL_TIMEOUT", "60"))

    def configured(self) -> bool:
        return bool(self.api_key and self.default_model and self.base_url)

    def health(self) -> bool:
        return self.configured()

    def _url(self, suffix: str) -> str:
        base = self.base_url.rstrip("/")
        return base if base.endswith(suffix) else f"{base}/{suffix.lstrip('/')}"

    @staticmethod
    def _extract_openai(data: dict[str, Any]) -> str:
        choices = data.get("choices") or []
        if not choices:
            return ""
        content = (choices[0].get("message") or {}).get("content") or ""
        if isinstance(content, list):
            return "".join(str(part.get("text", "")) for part in content if isinstance(part, dict))
        return str(content)

    @staticmethod
    def _extract_anthropic(data: dict[str, Any]) -> str:
        return "".join(str(block.get("text", "")) for block in (data.get("content") or []) if isinstance(block, dict) and block.get("type") == "text")

    @staticmethod
    def _extract_google(data: dict[str, Any]) -> str:
        parts: list[str] = []
        for candidate in data.get("candidates") or []:
            for part in (candidate.get("content") or {}).get("parts") or []:
                if isinstance(part, dict) and part.get("text"):
                    parts.append(str(part["text"]))
        return "".join(parts)

    @staticmethod
    def _flatten_messages(messages: list[dict[str, Any]]) -> str:
        return "\n\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages)

    def _request(self, messages: list[dict[str, Any]], model: str, tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        if self.provider in {"google", "gemini"}:
            url = self._url(f"models/{urllib.parse.quote(model, safe='')}:generateContent")
            payload = {"contents": [{"role": "user", "parts": [{"text": self._flatten_messages(messages)}]}]}
            headers = {"Content-Type": "application/json"}
            url += ("&" if "?" in url else "?") + "key=" + urllib.parse.quote(self.api_key)
        elif self.provider == "anthropic":
            url = self._url("messages")
            system = "\n\n".join(m["content"] for m in messages if m.get("role") == "system")
            payload = {"model": model, "max_tokens": 4096, "messages": [m for m in messages if m.get("role") != "system"]}
            if system:
                payload["system"] = system
            headers = {"Content-Type": "application/json", "x-api-key": self.api_key, "anthropic-version": "2023-06-01"}
        else:
            url = self._url("chat/completions")
            payload = {"model": model, "messages": messages, "stream": False}
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def _extract(self, data: dict[str, Any]) -> str:
        if self.provider in {"google", "gemini"}:
            return self._extract_google(data)
        if self.provider == "anthropic":
            return self._extract_anthropic(data)
        return self._extract_openai(data)

    def generate(self, prompt: str, model: str | None = None, system: str | None = None) -> dict[str, Any]:
        selected_model = (model or self.default_model).strip()
        started = time.perf_counter()
        if not self.api_key:
            return self._error(selected_model, "API key is not configured", started)
        if not selected_model:
            return self._error(selected_model, "Model is not configured", started)
        if not self.base_url:
            return self._error(selected_model, "Model API endpoint is not configured", started)
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        try:
            data = self._request(messages, selected_model)
            content = self._extract(data)
            return {"provider": self.provider, "model": selected_model, "response": content, "latency_ms": round((time.perf_counter() - started) * 1000, 2), "done": bool(content)}
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
            return self._error(selected_model, self._detail(exc), started)

    def generate_with_tools(self, prompt: str, model: str | None, tools: list[dict[str, Any]], tool_executor: Callable[[str, dict[str, Any]], dict[str, Any]], system: str | None = None, max_tool_calls: int = 6) -> dict[str, Any]:
        if self.provider in self.NATIVE_PROVIDERS:
            return self.generate(prompt, model=model, system=system)
        selected_model = (model or self.default_model).strip()
        started = time.perf_counter()
        if not self.api_key:
            return self._error(selected_model, "API key is not configured", started, 0)
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
                    raise ValueError("Model API returned no choices")
                message = choices[0].get("message") or {}
                tool_calls = message.get("tool_calls") or []
                if not tool_calls:
                    content = self._extract_openai(data)
                    return {"provider": self.provider, "model": selected_model, "response": content, "tool_calls": calls, "latency_ms": round((time.perf_counter() - started) * 1000, 2), "done": bool(content)}
                if calls + len(tool_calls) > max_tool_calls:
                    return {"provider": self.provider, "model": selected_model, "response": message.get("content") or "Tool-call limit reached before final response.", "tool_calls": calls, "latency_ms": round((time.perf_counter() - started) * 1000, 2), "done": False, "error": "sandbox tool-call limit reached"}
                messages.append(message)
                for call in tool_calls:
                    function = call.get("function") or {}
                    name = str(function.get("name", ""))
                    raw_arguments = function.get("arguments") or "{}"
                    arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
                    result = tool_executor(name, arguments)
                    calls += 1
                    messages.append({"role": "tool", "tool_call_id": call.get("id", f"tool-{calls}"), "content": json.dumps(result, ensure_ascii=False)})
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
            return self._error(selected_model, self._detail(exc), started, calls)

    def _error(self, model: str, detail: str, started: float, tool_calls: int | None = None) -> dict[str, Any]:
        result = {"provider": self.provider, "model": model, "response": "", "latency_ms": round((time.perf_counter() - started) * 1000, 2), "done": False, "error": detail}
        if tool_calls is not None:
            result["tool_calls"] = tool_calls
        return result

    @staticmethod
    def _detail(exc: Exception) -> str:
        detail = str(exc)
        if isinstance(exc, urllib.error.HTTPError):
            try:
                detail = exc.read().decode("utf-8")[:1000]
            except OSError:
                pass
        return detail or type(exc).__name__
