"""Vercel entrypoint for the ANT chat API.

The file itself is mounted at /api/chat by Vercel, so the FastAPI routes here
use / and /health rather than repeating the /api/chat prefix.
"""

import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request

app = FastAPI(title="ANT AI Vercel API", version="0.3.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    user_id: str | None = None
    conversation_id: str | None = None
    context: dict = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "ant-ai-api",
        "version": "0.3.0",
        "provider": "user-selected",
        "sandbox": "remote" if os.getenv("ANT_SANDBOX_URL", "").strip() else "local-bounded",
        "sandbox_configured": bool(os.getenv("ANT_SANDBOX_URL", "").strip()),
    }


@app.post("/")
async def chat(request: Request, payload: ChatRequest) -> dict:
    authorization = request.headers.get("Authorization", "")
    api_key = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    context = dict(payload.context)
    provider = str(context.get("model_provider", "")).strip().lower()
    model = str(context.get("model", "")).strip()
    base_url = str(context.get("model_base_url", "")).strip()

    if not api_key:
        raise HTTPException(status_code=400, detail="No model API key supplied. Add a provider API profile in ANT settings.")
    if not provider:
        raise HTTPException(status_code=400, detail="No model provider selected. Choose a provider in ANT settings.")
    if not model:
        raise HTTPException(status_code=400, detail="No model selected. Enter the exact model ID for the selected provider.")
    if provider == "custom" and not base_url:
        raise HTTPException(status_code=400, detail="Custom providers require an API endpoint.")

    context["model_api_key"] = api_key
    context["model_provider"] = provider
    context["model"] = model
    context["model_base_url"] = base_url

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
        raise HTTPException(status_code=500, detail=f"ANT execution failed — {detail}") from exc


__all__ = ["app"]
