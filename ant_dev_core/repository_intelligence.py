"""
ANT DEV Core - Repository Intelligence Foundation

Purpose:
Create a lightweight foundation for understanding repositories before
suggesting improvements. This module follows the ANT principle of minimal,
verified changes instead of unnecessary code generation.
"""

from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class RepositoryMap:
    root: str
    files: list[str]
    file_count: int


class RepositoryIntelligence:
    """Initial repository understanding layer for ANT DEV Core."""

    SUPPORTED_EXTENSIONS = {
        ".py", ".js", ".ts", ".tsx", ".java", ".kt",
        ".go", ".rs", ".md", ".json", ".yaml", ".yml"
    }

    def map_repository(self, root_path: str) -> dict:
        root = Path(root_path)
        files = []

        if not root.exists():
            return asdict(RepositoryMap(root_path, [], 0))

        for item in root.rglob("*"):
            if item.is_file() and item.suffix in self.SUPPORTED_EXTENSIONS:
                files.append(str(item.relative_to(root)))

        result = RepositoryMap(
            root=str(root),
            files=sorted(files),
            file_count=len(files),
        )

        return asdict(result)

    def analyze_scope(self, repository_map: dict) -> dict:
        """Return a focused analysis scope without modifying code."""
        return {
            "files_detected": repository_map.get("file_count", 0),
            "principle": "understand first, modify second",
            "changes_allowed": False,
        }
