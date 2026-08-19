try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
except ImportError:
    FastAPI = None
    BaseModel = None
    Field = None

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
    async def execute(request: ExecuteRequest):
        return await run_pipeline({
            "user_input": request.message,
            "user_id": request.user_id,
            "conversation_id": request.conversation_id,
            "context": request.context,
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
