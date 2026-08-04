"""Enhanced security manager with proper access control."""

import logging
from typing import Set, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SecurityManager:
    """Manages security policies and access control."""
    
    def __init__(self):
        self.allowed = set()  # Allowed actions
        self.denied = set()  # FIX: Explicitly denied actions (default deny)
        self.access_log = []  # FIX: Access audit trail
    
    def allow(self, action: str) -> None:
        """Explicitly allow an action."""
        self.allowed.add(action)
        # Remove from denied if it was there
        self.denied.discard(action)
        self._log_access("ALLOW", action, True)
    
    def deny(self, action: str) -> None:
        """Explicitly deny an action."""
        self.denied.add(action)
        # Remove from allowed if it was there
        self.allowed.discard(action)
        self._log_access("DENY", action, True)
    
    def check(self, action: str) -> bool:
        """Check if action is allowed. FIX: Default deny behavior."""
        # FIX: Explicit deny takes precedence
        if action in self.denied:
            self._log_access("CHECK", action, False)
            return False
        
        # Must be explicitly allowed
        allowed = action in self.allowed
        self._log_access("CHECK", action, allowed)
        return allowed
    
    def check_detailed(self, action: str) -> Dict[str, Any]:
        """Check permission and return detailed result."""
        allowed = self.check(action)
        return {
            "action": action,
            "allowed": allowed,
            "timestamp": datetime.utcnow().isoformat(),
            "reason": "Not in allowed list" if not allowed else "Allowed"
        }
    
    def _log_access(self, operation: str, action: str, result: bool) -> None:
        """Log access attempt."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "action": action,
            "result": result
        }
        self.access_log.append(entry)
        logger.debug(f"Security access log: {entry}")
    
    def get_access_log(self) -> List[Dict[str, Any]]:
        """Retrieve access log."""
        return self.access_log.copy()
