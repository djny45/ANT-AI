"""Software-side, Memory Fit-inspired tiering for ANT-AI.

This module classifies logical memory records; it does not move physical RAM pages.
It uses only the Python standard library and is safe to use without an external
database. A persistent adapter can be layered behind this manager later.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from threading import RLock
from time import time
from typing import Any, Dict, Iterable, Optional


class MemoryTier(str, Enum):
    FAST = "fast"
    WORKING = "working"
    LONG_TERM = "long_term"
    COLD = "cold"


@dataclass
class MemoryRecord:
    """A memory item plus access and quality signals used for placement."""

    memory_id: str
    payload: Any
    agent_id: Optional[str] = None
    importance: float = 0.5
    confidence: float = 0.5
    access_count: int = 0
    created_at: float = field(default_factory=time)
    last_accessed_at: float = field(default_factory=time)
    tier: MemoryTier = MemoryTier.LONG_TERM
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.importance = _unit(self.importance)
        self.confidence = _unit(self.confidence)
        self.access_count = max(0, int(self.access_count))


@dataclass(frozen=True)
class MemoryFit:
    score: float
    tier: MemoryTier
    reasons: tuple[str, ...]


def _unit(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


class MemoryFitScorer:
    """Ranks records using recency, frequency, importance and confidence."""

    def __init__(self, fast_threshold: float = 0.78,
                 working_threshold: float = 0.58,
                 long_term_threshold: float = 0.30,
                 recency_half_life_seconds: float = 7 * 24 * 3600) -> None:
        if not (0 <= long_term_threshold <= working_threshold <= fast_threshold <= 1):
            raise ValueError("tier thresholds must be ordered between 0 and 1")
        if recency_half_life_seconds <= 0:
            raise ValueError("recency_half_life_seconds must be positive")
        self.fast_threshold = fast_threshold
        self.working_threshold = working_threshold
        self.long_term_threshold = long_term_threshold
        self.recency_half_life_seconds = recency_half_life_seconds

    def score(self, record: MemoryRecord, now: Optional[float] = None) -> MemoryFit:
        current = time() if now is None else float(now)
        age = max(0.0, current - record.last_accessed_at)
        recency = 0.5 ** (age / self.recency_half_life_seconds)
        frequency = min(1.0, record.access_count / 20.0)
        score = (
            0.35 * recency
            + 0.25 * frequency
            + 0.25 * record.importance
            + 0.15 * record.confidence
        )
        reasons = (
            f"recency={recency:.3f}",
            f"frequency={frequency:.3f}",
            f"importance={record.importance:.3f}",
            f"confidence={record.confidence:.3f}",
        )
        if score >= self.fast_threshold:
            tier = MemoryTier.FAST
        elif score >= self.working_threshold:
            tier = MemoryTier.WORKING
        elif score >= self.long_term_threshold:
            tier = MemoryTier.LONG_TERM
        else:
            tier = MemoryTier.COLD
        return MemoryFit(score=round(score, 6), tier=tier, reasons=reasons)


class MemoryIntelligenceEngine:
    """Thread-safe logical tier manager with optional agent-scoped retrieval.

    Tier changes are classifications only. The manager does not silently delete
    data, persist secrets, or claim to control OS/hardware memory placement.
    """

    def __init__(self, scorer: Optional[MemoryFitScorer] = None,
                 max_records: Optional[int] = None) -> None:
        if max_records is not None and max_records < 1:
            raise ValueError("max_records must be at least 1")
        self.scorer = scorer or MemoryFitScorer()
        self.max_records = max_records
        self._records: Dict[str, MemoryRecord] = {}
        self._lock = RLock()

    def store(self, record: MemoryRecord) -> MemoryFit:
        if not record.memory_id:
            raise ValueError("memory_id must not be empty")
        with self._lock:
            fit = self.scorer.score(record)
            record.tier = fit.tier
            self._records[record.memory_id] = record
            self._enforce_capacity()
            return fit

    def retrieve(self, memory_id: str, agent_id: Optional[str] = None) -> Optional[MemoryRecord]:
        with self._lock:
            record = self._records.get(memory_id)
            if record is None or (agent_id is not None and record.agent_id != agent_id):
                return None
            record.access_count += 1
            record.last_accessed_at = time()
            record.tier = self.scorer.score(record).tier
            return record

    def retrieve_all(self, agent_id: Optional[str] = None,
                     tiers: Optional[Iterable[MemoryTier]] = None) -> list[MemoryRecord]:
        allowed = set(tiers) if tiers is not None else None
        with self._lock:
            records = [
                record for record in self._records.values()
                if (agent_id is None or record.agent_id == agent_id)
                and (allowed is None or record.tier in allowed)
            ]
            return sorted(records, key=lambda item: (
                self.scorer.score(item).score, item.last_accessed_at
            ), reverse=True)

    def rebalance(self, now: Optional[float] = None) -> Dict[str, int]:
        """Recalculate tiers without deleting or mutating record payloads."""
        counts = {tier.value: 0 for tier in MemoryTier}
        with self._lock:
            for record in self._records.values():
                fit = self.scorer.score(record, now=now)
                record.tier = fit.tier
                counts[fit.tier.value] += 1
        return counts

    def fit_for(self, memory_id: str, now: Optional[float] = None) -> Optional[MemoryFit]:
        with self._lock:
            record = self._records.get(memory_id)
            return self.scorer.score(record, now=now) if record else None

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            counts = {tier.value: 0 for tier in MemoryTier}
            for record in self._records.values():
                counts[record.tier.value] += 1
            return {"total_records": len(self._records), "tiers": counts,
                    "max_records": self.max_records}

    def _enforce_capacity(self) -> None:
        if self.max_records is None or len(self._records) <= self.max_records:
            return
        # Capacity pressure archives the lowest-fit record; it never deletes it.
        candidates = sorted(
            self._records.values(),
            key=lambda item: self.scorer.score(item).score
        )
        excess = len(self._records) - self.max_records
        for record in candidates[:excess]:
            record.tier = MemoryTier.COLD
