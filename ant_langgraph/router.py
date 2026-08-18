from typing import Literal

Route = Literal["direct", "coding", "research", "complex"]

CODING = ("code", "coding", "bug", "debug", "repository", "repo", "python", "typescript", "javascript", "api")
RESEARCH = ("research", "investigate", "compare", "information", "study", "analyze")
COMPLEX = ("build", "implement", "integrate", "architecture", "workflow", "multiple", "system", "project")


def route_request(user_input: str) -> Route:
    """Fast deterministic routing used as a safe baseline before model routing."""
    text = " ".join(user_input.lower().split())
    coding_hit = any(k in text for k in CODING)
    research_hit = any(k in text for k in RESEARCH)
    complex_hit = any(k in text for k in COMPLEX)

    if complex_hit and (coding_hit or research_hit):
        return "complex"
    if coding_hit:
        return "coding"
    if research_hit:
        return "research"
    if complex_hit:
        return "complex"
    return "direct"


def routing_features(user_input: str) -> dict[str, bool]:
    """Expose routing signals for metrics, evaluation and future LLM routing."""
    text = user_input.lower()
    return {
        "coding": any(k in text for k in CODING),
        "research": any(k in text for k in RESEARCH),
        "complex": any(k in text for k in COMPLEX),
    }
