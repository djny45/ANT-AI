"""
ANT AI Harness configuration layer.

Centralizes runtime settings for future environment based deployment.
"""

import os


class HarnessConfig:
    """Runtime configuration for the Harness service."""

    def __init__(self):
        self.environment = os.getenv("ANT_ENV", "development")
        self.service_name = os.getenv("ANT_SERVICE_NAME", "ANT AI Harness")
        self.debug = os.getenv("ANT_DEBUG", "false").lower() == "true"


config = HarnessConfig()
