"""Remote sandbox client used when the ANT web runtime is deployed separately."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class RemoteSandboxError(RuntimeError):
    """Raised when the configured sandbox service cannot complete an operation."""


class RemoteSandbox:
    """Small authenticated client for the dedicated sandbox service."""

    def __init__(self, execution_id: str, url: str | None = None, token: str | None = None, timeout: float = 10.0):
        self.execution_id = execution_id
        self.url = (url or os.getenv("ANT_SANDBOX_URL", "")).rstrip("/")
        self.token = token or os.getenv("ANT_SANDBOX_TOKEN", "")
        self.timeout = timeout

    def execute(self, operation: str, **kwargs: Any) -> dict[str, Any]:
        if not self.url:
            raise RemoteSandboxError("ANT_SANDBOX_URL is not configured")
        payload = {
            "execution_id": self.execution_id,
            "operation": operation,
            "path": kwargs.get("path"),
            "content": kwargs.get("content"),
        }
        request = urllib.request.Request(
            f"{self.url}/v1/execute",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            detail = str(exc)
            if isinstance(exc, urllib.error.HTTPError):
                try:
                    detail = exc.read().decode("utf-8")[:1000]
                except OSError:
                    pass
            raise RemoteSandboxError(detail) from exc
