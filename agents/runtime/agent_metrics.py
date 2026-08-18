from dataclasses import dataclass

@dataclass
class AgentMetrics:
    executions: int = 0
    failures: int = 0
    total_latency_ms: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.executions == 0:
            return 0.0
        return (self.executions - self.failures) / self.executions

    @property
    def average_latency_ms(self) -> float:
        return self.total_latency_ms / self.executions if self.executions else 0.0
