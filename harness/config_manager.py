"""
ANT AI configuration management layer.

Provides centralized runtime configuration access without coupling
services to deployment environments.
"""

import os
from typing import Dict, Any


class ConfigManager:
    """Loads and exposes runtime configuration values."""

    def get(self, key: str, default: Any = None) -> Any:
        return os.getenv(key, default)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "environment": self.get("ANT_ENV", "development"),
            "runtime": self.get("ANT_RUNTIME", "default"),
        }
