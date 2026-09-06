"""NOVA Core configuration foundation."""

DEFAULT_CONFIG = {
    "runtime_mode": "local",
    "memory_enabled": True,
    "learning_enabled": True,
    "logging_level": "INFO",
}


def load_config():
    return DEFAULT_CONFIG.copy()
