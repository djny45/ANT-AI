"""Shared shape for permission and validation decisions."""

from typing import Any, Dict

from ant_common.timeutil import utc_timestamp


def approval_result(approved: bool, **fields: Any) -> Dict[str, Any]:
    """Build a timestamped approval decision with review escalation flag."""
    return {
        **fields,
        "approved": approved,
        "review_required": not approved,
        "timestamp": utc_timestamp(),
    }
