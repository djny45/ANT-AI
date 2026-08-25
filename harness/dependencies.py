"""
ANT AI Harness dependency initialization layer.

Provides centralized creation of runtime dependencies.
"""

from .config import HarnessConfig
from .bootstrap import create_harness_runtime


def initialize_harness():
    """Initialize configured Harness runtime."""
    config = HarnessConfig()
    runtime = create_harness_runtime()

    return {
        "config": config,
        "runtime": runtime,
    }
