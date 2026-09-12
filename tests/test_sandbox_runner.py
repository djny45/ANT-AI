from pathlib import Path

import pytest

from skills.sandbox_runner import SandboxError, SkillSandbox


def test_sandbox_confines_paths(tmp_path: Path) -> None:
    sandbox = SkillSandbox(execution_id="test-run", root=str(tmp_path))
    sandbox.write_file("src/main.py", "print('ok')\n")
    assert sandbox.list_files() == ["src/main.py"]
    assert sandbox.check_python("src/main.py")["valid"] is True

    with pytest.raises(SandboxError):
        sandbox.read_file("../outside.txt")


def test_sandbox_reports_python_syntax_errors(tmp_path: Path) -> None:
    sandbox = SkillSandbox(execution_id="syntax-run", root=str(tmp_path))
    sandbox.write_file("broken.py", "def broken(:\n    pass\n")
    result = sandbox.check_python("broken.py")
    assert result["valid"] is False
    assert "line" in str(result["error"])


def test_sandbox_rejects_absolute_paths(tmp_path: Path) -> None:
    sandbox = SkillSandbox(execution_id="absolute-run", root=str(tmp_path))
    with pytest.raises(SandboxError):
        sandbox.write_file("/tmp/escape.txt", "blocked")
