"""Adapters that expose MemoryIntelligenceEngine through legacy store APIs."""
from __future__ import annotations

from time import time
from typing import Any, Dict, Optional
from uuid import uuid4

from learning.memory_intelligence_engine import (
    MemoryIntelligenceEngine,
    MemoryRecord,
)


class MemoryIntelligenceStoreAdapter:
    """Compatibility adapter for harness stores with store()/retrieve() methods.

    Payloads remain opaque application data. Agent IDs are enforced by the
    underlying engine when callers request an agent-scoped retrieval.
    """

    def __init__(self, engine: Optional[MemoryIntelligenceEngine] = None,
                 default_agent_id: Optional[str] = None) -> None:
        self.engine = engine or MemoryIntelligenceEngine()
        self.default_agent_id = default_agent_id

    def store(self, payload: Any, *, agent_id: Optional[str] = None,
              importance: float = 0.5, confidence: float = 0.5,
              memory_id: Optional[str] = None) -> str:
        identifier = memory_id or str(uuid4())
        resolved_agent = agent_id if agent_id is not None else self.default_agent_id
        record = MemoryRecord(
            memory_id=identifier,
            payload=payload,
            agent_id=resolved_agent,
            importance=importance,
            confidence=confidence,
            created_at=time(),
            last_accessed_at=time(),
        )
        self.engine.store(record)
        return identifier

    def retrieve(self, limit: int = 5,
                 *, agent_id: Optional[str] = None) -> list[Any]:
        if limit < 0:
            raise ValueError("limit must not be negative")
        resolved_agent = agent_id if agent_id is not None else self.default_agent_id
        records = self.engine.retrieve_all(agent_id=resolved_agent)
        selected = records[:limit]
        # Update access metadata through the engine's public retrieval method.
        refreshed = []
        for record in selected:
            item = self.engine.retrieve(record.memory_id, agent_id=resolved_agent)
            if item is not None:
                refreshed.append(item.payload)
        return refreshed

    def stats(self) -> Dict[str, Any]:
        return self.engine.stats()
