"""HTTP service for ANT's isolated sandbox execution boundary.

Run this service in a dedicated container/runtime, not inside the main web
frontend. It is intentionally limited to the allow-listed workspace operations.
"""

from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from .runtime import SandboxError, SkillSandbox

app = FastAPI(title="ANT Sandbox", version="1.0.0")


class SandboxRequest(BaseModel):
    execution_id: str = Field(min_length=1, max_length=128)
    operation: str = Field(pattern="^(list_files|read_file|write_file|check_python)$")
    path: str | None = Field(default=None, max_length=512)
    content: str | None = Field(default=None, max_length=262144)


def _authorize(authorization: str | None) -> None:
    expected = os.getenv("ANT_SANDBOX_TOKEN", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="ANT_SANDBOX_TOKEN is not configured")
    provided = (authorization or "").removeprefix("Bearer ").strip()
    if not provided or provided != expected:
        raise HTTPException(status_code=401, detail="sandbox authorization failed")


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "service": "ant-sandbox", "version": "1.0.0"}


@app.post("/v1/execute")
def execute(payload: SandboxRequest, authorization: str | None = Header(default=None)) -> dict[str, object]:
    _authorize(authorization)
    sandbox = SkillSandbox(execution_id=payload.execution_id)
    try:
        return sandbox.execute(
            payload.operation,
            path=payload.path or "",
            content=payload.content or "",
        )
    except SandboxError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
