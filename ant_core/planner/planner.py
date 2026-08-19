class IntelligencePlanner:
    """Deterministic planning layer; an LLM planner can be injected later."""

    def plan(self, goal: str) -> dict[str, object]:
        text = goal.lower()
        tasks: list[dict[str, Any]] = []
        if any(k in text for k in ("code", "bug", "debug", "repository", "repo", "python", "api")):
            tasks.append({"agent": "coding", "objective": "analyze and improve the software"})
        if any(k in text for k in ("research", "investigate", "compare", "information", "analyze")):
            tasks.append({"agent": "research", "objective": "research and structure relevant findings"})
        if any(k in text for k in ("security", "secure", "vulnerability", "permission")):
            tasks.append({"agent": "security", "objective": "review security and operational risk"})
        if any(k in text for k in ("data", "dataset", "sql", "csv", "analytics", "database")):
            tasks.append({"agent": "data", "objective": "analyze and structure relevant data"})
        if not tasks:
            tasks.append({"agent": "master", "objective": "provide a direct response"})
        required_capabilities = [task["agent"] for task in tasks if task["agent"] != "master"]
        complex_markers = ("build", "implement", "integrate", "architecture", "system", "workflow")
        if len(tasks) > 1 or any(marker in text for marker in complex_markers):
            strategy = "multi-agent"
            confidence = 0.90
        elif required_capabilities:
            strategy = "single-specialist"
            confidence = 0.82
        else:
            strategy = "direct-work"
            confidence = 0.70
        return {
            "goal": goal,
            "tasks": tasks,
            "context": {},
            "strategy": strategy,
            "required_capabilities": required_capabilities,
            "confidence": confidence,
        }
