"""Read-only ANT repository snapshot access for sandbox runs."""

from __future__ import annotations

import io
import os
import tarfile
import urllib.error
import urllib.request
from pathlib import Path


class RepositoryAccessError(ValueError):
    """Raised when a repository snapshot cannot be safely accessed."""


class RepositorySnapshot:
    """Fetch and expose a fixed public ANT repository snapshot read-only."""

    DEFAULT_REPOSITORY = "https://github.com/djny45/ANT-AI"
    DEFAULT_REF = "main"
    MAX_FILE_BYTES = 512 * 1024
    MAX_FILES = 5000

    def __init__(self, root: str, repository: str | None = None, ref: str | None = None):
        self.root = Path(root).resolve()
        self.repository = (repository or os.getenv("ANT_REPOSITORY_URL", self.DEFAULT_REPOSITORY)).rstrip("/")
        self.ref = ref or os.getenv("ANT_REPOSITORY_REF", self.DEFAULT_REF)
        if self.repository != self.DEFAULT_REPOSITORY:
            raise RepositoryAccessError("repository access is restricted to the ANT repository")

    def ensure(self) -> None:
        if (self.root / ".ant-repository-ready").exists():
            return
        self.root.mkdir(parents=True, exist_ok=True)
        url = f"{self.repository}/archive/refs/heads/{self.ref}.tar.gz"
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                archive = response.read()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RepositoryAccessError(f"repository snapshot unavailable: {exc}") from exc
        if len(archive) > 50 * 1024 * 1024:
            raise RepositoryAccessError("repository snapshot exceeds size limit")

        temp = self.root.with_name(f"{self.root.name}.tmp")
        if temp.exists():
            raise RepositoryAccessError("repository staging directory already exists")
        temp.mkdir(parents=True)
        try:
            with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
                members = [m for m in tar.getmembers() if m.isfile()]
                if len(members) > self.MAX_FILES:
                    raise RepositoryAccessError("repository contains too many files")
                for member in members:
                    if member.size > self.MAX_FILE_BYTES:
                        continue
                    parts = Path(member.name).parts
                    if len(parts) < 2 or any(part in {"", ".", ".."} for part in parts):
                        continue
                    relative = Path(*parts[1:])
                    destination = (temp / relative).resolve()
                    if temp not in destination.parents:
                        continue
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    extracted = tar.extractfile(member)
                    if extracted is not None:
                        destination.write_bytes(extracted.read(self.MAX_FILE_BYTES + 1))
            (temp / ".ant-repository-ready").write_text(self.ref, encoding="utf-8")
            temp.replace(self.root)
        except Exception:
            import shutil
            shutil.rmtree(temp, ignore_errors=True)
            raise

    def _path(self, relative: str) -> Path:
        if not relative or relative.startswith("/"):
            raise RepositoryAccessError("repository paths must be relative")
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise RepositoryAccessError("path escapes repository snapshot")
        return candidate

    def list_files(self) -> list[str]:
        self.ensure()
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*") if p.is_file() and p.name != ".ant-repository-ready")

    def read_file(self, path: str) -> str:
        self.ensure()
        target = self._path(path)
        if not target.is_file():
            raise RepositoryAccessError("repository file does not exist")
        if target.stat().st_size > self.MAX_FILE_BYTES:
            raise RepositoryAccessError("repository file exceeds sandbox read limit")
        return target.read_text(encoding="utf-8")
