"""Minimal production-shaped FastAPI entrypoint for the ANT prototype."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request

app = FastAPI(title="ANT AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    user_id: str | None = None
    conversation_id: str | None = None
    context: dict = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "ant-ai-api"}


@app.post("/api/chat")
async def chat(request: ChatRequest) -> dict:
    try:
        return await process_chat_request(
            message=request.message,
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            context=request.context,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="ANT execution failed") from exc


# Serve the existing prototype website when running the backend locally.
website_dir = Path(__file__).resolve().parent.parent / "website"
if website_dir.exists():
    app.mount("/", StaticFiles(directory=website_dir, html=True), name="website")
