"""ANT model routing foundation.

Provides a routing point for future model selection strategies.
"""


class ModelRouter:
    def route(self, task, models):
        if not models:
            return None
        return models[0]
