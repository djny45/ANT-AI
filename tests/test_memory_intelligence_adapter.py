import unittest

from harness.memory_intelligence_adapter import MemoryIntelligenceStoreAdapter
from learning.memory_intelligence_engine import MemoryIntelligenceEngine


class MemoryIntelligenceAdapterTests(unittest.TestCase):
    def test_legacy_store_retrieve_contract(self):
        store = MemoryIntelligenceStoreAdapter()
        store.store({"request": "hello", "result": "world"})
        self.assertEqual(store.retrieve(limit=1), [
            {"request": "hello", "result": "world"}
        ])

    def test_default_agent_scope_isolation(self):
        engine = MemoryIntelligenceEngine()
        store_a = MemoryIntelligenceStoreAdapter(engine, default_agent_id="a")
        store_b = MemoryIntelligenceStoreAdapter(engine, default_agent_id="b")
        store_a.store("private to a")
        self.assertEqual(store_b.retrieve(), [])
        self.assertEqual(store_a.retrieve(), ["private to a"])

    def test_explicit_agent_override(self):
        store = MemoryIntelligenceStoreAdapter()
        store.store("agent a", agent_id="a")
        store.store("agent b", agent_id="b")
        self.assertEqual(store.retrieve(agent_id="a"), ["agent a"])

    def test_negative_limit_rejected(self):
        store = MemoryIntelligenceStoreAdapter()
        with self.assertRaises(ValueError):
            store.retrieve(limit=-1)


if __name__ == "__main__":
    unittest.main()
