"""Append-only in-memory audit trail."""

import logging
from typing import Any, Dict, List, Optional

from ant_common.timeutil import utc_timestamp


class AuditTrail:
    """Records timestamped entries and optionally forwards them to a logger."""

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        log_level: int = logging.INFO,
        message_prefix: str = "Audit",
    ):
        self.entries: List[Dict[str, Any]] = []
        self.logger = logger
        self.log_level = log_level
        self.message_prefix = message_prefix

    def record(self, **fields: Any) -> Dict[str, Any]:
        """Append an entry with a UTC timestamp and return it."""
        entry = {"timestamp": utc_timestamp(), **fields}
        self.entries.append(entry)
        if self.logger:
            self.logger.log(self.log_level, "%s: %s", self.message_prefix, entry)
        return entry

    def history(self) -> List[Dict[str, Any]]:
        """Return a copy of all recorded entries."""
        return self.entries.copy()

    def clear(self) -> None:
        self.entries.clear()

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)
