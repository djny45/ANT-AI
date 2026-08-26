"""ANT AI Harness memory context integration layer.

Provides controlled context retrieval and storage around runtime execution.
Keeps memory implementation independent from orchestration and runtime logic.
"""


class MemoryContextManager:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    def get_context(self, request):
        """Retrieve relevant execution context before runtime execution."""
        return self.memory_store.retrieve()

    def save_context(self, request, result):
        """Persist execution context after runtime completion."""
        self.memory_store.store({
            "request": request,
            "result": result,
        })
