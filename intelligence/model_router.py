"""ANT AI model router.

Provider selection is explicit and comes from the active user API profile.
ANT does not impose a hosted model aggregator.
"""


class ModelRouter:
    def choose_provider(self, provider: str = "custom") -> str:
        return (provider or "custom").strip().lower()

    def get_runtime_name(self, provider: str = "custom") -> str:
        return self.choose_provider(provider)

    def fallback(self, provider: str = "custom") -> str:
        return self.choose_provider(provider)
