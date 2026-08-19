"""ANT X OS HTTP API.

Every endpoint requires an API key, validates its input and is rate limited.
Configuration is read from the environment:

    ANT_API_KEY          shared secret clients must send in ``X-API-Key``
    ANT_ALLOWED_ORIGINS  comma separated CORS origins (default: none)
    ANT_RATE_LIMIT       max requests per client per minute (default: 20)
"""

import hmac
import os

try:
    from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
except ImportError:
    FastAPI = None

from security.input_validator import InputValidator
from security.rate_limiter import RateLimiter

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None) if FastAPI else None


if app:
    _validator = InputValidator()
    _rate_limiter = RateLimiter(max_requests=int(os.getenv("ANT_RATE_LIMIT", "20")))

    _allowed_origins = [
        origin.strip()
        for origin in os.getenv("ANT_ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins,
        allow_credentials=bool(_allowed_origins),
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-API-Key"],
    )

    SECURITY_HEADERS = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": "default-src 'none'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers.setdefault(header, value)
        return response

    def require_api_key(
        request: Request,
        x_api_key: str | None = Header(default=None),
    ) -> None:
        """Reject unauthenticated and rate limited callers."""
        expected = os.getenv("ANT_API_KEY", "")
        if not expected:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="API key is not configured",
            )
        if not x_api_key or not hmac.compare_digest(x_api_key, expected):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid API key",
            )

        client = request.client.host if request.client else "unknown"
        if not _rate_limiter.allow(client):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="rate limit exceeded",
            )

    class ExecuteRequest(BaseModel):
        message: str = Field(min_length=1, max_length=10000)

    @app.post("/execute", dependencies=[Depends(require_api_key)])
    def execute(request: ExecuteRequest):
        if not _validator.validate_string(request.message):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="input rejected by validation",
            )
        return {"goal": request.message, "status": "received"}

    try:
        from ANT_X_OS.skills.registry import registry
    except Exception:
        registry = None

    try:
        from ANT_X_OS.core.memory import Memory
        _memory = Memory()
    except Exception:
        _memory = None

    @app.get("/skills/status", dependencies=[Depends(require_api_key)])
    def skills_status():
        if registry:
            active = registry.active_skills()
        else:
            active = []

        validation_results = []
        if _memory:
            try:
                validation_results = _memory.retrieve_workflows()
            except Exception:
                validation_results = []

        return JSONResponse({
            "active_skills": active,
            "agents_using_skills": {},
            "validation_results": validation_results
        })
