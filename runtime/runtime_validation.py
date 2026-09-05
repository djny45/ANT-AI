"""Runtime validation helpers for ANT."""


def validate_runtime(services):
    missing = [service for service in services if service is None]
    return {
        "ready": len(missing) == 0,
        "missing": missing
    }
