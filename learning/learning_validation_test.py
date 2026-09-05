"""Validation checks for learning loop integration."""

from learning.adaptive_memory_manager import AdaptiveMemoryManager


def test_memory_cycle():
    memory = AdaptiveMemoryManager()
    memory.store({"task": "sample", "score": 1})
    assert len(memory.retrieve()) == 1
