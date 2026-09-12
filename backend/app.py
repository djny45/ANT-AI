"""FastAPI entrypoint for the ANT unified intelligence prototype."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request

app = FastAPI(title="ANT AI API", version="0.3.0")

configured_origins = os.getenv("ANT_CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
allowed_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    user_id: str | None = None
    conversation_id: str | None = None
    context: dict = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "ant-ai-api", "version": "0.3.0", "provider": "user-selected"}


@app.get("/health/model")
async def model_health() -> dict:
    """Report the active model API contract without probing a provider."""
    return {
        "provider": "user-selected",
        "configured": False,
        "note": "Model API credentials are supplied per request from the active browser profile.",
    }


@app.post("/api/chat")
async def chat(request: Request, payload: ChatRequest) -> dict:
    authorization = request.headers.get("Authorization", "")
    api_key = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    context = dict(payload.context)
    provider = str(context.get("model_provider", "")).strip().lower()
    model = str(context.get("model", "")).strip()
    base_url = str(context.get("model_base_url", "")).strip()
    if not api_key or not provider or not model:
        raise HTTPException(status_code=400, detail="A provider, model, and API key are required in the active API profile.")
    if provider == "custom" and not base_url:
        raise HTTPException(status_code=400, detail="Custom providers require an API endpoint.")
    context.update({"model_api_key": api_key, "model_provider": provider, "model": model, "model_base_url": base_url})
    try:
        return await process_chat_request(message=payload.message, user_id=payload.user_id, conversation_id=payload.conversation_id, context=context)
    except HTTPException:
        raise
    except Exception as exc:
        detail = f"{type(exc).__name__}: {str(exc)[:500]}" or type(exc).__name__
        raise HTTPException(status_code=500, detail=f"ANT execution failed — {detail}") from exc


website_dir = Path(__file__).resolve().parent.parent / "website"
if website_dir.exists():
    app.mount("/", StaticFiles(directory=website_dir, html=True), name="website")
