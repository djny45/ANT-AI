"""Vercel entrypoint for the ANT chat API.

The file itself is mounted at /api/chat by Vercel, so the FastAPI routes here
use / and /health rather than repeating the /api/chat prefix.
"""

import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request

app = FastAPI(title="ANT AI Vercel API", version="0.2.1")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    user_id: str | None = None
    conversation_id: str | None = None
    context: dict = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict:
    """Return deployment state without exposing credentials."""
    return {
        "status": "ok",
        "service": "ant-ai-api",
        "version": "0.2.1",
        "provider": "openrouter",
        "sandbox": "remote" if os.getenv("ANT_SANDBOX_URL", "").strip() else "local-bounded",
        "sandbox_configured": bool(os.getenv("ANT_SANDBOX_URL", "").strip()),
    }


@app.post("/")
async def chat(request: Request, payload: ChatRequest) -> dict:
    """Execute one ANT request using the browser's explicitly selected model."""
    authorization = request.headers.get("Authorization", "")
    api_key = ""
    if authorization.lower().startswith("bearer "):
        api_key = authorization[7:].strip()

    context = dict(payload.context)
    selected_model = str(context.get("openrouter_model", "")).strip()
    if not selected_model:
        raise HTTPException(
            status_code=400,
            detail="No OpenRouter model selected. Choose a Free or Paid model in ANT settings.",
        )

    if api_key:
        context["openrouter_api_key"] = api_key

    try:
        return await process_chat_request(
            message=payload.message,
            user_id=payload.user_id,
            conversation_id=payload.conversation_id,
            context=context,
        )
    except HTTPException:
        raise
    except Exception as exc:
        detail = f"{type(exc).__name__}: {str(exc)[:500]}" or type(exc).__name__
        raise HTTPException(
            status_code=500,
            detail=f"ANT execution failed — {detail}",
        ) from exc


__all__ = ["app"]
