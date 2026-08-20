"""
ANT AI Risk Assessment Engine

Reviews proposed operations before execution.
Designed as a safety and reliability control, not an autonomous executor.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class RiskReport:
    score: int
    risks: List[str]
    approved: bool


class RiskEngine:
    def __init__(self, threshold: int = 70):
        self.threshold = threshold

    def analyze(self, proposal: str) -> RiskReport:
        risks = []
        score = 100

        checks = {
            "secret": "Possible secret exposure detected",
            "delete": "Destructive operation detected",
            "production": "Production impact detected",
            "bypass": "Security bypass detected",
        }

        text = proposal.lower()
        for key, message in checks.items():
            if key in text:
                risks.append(message)
                score -= 20

        return RiskReport(
            score=max(score, 0),
            risks=risks,
            approved=score >= self.threshold,
        )
