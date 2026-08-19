import re
from typing import Any

from .base import BaseCapability


class SecurityCapability(BaseCapability):
    capability_name = "Security Skill"
    execution_target = "security"
    handler_name = "security_capability"

    def run(self, *, task: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        request = self.request_text(task, context)
        documents, input_errors = self.input_documents(
            task,
            context,
            ("source", "text", "content", "python_source"),
        )
        if not documents:
            result = {
                "mode": "review_checklist",
                "objective": request,
                "checks": [
                    "Inspect dynamic code execution.",
                    "Inspect subprocess and deserialization behavior.",
                    "Inspect transport verification and hardcoded credentials.",
                ],
                "source_inspected": False,
                "headline": "Prepared a request-derived security checklist; nothing was scanned.",
                "skill_metadata": self.skill_metadata(),
            }
            verification = {
                "source_inspected": False,
                "evidence": "Nothing was supplied for security scanning.",
                "input_errors": input_errors,
            }
            return self.envelope(
                result=result,
                confidence=self.derive_confidence(request, 0, 4),
                verification=verification,
            )

        patterns = (
            ("eval_or_exec", re.compile(r"\b(?:eval|exec)\s*\("), "high"),
            (
                "subprocess_shell_true",
                re.compile(r"\bsubprocess\b.*\bshell\s*=\s*True\b"),
                "high",
            ),
            ("pickle_loads", re.compile(r"\bpickle\.loads\s*\("), "high"),
            ("verify_false", re.compile(r"\bverify\s*=\s*False\b"), "medium"),
            (
                "hardcoded_credential",
                re.compile(
                    r"""(?i)\b(?:password|passwd|secret|token|api[_-]?key|access[_-]?key)\s*=\s*(['"]).+?\1"""
                ),
                "high",
            ),
        )
        findings: list[dict[str, Any]] = []
        lines_scanned = 0
        for document in documents:
            for line_number, line in enumerate(document["content"].splitlines(), start=1):
                lines_scanned += 1
                for pattern_name, pattern, severity in patterns:
                    if pattern.search(line):
                        findings.append({
                            "file": document["name"],
                            "line": line_number,
                            "pattern": pattern_name,
                            "severity": severity,
                            "text": line.strip(),
                        })

        result = {
            "mode": "source_scan",
            "source_inspected": True,
            "files_inspected": [document["name"] for document in documents],
            "lines_scanned": lines_scanned,
            "findings": findings,
            "headline": (
                f"Scanned {lines_scanned} source line(s) and found "
                f"{len(findings)} risky pattern(s)."
            ),
            "skill_metadata": self.skill_metadata(),
        }
        verification = {
            "source_inspected": True,
            "files_inspected": [document["name"] for document in documents],
            "lines_scanned": lines_scanned,
            "patterns_checked": [name for name, _, _ in patterns],
            "finding_count": len(findings),
            "input_errors": input_errors,
        }
        return self.envelope(
            result=result,
            confidence=self.derive_confidence(request, lines_scanned, 10),
            verification=verification,
        )
