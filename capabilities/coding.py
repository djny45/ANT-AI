import ast
import re
from typing import Any

from .base import BaseCapability


class CodingCapability(BaseCapability):
    capability_name = "Coding Skill"
    execution_target = "coding"
    handler_name = "coding_capability"

    def run(self, *, task: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        request = self.request_text(task, context)
        documents, input_errors = self.input_documents(
            task,
            context,
            ("python_source", "source", "content"),
        )
        if not documents:
            result = {
                "mode": "change_plan",
                "objective": request,
                "steps": [
                    "Inspect the relevant Python modules.",
                    "Implement the requested change with focused edits.",
                    "Run the relevant tests and review the diff.",
                ],
                "risks": [
                    "The plan is request-derived because no Python source was supplied.",
                ],
                "source_inspected": False,
                "headline": "Prepared a request-derived change plan; no Python source was inspected.",
                "skill_metadata": self.skill_metadata(),
            }
            verification = {
                "source_inspected": False,
                "evidence": "No Python source was supplied.",
                "input_errors": input_errors,
            }
            return self.envelope(
                result=result,
                confidence=self.derive_confidence(request, 0, 4),
                verification=verification,
            )

        syntax_errors: list[dict[str, Any]] = []
        functions: list[dict[str, Any]] = []
        classes: list[dict[str, Any]] = []
        long_functions: list[dict[str, Any]] = []
        missing_docstrings: list[dict[str, Any]] = []
        todo_markers: list[dict[str, Any]] = []
        parsed_files = 0

        for document in documents:
            source = document["content"]
            for line_number, line in enumerate(source.splitlines(), start=1):
                marker = re.search(r"\b(TODO|FIXME)\b", line)
                if marker:
                    todo_markers.append({
                        "file": document["name"],
                        "line": line_number,
                        "marker": marker.group(1),
                        "text": line.strip(),
                    })
            try:
                tree = ast.parse(source, filename=document["name"])
            except SyntaxError as error:
                syntax_errors.append({
                    "file": document["name"],
                    "line": error.lineno,
                    "column": error.offset,
                    "message": error.msg,
                })
                continue

            parsed_files += 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    end_line = getattr(node, "end_lineno", node.lineno)
                    inventory = {
                        "file": document["name"],
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": end_line,
                    }
                    functions.append(inventory)
                    if end_line - node.lineno + 1 > 50:
                        long_functions.append({
                            **inventory,
                            "lines": end_line - node.lineno + 1,
                        })
                    if ast.get_docstring(node) is None:
                        missing_docstrings.append({
                            "file": document["name"],
                            "kind": "function",
                            "name": node.name,
                            "line": node.lineno,
                        })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "file": document["name"],
                        "name": node.name,
                        "line": node.lineno,
                    })
                    if ast.get_docstring(node) is None:
                        missing_docstrings.append({
                            "file": document["name"],
                            "kind": "class",
                            "name": node.name,
                            "line": node.lineno,
                        })

        syntax_valid = not syntax_errors
        result = {
            "mode": "source_analysis",
            "source_inspected": True,
            "files_inspected": [document["name"] for document in documents],
            "syntax_valid": syntax_valid,
            "syntax_errors": syntax_errors,
            "functions": functions,
            "classes": classes,
            "over_long_functions": long_functions,
            "todo_markers": todo_markers,
            "missing_docstrings": missing_docstrings,
            "headline": (
                f"Inspected {len(documents)} Python source file(s): "
                f"{len(functions)} function(s), {len(classes)} class(es), "
                f"{len(syntax_errors)} syntax error(s)."
            ),
            "skill_metadata": self.skill_metadata(),
        }
        verification = {
            "source_inspected": True,
            "files_inspected": [document["name"] for document in documents],
            "ast_parsed_files": parsed_files,
            "syntax_valid": syntax_valid,
            "syntax_errors": syntax_errors,
            "input_errors": input_errors,
        }
        concrete_evidence = parsed_files + len(todo_markers) + len(functions)
        return self.envelope(
            result=result,
            confidence=self.derive_confidence(request, concrete_evidence, 4),
            verification=verification,
        )
