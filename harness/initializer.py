"""
ANT AI Harness initialization layer.

Connects configuration and dependencies during service startup.
"""

from .config import HarnessConfig
from .dependencies import initialize_dependencies


def initialize_harness():
    """Initialize the Harness runtime dependencies."""
    config = HarnessConfig()
    dependencies = initialize_dependencies(config)
    return {
        "config": config,
        "dependencies": dependencies,
    }
