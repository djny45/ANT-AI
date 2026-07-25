"""OpenRouter model gateway connector."""

import os

class OpenRouterConnector:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")

    def generate(self, prompt, model="free"):
        return {
            "provider": "openrouter",
            "model": model,
            "prompt": prompt
        }
