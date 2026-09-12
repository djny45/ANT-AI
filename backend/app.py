"""FastAPI entrypoint for the ANT unified intelligence prototype."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request

app = FastAPI(title="ANT AI API", version="0.1.1")

configured_origins = os.getenv(
    "ANT_CORS_ORIGINS",
    "http://localhost:3000,http://localhost:8000",
)
allowed_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


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
        "version": "0.1.1",
        "provider": "openrouter",
    }


@app.get("/health/model")
async def model_health() -> dict:
    """Report the hosted OpenRouter runtime configuration without probing the API."""
    return {
        "provider": "openrouter",
        "model": os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free"),
        "configured": bool(os.getenv("OPENROUTER_API_KEY")),
    }


@app.post("/api/chat")
async def chat(request: Request, payload: ChatRequest) -> dict:
    """Execute one ANT request using the user's explicitly selected OpenRouter model.

    The browser may send the OpenRouter key as a Bearer token. ANT keeps that key
    request-scoped and never copies it into audit or memory state.
    """
    authorization = request.headers.get("Authorization", "")
    api_key = ""
    if authorization.lower().startswith("bearer "):
        api_key = authorization[7:].strip()

    context = dict(payload.context)
    selected_model = str(context.get("openrouter_model", "")).strip()

    # The UI is intentionally model-explicit: do not silently select, route, or
    # substitute a model when a client calls this endpoint.
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
        # Keep deployment debugging actionable without returning request headers,
        # credentials, or a full server traceback to the browser.
        detail = f"{type(exc).__name__}: {str(exc)[:500]}" or type(exc).__name__
        raise HTTPException(status_code=500, detail=f"ANT execution failed — {detail}") from exc


website_dir = Path(__file__).resolve().parent.parent / "website"
if website_dir.exists():
    app.mount("/", StaticFiles(directory=website_dir, html=True), name="website")
