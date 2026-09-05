"""Execution metrics for ANT resilient runtime."""

from dataclasses import dataclass, field
from time import time


@dataclass
class ExecutionMetrics:
    started_at: float = field(default_factory=time)
    completed_at: float | None = None
    success_count: int = 0
    failure_count: int = 0
    recovery_count: int = 0

    def record_success(self):
        self.success_count += 1
        self.completed_at = time()

    def record_failure(self):
        self.failure_count += 1
        self.completed_at = time()

    def record_recovery(self):
        self.recovery_count += 1

    def snapshot(self):
        return {
            "success": self.success_count,
            "failure": self.failure_count,
            "recovery": self.recovery_count,
            "duration": (time() - self.started_at),
        }
