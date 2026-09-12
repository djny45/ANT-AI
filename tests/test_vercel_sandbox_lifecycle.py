from __future__ import annotations

import sys
import types

from sandbox.client import RemoteSandbox


class _FakeCommand:
    exit_code = 0

    def stdout(self):
        return ""

    def stderr(self):
        return ""


class _FakeSandbox:
    created = []
    stopped = 0

    @classmethod
    def create(cls, **kwargs):
        cls.created.append(kwargs)
        return cls()

    def run_command(self, *_args, **_kwargs):
        return _FakeCommand()

    def stop(self):
        type(self).stopped += 1


def test_vercel_sandbox_is_ephemeral(monkeypatch):
    module = types.ModuleType("vercel.sandbox")
    module.Sandbox = _FakeSandbox
    vercel = types.ModuleType("vercel")
    vercel.sandbox = module
    monkeypatch.setitem(sys.modules, "vercel", vercel)
    monkeypatch.setitem(sys.modules, "vercel.sandbox", module)

    sandbox = RemoteSandbox("test-execution")
    sandbox.execute("list_files")
    sandbox.close()

    assert _FakeSandbox.created[-1]["persistent"] is False
    assert _FakeSandbox.stopped >= 1


def test_sandbox_rejects_workspace_traversal():
    sandbox = RemoteSandbox("test-execution")

    try:
        sandbox.execute("read_file", path="../outside.txt")
    except Exception as exc:
        assert "relative" in str(exc)
    else:
        raise AssertionError("path traversal should be rejected")
