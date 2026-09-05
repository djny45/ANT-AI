"""ANT bottleneck detection foundation."""


def detect_bottlenecks(metrics=None):
    return {
        "metrics_available": metrics is not None,
        "bottlenecks": [],
        "status": "detection_ready",
    }
