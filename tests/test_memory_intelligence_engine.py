import unittest

from learning.memory_intelligence_engine import (
    MemoryFitScorer, MemoryIntelligenceEngine, MemoryRecord, MemoryTier,
)


class MemoryFitScorerTests(unittest.TestCase):
    def test_frequently_accessed_important_memory_is_fast(self):
        record = MemoryRecord(
            "hot", "active", importance=1, confidence=1,
            access_count=20, last_accessed_at=1000,
        )
        fit = MemoryFitScorer().score(record, now=1000)
        self.assertEqual(fit.tier, MemoryTier.FAST)

    def test_old_low_value_memory_becomes_cold(self):
        record = MemoryRecord(
            "old", "archive", importance=0, confidence=0,
            access_count=0, last_accessed_at=0,
        )
        fit = MemoryFitScorer().score(record, now=365 * 24 * 3600)
        self.assertEqual(fit.tier, MemoryTier.COLD)


class MemoryIntelligenceEngineTests(unittest.TestCase):
    def test_store_retrieve_and_agent_isolation(self):
        engine = MemoryIntelligenceEngine()
        engine.store(MemoryRecord("a", {"note": "private"}, agent_id="agent-a"))
        self.assertIsNone(engine.retrieve("a", agent_id="agent-b"))
        self.assertIsNotNone(engine.retrieve("a", agent_id="agent-a"))

    def test_rebalance_changes_tiers_without_deleting_records(self):
        engine = MemoryIntelligenceEngine()
        engine.store(MemoryRecord(
            "old", "retained", importance=0, confidence=0,
            last_accessed_at=0,
        ))
        counts = engine.rebalance(now=365 * 24 * 3600)
        self.assertEqual(counts[MemoryTier.COLD.value], 1)
        self.assertIsNotNone(engine.retrieve("old"))

    def test_capacity_archives_instead_of_deleting(self):
        engine = MemoryIntelligenceEngine(max_records=1)
        engine.store(MemoryRecord("older", "keep", importance=0, confidence=0,
                                  last_accessed_at=0))
        engine.store(MemoryRecord("newer", "also keep", importance=1, confidence=1,
                                  access_count=20))
        self.assertEqual(engine.stats()["total_records"], 2)
        self.assertEqual(engine.fit_for("older").tier, MemoryTier.COLD)

    def test_invalid_thresholds_are_rejected(self):
        with self.assertRaises(ValueError):
            MemoryFitScorer(fast_threshold=0.2, working_threshold=0.8)


if __name__ == "__main__":
    unittest.main()
