"""Security gateway for connector validation and permission enforcement."""

import logging
from typing import Dict, Any, List

from ant_common import AuditTrail, approval_result

logger = logging.getLogger(__name__)

class SecurityGateway:
    """Validates connectors before allowing connections."""
    
    def __init__(self):
        self.approved_connectors = set()  # FIX: Track approved connectors
        self.audit = AuditTrail(logger=logger, message_prefix="Connector validation")
        self.required_permissions = {
            'network': ['read_only', 'write', 'execute'],
            'file': ['read_only', 'write', 'delete'],
            'system': ['read_only', 'execute']
        }
    
    @property
    def validation_log(self) -> List[Dict[str, Any]]:
        return self.audit.entries
    
    def validate(self, connector: str, permissions: List[str]) -> Dict[str, Any]:
        """Validate connector and permissions. FIX: Actual validation logic."""
        
        # Check if connector is approved
        is_approved = connector in self.approved_connectors
        
        # Validate permissions
        valid_permissions = self._validate_permissions(connector, permissions)
        
        # FIX: Return actual decision instead of always pending
        result = approval_result(
            is_approved and valid_permissions,
            connector=connector,
            permissions=permissions,
            validation_details={
                "connector_approved": is_approved,
                "permissions_valid": valid_permissions
            },
        )
        
        self.audit.record(connector=connector, approved=result['approved'])
        return result
    
    def approve_connector(self, connector: str) -> None:
        """Approve a connector for use."""
        self.approved_connectors.add(connector)
        logger.info(f"Connector approved: {connector}")
    
    def revoke_connector(self, connector: str) -> None:
        """Revoke approval for a connector."""
        self.approved_connectors.discard(connector)
        logger.warning(f"Connector revoked: {connector}")
    
    def _validate_permissions(self, connector: str, permissions: List[str]) -> bool:
        """Validate that requested permissions are reasonable."""
        # Get connector type from name (simplified)
        for perm in permissions:
            if perm not in ['read_only', 'write', 'execute', 'delete']:
                return False
        return True
