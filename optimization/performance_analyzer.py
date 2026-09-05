"""ANT performance analyzer foundation."""


def analyze_execution(trace=None):
    return {
        "trace_available": trace is not None,
        "status": "analysis_ready",
    }
