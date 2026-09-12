"""Production sandbox adapter backed by Vercel's open Sandbox SDK."""

from __future__ import annotations

import os
from typing import Any


# Vercel Functions expose VERCEL=1. In that environment the graph selects
# RemoteSandbox automatically, so no separately hosted sandbox URL is needed.
if os.getenv("VERCEL") == "1" and not os.getenv("ANT_SANDBOX_URL"):
    os.environ["ANT_SANDBOX_URL"] = "vercel://managed"


class RemoteSandboxError(RuntimeError):
    """Raised when the configured production sandbox cannot complete an operation."""


class RemoteSandbox:
    """Create one isolated Vercel Sandbox per ANT capability execution.

    The public ANT repository is cloned into the VM as read-only-by-policy
    input: repository operations never expose a write operation. Generated
    files live under a separate writable ``workspace`` directory.
    """

    REPOSITORY_URL = "https://github.com/djny45/ANT-AI.git"

    def __init__(self, execution_id: str, url: str | None = None, token: str | None = None, timeout: float = 10.0):
        self.execution_id = execution_id
        self.url = (url or os.getenv("ANT_SANDBOX_URL", "")).rstrip("/")
        self.token = token or os.getenv("ANT_SANDBOX_TOKEN", "")
        self.timeout = timeout
        self._sandbox: Any = None

    def _ensure_sandbox(self) -> Any:
        if self._sandbox is not None:
            return self._sandbox
        try:
            from vercel.sandbox import Sandbox

            self._sandbox = Sandbox.create(
                runtime=os.getenv("ANT_SANDBOX_RUNTIME", "python3.13"),
                timeout=int(float(os.getenv("ANT_SANDBOX_TIMEOUT_MS", "600000"))),
                name=f"ant-{self.execution_id[:48]}",
            )
            clone = self._sandbox.run_command(
                "git",
                [
                    "clone", "--depth", "1", "--branch",
                    os.getenv("ANT_REPOSITORY_REF", "main"),
                    self.REPOSITORY_URL, "repo",
                ],
            )
            if clone.exit_code != 0:
                raise RemoteSandboxError(f"ANT repository clone failed: {clone.stderr()[:1000]}")
            mkdir = self._sandbox.run_command("mkdir", ["-p", "workspace"])
            if mkdir.exit_code != 0:
                raise RemoteSandboxError(f"sandbox workspace initialization failed: {mkdir.stderr()[:1000]}")
            return self._sandbox
        except RemoteSandboxError:
            self.close()
            raise
        except Exception as exc:
            self.close()
            raise RemoteSandboxError(f"Vercel Sandbox initialization failed: {exc}") from exc

    @staticmethod
    def _output(command: Any) -> tuple[int, str, str]:
        return int(command.exit_code), command.stdout() or "", command.stderr() or ""

    @staticmethod
    def _safe_path(path: str) -> None:
        if not path or path.startswith("/") or ".." in path.split("/"):
            raise RemoteSandboxError("sandbox paths must be relative and cannot escape the workspace")

    def execute(self, operation: str, **kwargs: Any) -> dict[str, Any]:
        sandbox = self._ensure_sandbox()
        path = str(kwargs.get("path", ""))
        content = str(kwargs.get("content", ""))

        if operation == "list_files":
            command = sandbox.run_command("find", ["workspace", "-type", "f", "-print"])
            code, stdout, stderr = self._output(command)
            if code != 0:
                raise RemoteSandboxError(stderr[:1000] or "workspace listing failed")
            return {"files": [line.removeprefix("workspace/") for line in stdout.splitlines() if line]}

        if operation == "repo_list_files":
            command = sandbox.run_command("git", ["-C", "repo", "ls-files"])
            code, stdout, stderr = self._output(command)
            if code != 0:
                raise RemoteSandboxError(stderr[:1000] or "repository listing failed")
            return {"files": [line for line in stdout.splitlines() if line], "read_only": True}

        if operation == "repo_read_file":
            self._safe_path(path)
            command = sandbox.run_command(
                "python", [
                    "-c",
                    "from pathlib import Path; import sys; p=Path('repo')/sys.argv[1]; r=p.resolve(); root=Path('repo').resolve(); assert r==root or root in r.parents; print(r.read_text(encoding='utf-8'),end='')",
                    path,
                ],
            )
            code, stdout, stderr = self._output(command)
            if code != 0:
                raise RemoteSandboxError(stderr[:1000] or "repository read failed")
            return {"path": path, "content": stdout, "read_only": True}

        if operation == "read_file":
            self._safe_path(path)
            command = sandbox.run_command(
                "python", [
                    "-c",
                    "from pathlib import Path; import sys; p=Path('workspace')/sys.argv[1]; r=p.resolve(); root=Path('workspace').resolve(); assert r==root or root in r.parents; print(r.read_text(encoding='utf-8'),end='')",
                    path,
                ],
            )
            code, stdout, stderr = self._output(command)
            if code != 0:
                raise RemoteSandboxError(stderr[:1000] or "workspace read failed")
            return {"path": path, "content": stdout}

        if operation == "write_file":
            self._safe_path(path)
            command = sandbox.run_command(
                "python", [
                    "-c",
                    "from pathlib import Path; import sys; p=Path('workspace')/sys.argv[1]; r=p.resolve(); root=Path('workspace').resolve(); assert r==root or root in r.parents; r.parent.mkdir(parents=True,exist_ok=True); r.write_text(sys.argv[2],encoding='utf-8'); print(len(sys.argv[2].encode('utf-8')))",
                    path, content,
                ],
            )
            code, stdout, stderr = self._output(command)
            if code != 0:
                raise RemoteSandboxError(stderr[:1000] or "workspace write failed")
            return {"path": path, "bytes": int(stdout.strip() or 0)}

        if operation == "check_python":
            self._safe_path(path)
            command = sandbox.run_command(
                "python", [
                    "-c",
                    "import ast,sys; p='workspace/'+sys.argv[1]; ast.parse(open(p,encoding='utf-8').read(),filename=p); print('valid')",
                    path,
                ],
            )
            code, _, stderr = self._output(command)
            return {"path": path, "valid": code == 0, "error": None if code == 0 else stderr[:1000]}

        raise RemoteSandboxError(f"unsupported sandbox operation: {operation}")

    def close(self) -> None:
        if self._sandbox is None:
            return
        try:
            self._sandbox.stop()
        except Exception:
            pass
        finally:
            self._sandbox = None
