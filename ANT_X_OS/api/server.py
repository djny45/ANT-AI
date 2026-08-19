try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
except ImportError:
    FastAPI = None
    BaseModel = None
    Field = None

from security.input_validator import InputValidator

app = FastAPI() if FastAPI else None


if BaseModel:
    class ExecuteRequest(BaseModel):
        message: str
        user_id: str | None = None
        conversation_id: str | None = None
        context: dict = Field(default_factory=dict)
else:
    class ExecuteRequest:
        pass


if app:
    from ant_langgraph.integration_pipeline import run_pipeline

    @app.post("/execute")
    async def execute(request: dict):
        validator = InputValidator()
        message = request.get("message")
        if (
            not isinstance(message, str)
            or not message.strip()
            or not validator.validate_input(request)
        ):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Input validation failed",
                    "stage": "validation",
                    "recovery_action": "reject_invalid_input",
                },
            )
        return await run_pipeline({
            "user_input": message,
            "user_id": request.get("user_id"),
            "conversation_id": request.get("conversation_id"),
            "request_id": request.get("request_id"),
            "context": request.get("context") or {},
        })

    try:
        from ANT_X_OS.skills.registry import registry
    except Exception:
        registry = None

    try:
        from ANT_X_OS.core.memory import Memory
        _memory = Memory()
    except Exception:
        _memory = None


    @app.get('/skills/status')
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
