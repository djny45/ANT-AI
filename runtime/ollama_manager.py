"""ANT AI local Ollama manager."""

class OllamaManager:
    def __init__(self, endpoint="http://localhost:11434"):
        self.endpoint = endpoint

    def status(self):
        return {
            "engine": "ollama",
            "endpoint": self.endpoint
        }
