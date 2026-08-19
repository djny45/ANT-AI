from pathlib import Path
from typing import Any

from ANT_X_OS.skills.registry import registry as default_registry


class BaseCapability:
    capability_name = ""
    execution_target = ""
    handler_name = ""

    def __init__(self, skill_registry=None):
        self.skill_registry = skill_registry or default_registry

    def __call__(self, *, task: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        return self.run(task=task, context=context)

    def run(self, *, task: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def skill_metadata(self) -> dict[str, Any]:
        skill = self.skill_registry.get(self.capability_name)
        if skill is None:
            return {
                "available": False,
                "name": self.capability_name,
                "description": "",
                "rules": [],
            }
        return {
            "available": True,
            "name": skill.name,
            "description": skill.description,
            "rules": list(skill.rules),
        }

    @staticmethod
    def request_text(task: dict[str, Any], context: dict[str, Any] | None = None) -> str:
        context = context or {}
        return str(
            context.get("request")
            or task.get("objective")
            or task.get("description")
            or task.get("request")
            or ""
        ).strip()

    @staticmethod
    def input_documents(
        task: dict[str, Any],
        context: dict[str, Any],
        keys: tuple[str, ...],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        documents: list[dict[str, str]] = []
        errors: list[dict[str, str]] = []

        def add_document(name: str, content: Any) -> None:
            if isinstance(content, str) and content:
                documents.append({"name": name, "content": content})

        for key in keys:
            add_document(key, task.get(key))
            add_document(key, context.get(key))

        for source in (
            (task.get("files") or {}),
            (context.get("files") or {}),
        ):
            if isinstance(source, dict):
                for name, content in source.items():
                    add_document(str(name), content)

        paths = task.get("file_paths") or context.get("file_paths") or []
        if isinstance(paths, (str, Path)):
            paths = [paths]
        for path_value in paths:
            path = Path(path_value)
            try:
                add_document(str(path), path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as error:
                errors.append({"name": str(path), "error": str(error)})
        return documents, errors

    @staticmethod
    def derive_confidence(
        request: str,
        concrete_evidence: int,
        expected_evidence: int,
    ) -> float:
        request_score = min(len(request.split()) / 12, 1.0)
        if concrete_evidence <= 0:
            return round(0.20 + 0.20 * request_score, 2)
        evidence_score = min(concrete_evidence / max(expected_evidence, 1), 1.0)
        return round(min(0.99, 0.45 + 0.50 * evidence_score + 0.05 * request_score), 2)

    def envelope(
        self,
        *,
        result: dict[str, Any],
        confidence: float,
        verification: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "success": True,
            "capability": self.capability_name,
            "handler": self.handler_name,
            "execution_target": self.execution_target,
            "result": result,
            "confidence": confidence,
            "verification": verification,
        }
