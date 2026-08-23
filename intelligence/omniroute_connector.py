"""OmniRoute OpenAI-compatible model gateway connector for ANT AI.

OmniRoute acts as a routing layer between ANT Intelligence and model providers.
It does not create additional intelligence or agents.
"""

import os
import time
from typing import Any, Dict

import requests


class OmniRouteConnector:
    """Connect ANT model runtime to an OmniRoute gateway."""

    def __init__(self):
        self.base_url = os.getenv(
            "OMNIROUTE_BASE_URL",
            "http://localhost:20128/v1",
        )
        self.api_key = os.getenv("OMNIROUTE_API_KEY", "")
        self.model = os.getenv("ANT_DEFAULT_MODEL", "auto")

    def generate(self, prompt: str, model: str | None = None, **kwargs) -> Dict[str, Any]:
        start = time.time()

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model or self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()

        return {
            "response": data["choices"][0]["message"]["content"],
            "model": data.get("model", model or self.model),
            "latency_ms": (time.time() - start) * 1000,
            "done": True,
        }
