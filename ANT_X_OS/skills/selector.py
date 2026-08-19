"""Skill selector maps tasks to required skills."""
from typing import Any

from .registry import registry as default_registry


class SkillSelector:
    def __init__(self, registry=None):
        self.registry = registry or default_registry

    def select_for_task(self, task: dict[str, Any]) -> list[str]:
        return [selection["capability"] for selection in self.select_capabilities_for_task(task)]

    def select_capabilities_for_task(self, task: dict[str, Any]) -> list[dict[str, Any]]:
        """Return selected capabilities and the evidence for each selection."""
        text = ""
        task_type = ""
        if isinstance(task, dict):
            task_type = str(task.get("type", "")).lower().strip()
            text = (task_type + " " + task.get("description", "")).lower()
        else:
            text = str(task).lower()

        rules = (
            (
                ("code", "implement", "feature"),
                "Coding Skill",
                "coding",
                "The request describes software implementation work.",
                0.95,
            ),
            (
                ("bug", "fix", "error", "debug"),
                "Debugging Skill",
                "coding",
                "The request describes diagnosis or defect remediation.",
                0.92,
            ),
            (
                ("research", "investigate", "compare", "information", "study"),
                "Research Skill",
                "research",
                "The request asks for investigation or structured findings.",
                0.90,
            ),
            (
                ("security", "secure", "vulnerability", "permission"),
                "Security Skill",
                "security",
                "The request identifies security or access concerns.",
                0.94,
            ),
            (
                ("data", "dataset", "sql", "csv", "analytics", "database"),
                "Data Skill",
                "data",
                "The request involves data, analytics, or structured datasets.",
                0.91,
            ),
            (
                ("deploy", "release", "rollback"),
                "Deployment Skill",
                "deployment",
                "The request concerns release or rollback operations.",
                0.90,
            ),
            (
                ("design", "architecture", "plan"),
                "Think Before Coding",
                "planning",
                "The request calls for design or architectural planning.",
                0.84,
            ),
        )
        selections: list[dict[str, Any]] = []
        selected_names: set[str] = set()
        family_capabilities = {
            "coding": (
                "Coding Skill",
                "coding",
                "The planner assigned the coding capability family.",
                0.96,
            ),
            "research": (
                "Research Skill",
                "research",
                "The planner assigned the research capability family.",
                0.96,
            ),
            "security": (
                "Security Skill",
                "security",
                "The planner assigned the security capability family.",
                0.96,
            ),
            "data": (
                "Data Skill",
                "data",
                "The planner assigned the data capability family.",
                0.96,
            ),
            "master": (
                "Think Before Coding",
                "master",
                "The planner assigned the master capability family.",
                0.70,
            ),
        }
        if task_type in family_capabilities:
            capability, target, reason, confidence = family_capabilities[task_type]
            if self.registry.get(capability):
                selections.append({
                    "capability": capability,
                    "reason": reason,
                    "confidence": confidence,
                    "execution_target": target,
                })
                selected_names.add(capability)
        for keywords, capability, target, reason, confidence in rules:
            if (
                any(keyword in text for keyword in keywords)
                and capability not in selected_names
                and self.registry.get(capability)
            ):
                selections.append({
                    "capability": capability,
                    "reason": reason,
                    "confidence": confidence,
                    "execution_target": target,
                })
                selected_names.add(capability)

        if not selections and self.registry.get("Think Before Coding"):
            selections.append({
                "capability": "Think Before Coding",
                "reason": "No specialized capability keyword matched; use the safe planning fallback.",
                "confidence": 0.40,
                "execution_target": "master",
            })
        return selections
