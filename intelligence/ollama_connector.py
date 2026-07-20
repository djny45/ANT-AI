"""Ollama local model connector."""

class OllamaConnector:
    def __init__(self, url="http://localhost:11434"):
        self.url = url

    def generate(self, prompt, model="llama"):
        return {
            "provider": "ollama",
            "model": model,
            "prompt": prompt
        }
