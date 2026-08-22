from typing import Any


class IntelligencePlanner:
    """Deterministic planner for temporary capabilities formed by ANT Intelligence."""

    def plan(self, request: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        text = request.lower()
        tasks: list[dict[str, Any]] = []

        if any(k in text for k in ("code", "bug", "debug", "repository", "repo", "python", "api")):
            tasks.append({
                "capability": "coding",
                "objective": "analyze and improve the software",
            })
        if any(k in text for k in ("research", "investigate", "compare", "information", "analyze")):
            tasks.append({
                "capability": "research",
                "objective": "research and structure relevant findings",
            })
        if any(k in text for k in ("security", "secure", "vulnerability", "permission")):
            tasks.append({
                "capability": "security",
                "objective": "review security and operational risk",
            })
        if not tasks:
            tasks.append({
                "capability": "direct_reasoning",
                "objective": "provide a direct response",
            })

        return {"goal": request, "tasks": tasks, "context": context or {}}
