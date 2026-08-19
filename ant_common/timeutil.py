"""Timestamp helpers shared by audit, governance and security modules."""

from datetime import datetime, timezone


def utc_timestamp() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()
