import json
from typing import Any, Dict

from sqlalchemy import Column, Integer, MetaData, String, Table, Text, create_engine, insert, select


class SQLAlchemyMemoryBackend:
    """SQLAlchemy-backed memory storage for SQLite development or PostgreSQL."""

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        metadata = MetaData()
        self.records = Table(
            "ant_memory_records",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("conversation_id", String(255), nullable=False, index=True),
            Column("item_json", Text, nullable=False),
        )
        metadata.create_all(self.engine)

    def save(self, conversation_id: str, item: Dict[str, Any]) -> None:
        with self.engine.begin() as connection:
            connection.execute(insert(self.records).values(
                conversation_id=conversation_id,
                item_json=json.dumps(item),
            ))

    def load(self, conversation_id: str | None) -> Dict[str, Any]:
        if not conversation_id:
            return {"short_term": []}
        statement = (
            select(self.records.c.item_json)
            .where(self.records.c.conversation_id == conversation_id)
            .order_by(self.records.c.id)
        )
        with self.engine.connect() as connection:
            items = [
                json.loads(item_json)
                for item_json in connection.execute(statement).scalars()
            ]
        return {"short_term": items}


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
