"""Vercel entrypoint for the ANT chat API.

The file itself is mounted at /api/chat by Vercel, so the FastAPI routes here
use / and /health rather than repeating the /api/chat prefix.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from ant_langgraph.integrations.fastapi_bridge import process_chat_request

app = FastAPI(title="ANT AI Vercel API", version="0.1.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20000)
    user_id: str | None = None
    conversation_id: str | None = None
    context: dict = Field(default_factory=dict)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "ant-ai-api", "provider": "openrouter"}


@app.post("/")
async def chat(request: Request, payload: ChatRequest) -> dict:
    """Execute one ANT request using the browser's selected OpenRouter model."""
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
        # Keep secrets out of the response while making runtime failures
        # diagnosable from the browser instead of returning an opaque 500.
        raise HTTPException(status_code=500, detail=f"ANT execution failed: {type(exc).__name__}") from exc


__all__ = ["app"]
