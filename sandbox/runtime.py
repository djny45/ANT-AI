"""Bounded workspace sandbox used by ANT tool execution.

The default runtime intentionally does not execute arbitrary shell commands.
It provides isolated per-run files and Python syntax validation. A production
process-execution deployment should run behind the remote sandbox service.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path
from uuid import uuid4


class SandboxError(ValueError):
    """Raised when a sandbox operation violates its workspace policy."""


class SkillSandbox:
    """Per-execution, path-confined workspace for ANT capabilities."""

    MAX_FILE_BYTES = 256 * 1024
    MAX_FILES = 100

    def __init__(self, execution_id: str | None = None, root: str | None = None):
        base = Path(root or os.getenv("ANT_SANDBOX_ROOT", "/tmp/ant-sandbox"))
        base.mkdir(parents=True, exist_ok=True)
        run_id = execution_id or str(uuid4())
        self.root = (base / run_id).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, relative: str) -> Path:
        if not relative or relative.startswith("/"):
            raise SandboxError("sandbox paths must be relative")
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise SandboxError("path escapes sandbox workspace")
        return candidate

    def list_files(self) -> list[str]:
        return sorted(
            str(path.relative_to(self.root))
            for path in self.root.rglob("*")
            if path.is_file()
        )

    def read_file(self, path: str) -> str:
        target = self._path(path)
        if not target.is_file():
            raise SandboxError("file does not exist")
        if target.stat().st_size > self.MAX_FILE_BYTES:
            raise SandboxError("file exceeds sandbox size limit")
        return target.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> dict[str, object]:
        encoded = content.encode("utf-8")
        if len(encoded) > self.MAX_FILE_BYTES:
            raise SandboxError("file exceeds sandbox size limit")
        target = self._path(path)
        if not target.exists() and len(self.list_files()) >= self.MAX_FILES:
            raise SandboxError("sandbox file limit reached")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encoded)
        return {"path": str(target.relative_to(self.root)), "bytes": len(encoded)}

    def check_python(self, path: str) -> dict[str, object]:
        source = self.read_file(path)
        try:
            ast.parse(source, filename=path)
        except SyntaxError as exc:
            return {"path": path, "valid": False, "error": f"line {exc.lineno}: {exc.msg}"}
        return {"path": path, "valid": True, "error": None}

    def test(self, skill: str) -> dict[str, object]:
        return {
            "skill": skill,
            "tests": ["syntax", "permissions", "dependency_check"],
            "status": "available",
            "workspace": str(self.root),
        }

    def execute(self, operation: str, **kwargs: object) -> dict[str, object]:
        if operation == "list_files":
            return {"files": self.list_files()}
        if operation == "read_file":
            path = str(kwargs.get("path", ""))
            return {"path": path, "content": self.read_file(path)}
        if operation == "write_file":
            return self.write_file(str(kwargs.get("path", "")), str(kwargs.get("content", "")))
        if operation == "check_python":
            return self.check_python(str(kwargs.get("path", "")))
        raise SandboxError(f"unsupported sandbox operation: {operation}")
