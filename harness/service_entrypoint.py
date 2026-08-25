"""
ANT AI Harness service entrypoint.

Provides a single startup entry for initializing the Harness runtime.
"""

from .initializer import initialize_harness


def start_harness_service():
    """Initialize and return the Harness service runtime."""
    return initialize_harness()
