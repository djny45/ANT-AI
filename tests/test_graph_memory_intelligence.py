from ant_langgraph.memory import MemoryAdapter
from learning.memory_intelligence_engine import MemoryIntelligenceEngine, MemoryTier


def test_graph_memory_adapter_uses_intelligence_engine():
    engine = MemoryIntelligenceEngine()
    memory = MemoryAdapter(intelligence_engine=engine)
    item = {"execution_id": "e1", "response": "verified"}
    memory.save("conversation-a", item)

    loaded = memory.load("conversation-a")
    assert loaded == {"short_term": [item]}
    assert memory.stats()["total_records"] == 1


def test_graph_memory_isolation_between_conversations():
    memory = MemoryAdapter()
    memory.save("conversation-a", {"response": "private a"})
    memory.save("conversation-b", {"response": "private b"})

    assert memory.load("conversation-a")["short_term"] == [{"response": "private a"}]
    assert memory.load("conversation-b")["short_term"] == [{"response": "private b"}]
    assert memory.load(None) == {"short_term": []}


def test_external_backend_keeps_precedence():
    class Backend:
        def __init__(self):
            self.data = {}

        def load(self, key):
            return self.data.get(key, {"short_term": []})

        def save(self, key, value):
            self.data.setdefault(key, {"short_term": []})["short_term"].append(value)

    backend = Backend()
    memory = MemoryAdapter(backend=backend)
    memory.save("c", {"response": "backend"})
    assert memory.load("c")["short_term"] == [{"response": "backend"}]
    assert memory.stats()["backend"] == "external"
