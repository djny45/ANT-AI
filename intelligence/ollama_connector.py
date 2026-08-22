"""Ollama local model connector used by the unified ANT intelligence core.

The connector intentionally uses Python's standard library so local-model
execution does not introduce another runtime dependency for the prototype.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


class OllamaConnector:
    def __init__(self, url: str | None = None, timeout: float | None = None):
        self.url = (url or os.getenv("OLLAMA_URL", "http://localhost:11434")).rstrip("/")
        self.timeout = timeout or float(os.getenv("OLLAMA_TIMEOUT", "30"))

    def health(self) -> bool:
        try:
            request = urllib.request.Request(f"{self.url}/api/tags", method="GET")
            with urllib.request.urlopen(request, timeout=min(self.timeout, 5)) as response:
                return response.status == 200
        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    def generate(self, prompt: str, model: str | None = None, system: str | None = None) -> dict[str, Any]:
        selected_model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        payload: dict[str, Any] = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        request = urllib.request.Request(
            f"{self.url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            return {
                "provider": "ollama",
                "model": selected_model,
                "response": data.get("response", ""),
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "done": bool(data.get("done", True)),
            }
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            return {
                "provider": "ollama",
                "model": selected_model,
                "response": "",
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "done": False,
                "error": str(exc),
            }
