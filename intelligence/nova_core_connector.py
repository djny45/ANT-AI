"""NOVA-Core runtime bridge.

ANT remains the control plane. When a NOVA-Core API endpoint is configured,
requests are delegated to NOVA-Core while the user's selected model API
profile is forwarded as request-scoped context. Without an endpoint, ANT
falls back to its native provider-neutral model connector.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


class NovaCoreConnector:
    """Delegate an ANT request to a deployed NOVA-Core API service."""

    def __init__(self, endpoint: str | None = None, timeout: float | None = None):
        self.endpoint = (endpoint or os.getenv("ANT_NOVA_CORE_URL", "")).strip().rstrip("/")
        self.timeout = timeout or float(os.getenv("ANT_MODEL_TIMEOUT", "60"))

    def configured(self) -> bool:
        return bool(self.endpoint)

    def generate(self, prompt: str, model: str, provider: str, api_key: str, base_url: str = "", user_id: str | None = None, conversation_id: str | None = None) -> dict[str, Any]:
        started = time.perf_counter()
        if not self.endpoint:
            return {"runtime": "nova-core", "model": model, "provider": provider, "response": "", "done": False, "error": "NOVA-Core endpoint is not configured"}
        url = self.endpoint if self.endpoint.endswith("/chat") else f"{self.endpoint}/api/chat"
        payload = {
            "user_id": user_id or "anonymous",
            "message": prompt,
            "context": {
                "model_provider": provider,
                "model": model,
                "model_base_url": base_url,
                "model_api_key": api_key,
                "runtime": "nova-core",
                "conversation_id": conversation_id,
            },
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            content = data.get("response") or data.get("output") or data.get("message") or ""
            return {
                "runtime": "nova-core",
                "provider": provider,
                "model": model,
                "response": str(content),
                "done": bool(content),
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "nova": data,
            }
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
            detail = str(exc)
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    detail = exc.read().decode("utf-8")[:1000]
                except OSError:
                    pass
            return {
                "runtime": "nova-core",
                "provider": provider,
                "model": model,
                "response": "",
                "done": False,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "error": detail or type(exc).__name__,
            }
