"""ANT AI model router.

ANT uses OpenRouter as its hosted model transport.
"""


class ModelRouter:
    def __init__(self):
        self.provider = "openrouter"

    def choose_provider(self):
        return "openrouter"

    def get_runtime_name(self):
        return "openrouter"

    def fallback(self):
        return "openrouter"
