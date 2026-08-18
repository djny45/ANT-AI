from typing import Any, Dict


class MemoryAdapter:
    """Framework-neutral memory boundary for existing ANT_X_OS memory services."""

    def __init__(self, backend: Any | None = None):
        self.backend = backend
        self._short_term: Dict[str, list] = {}

    def load(self, conversation_id: str | None) -> Dict[str, Any]:
        if not conversation_id:
            return {"short_term": []}
        if self.backend and hasattr(self.backend, "load"):
            return self.backend.load(conversation_id)
        return {"short_term": self._short_term.get(conversation_id, [])}

    def save(self, conversation_id: str, item: Dict[str, Any]) -> None:
        if self.backend and hasattr(self.backend, "save"):
            self.backend.save(conversation_id, item)
            return
        self._short_term.setdefault(conversation_id, []).append(item)
