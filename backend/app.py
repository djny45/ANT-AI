"""FastAPI entrypoint for the ANT unified intelligence prototype."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request
from intelligence.ollama_connector import OllamaConnector

app = FastAPI(title="ANT AI API", version="0.1.0")

# Keep local development permissive while allowing production deployments to
# provide an explicit comma-separated origin list through ANT_CORS_ORIGINS.
configured_origins = os.getenv("ANT_CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
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
    return {"status": "ok", "service": "ant-ai-api", "version": "0.1.0"}


@app.get("/health/model")
async def model_health() -> dict:
    """Report whether the configured local model runtime is reachable."""
    connector = OllamaConnector()
    return {
        "provider": "ollama",
        "url": connector.url,
        "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
        "available": connector.health(),
    }


@app.post("/api/chat")
async def chat(request: Request, payload: ChatRequest) -> dict:
    """Execute one ANT request, optionally using the caller's OpenRouter key.

    The browser sends the key as a Bearer token. ANT passes it only through the
    current request context; it is not written to audit or memory state.
    """
    authorization = request.headers.get("Authorization", "")
    api_key = ""
    if authorization.lower().startswith("bearer "):
        api_key = authorization[7:].strip()

    context = dict(payload.context)
    if api_key:
        context["openrouter_api_key"] = api_key

    try:
        return await process_chat_request(
            message=payload.message,
            user_id=payload.user_id,
            conversation_id=payload.conversation_id,
            context=context,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="ANT execution failed") from exc


website_dir = Path(__file__).resolve().parent.parent / "website"
if website_dir.exists():
    app.mount("/", StaticFiles(directory=website_dir, html=True), name="website")
