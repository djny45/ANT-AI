"""Godmode 10x Governance Approval Flow.

Controls execution lifecycle:
Proposal -> Risk Review -> Approval -> Execution
"""

from dataclasses import dataclass

from ant_common import utc_timestamp


@dataclass
class ApprovalDecision:
    approved: bool
    reason: str
    timestamp: str


class ApprovalFlow:
    def __init__(self, risk_threshold: int = 70):
        self.risk_threshold = risk_threshold

    def evaluate(self, risk_score: int) -> ApprovalDecision:
        allowed = risk_score < self.risk_threshold
        return ApprovalDecision(
            approved=allowed,
            reason="Approved by governance policy" if allowed else "Blocked by risk policy",
            timestamp=utc_timestamp(),
        )
