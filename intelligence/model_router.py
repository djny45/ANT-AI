"""ANT AI Model Router
Routes tasks between local and cloud models.
"""

class ModelRouter:
    def __init__(self):
        self.providers = {
            "ollama": True,
            "openrouter": True
        }

    def choose_model(self, task_type="general"):
        if task_type == "local":
            return "ollama"
        return "openrouter"

    def fallback(self):
        return "ollama"
