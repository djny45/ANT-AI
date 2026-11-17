"""Framework-neutral memory boundary with optional intelligent tier scoring."""
from __future__ import annotations

from time import time
from typing import Any, Dict
from uuid import uuid4

from learning.memory_intelligence_engine import MemoryIntelligenceEngine, MemoryRecord


class MemoryAdapter:
    """Memory boundary for ANT graph executions.

    A supplied durable backend takes precedence. Without one, the adapter uses
    the in-process MemoryIntelligenceEngine and scopes records by conversation
    ID. This preserves the existing short_term response contract.
    """

    def __init__(self, backend: Any | None = None,
                 intelligence_engine: MemoryIntelligenceEngine | None = None):
        self.backend = backend
        self.intelligence_engine = (
            intelligence_engine or MemoryIntelligenceEngine()
            if backend is None else intelligence_engine
        )

    def load(self, conversation_id: str | None,
             max_items: int = 50) -> Dict[str, Any]:
        if not conversation_id:
            return {"short_term": []}
        if self.backend and hasattr(self.backend, "load"):
            return self.backend.load(conversation_id)
        if self.intelligence_engine is not None:
            records = self.intelligence_engine.retrieve_all(agent_id=conversation_id)
            # Preserve chronological context order while limiting the window.
            records.sort(key=lambda record: (record.created_at, record.memory_id))
            selected = records[-max_items:] if max_items else []
            payloads = []
            for record in selected:
                accessed = self.intelligence_engine.retrieve(
                    record.memory_id, agent_id=conversation_id
                )
                if accessed is not None:
                    payloads.append(accessed.payload)
            return {"short_term": payloads}
        return {"short_term": []}

    def save(self, conversation_id: str, item: Dict[str, Any],
             max_items: int = 50) -> None:
        if self.backend and hasattr(self.backend, "save"):
            self.backend.save(conversation_id, item)
            return
        if self.intelligence_engine is None:
            return
        now = time()
        self.intelligence_engine.store(MemoryRecord(
            memory_id=str(uuid4()),
            payload=item,
            agent_id=conversation_id,
            importance=0.65,
            confidence=0.8,
            created_at=now,
            last_accessed_at=now,
            metadata={"memory_kind": "verified_execution"},
        ))

    def stats(self) -> Dict[str, Any]:
        if self.intelligence_engine is None:
            return {"backend": "external", "intelligence_engine": False}
        return self.intelligence_engine.stats()
