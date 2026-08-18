from typing import Literal

Route = Literal["direct", "coding", "research", "complex"]


def route_request(user_input: str) -> Route:
    """Deterministic first-pass routing; an LLM router can refine this later."""
    text = user_input.lower().strip()
    coding = ("code", "coding", "bug", "debug", "repository", "repo", "python", "typescript", "javascript", "api")
    research = ("research", "analyze", "compare", "investigate", "find information", "study")
    complex_markers = ("build", "implement", "integrate", "architecture", "workflow", "multiple", "system")

    if any(k in text for k in coding):
        return "complex" if any(k in text for k in complex_markers) else "coding"
    if any(k in text for k in research):
        return "complex" if any(k in text for k in complex_markers) else "research"
    return "complex" if any(k in text for k in complex_markers) else "direct"
