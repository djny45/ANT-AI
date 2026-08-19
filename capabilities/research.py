import re
from typing import Any

from .base import BaseCapability


class ResearchCapability(BaseCapability):
    capability_name = "Research Skill"
    execution_target = "research"
    handler_name = "research_capability"

    def run(self, *, task: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        request = self.request_text(task, context)
        clauses = [
            clause.strip()
            for clause in re.split(r"\s+(?:and|or)\s+|[,;]", request)
            if clause.strip()
        ]
        sub_questions = [
            {
                "source": "request",
                "question": f"What evidence addresses: {clause}?",
            }
            for clause in clauses
        ]
        memory_context = context.get("memory_context") or {}
        memory_items = memory_context.get("short_term", [])
        findings = [
            {"source": "memory", "item": item}
            for item in memory_items
        ]
        request_evidence = {
            "source": "request",
            "item": request,
        }
        result = {
            "mode": "structured_research",
            "sub_questions": sub_questions,
            "findings": findings,
            "request_evidence": request_evidence,
            "open_questions": [
                {
                    "source": "request",
                    "question": question["question"],
                }
                for question in sub_questions
            ],
            "next_steps": [
                {
                    "source": "request",
                    "step": "Gather evidence for each request-derived sub-question.",
                },
                {
                    "source": "memory",
                    "step": "Compare findings with the supplied memory context.",
                },
            ],
            "attributions": {
                "memory_items": len(memory_items),
                "request_items": 1 + len(sub_questions),
            },
            "headline": (
                f"Structured {len(sub_questions)} request sub-question(s) with "
                f"{len(memory_items)} memory item(s)."
            ),
            "skill_metadata": self.skill_metadata(),
        }
        verification = {
            "request_used": bool(request),
            "memory_items_inspected": len(memory_items),
            "attribution_sources": ["request", "memory"],
            "external_sources_used": 0,
        }
        concrete_evidence = 1 + len(memory_items) + len(sub_questions)
        return self.envelope(
            result=result,
            confidence=self.derive_confidence(request, concrete_evidence, 6),
            verification=verification,
        )
