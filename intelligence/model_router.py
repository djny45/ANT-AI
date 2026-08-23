"""ANT AI unified model router.

ANT remains one intelligence. This layer only selects the model transport.
"""

import os


class ModelRouter:
    def __init__(self):
        self.provider = os.getenv("ANT_MODEL_PROVIDER", "ollama").strip().lower()

    def choose_provider(self):
        if self.provider in {"omniroute", "ollama"}:
            return self.provider
        return "ollama"

    def get_runtime_name(self):
        return self.choose_provider()

    def fallback(self):
        return "ollama"
