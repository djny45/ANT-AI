"""ANT AI model routing layer."""

class ModelOrchestrator:
    def select(self, models, task):
        return {
            "task": task,
            "model": models[0] if models else None
        }
