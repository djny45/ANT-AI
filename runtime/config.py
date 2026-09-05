"""ANT Runtime Configuration"""

DEFAULT_CONFIG = {
    "runtime": "ant",
    "verification_enabled": True,
    "memory_enabled": True
}


def get_config():
    return DEFAULT_CONFIG.copy()
