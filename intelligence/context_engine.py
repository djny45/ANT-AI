"""ANT AI context management."""

class ContextEngine:
    def __init__(self, max_context=8000):
        self.max_context = max_context

    def optimize(self, context):
        return context[-self.max_context:]
