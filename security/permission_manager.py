"""ANT AI permission management with audit logging."""

import logging
from typing import Dict, List, Any

from ant_common import AuditTrail, approval_result

logger = logging.getLogger(__name__)

class PermissionManager:
    """Manages and audits permissions with detailed logging."""
    
    def __init__(self):
        self.permissions: Dict[str, List[str]] = {}
        self.audit = AuditTrail(logger=logger, message_prefix="Permission audit")
        self.permission_cache = {}  # FIX: Cache for performance
    
    @property
    def audit_log(self) -> List[Dict[str, Any]]:
        return self.audit.entries
    
    def grant(self, agent: str, action: str, reason: str = "unspecified") -> None:
        """Grant permission with audit logging."""
        if agent not in self.permissions:
            self.permissions[agent] = []
        
        if action not in self.permissions[agent]:
            self.permissions[agent].append(action)
            self.audit.record(action="GRANT", agent=agent, permission=action, reason=reason)
            self._invalidate_cache(agent)
    
    def revoke(self, agent: str, action: str, reason: str = "security_review") -> None:
        """Revoke permission with audit logging."""
        if agent in self.permissions and action in self.permissions[agent]:
            self.permissions[agent].remove(action)
            self.audit.record(action="REVOKE", agent=agent, permission=action, reason=reason)
            self._invalidate_cache(agent)
    
    def check(self, agent: str, action: str) -> Dict[str, Any]:
        """Check if agent has permission. FIX: Return actual decision."""
        # Check cache first
        cache_key = f"{agent}:{action}"
        if cache_key in self.permission_cache:
            return self.permission_cache[cache_key]
        
        approved = (agent in self.permissions and 
                   action in self.permissions[agent])
        
        result = approval_result(
            approved,
            action=action,
            agent=agent,
            permissions=self.permissions.get(agent, []),
        )
        
        # Cache result
        self.permission_cache[cache_key] = result
        return result
    
    def _invalidate_cache(self, agent: str) -> None:
        """Invalidate cache for agent."""
        keys_to_remove = [k for k in self.permission_cache if k.startswith(f"{agent}:")]
        for key in keys_to_remove:
            del self.permission_cache[key]
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Retrieve audit log."""
        return self.audit.history()
