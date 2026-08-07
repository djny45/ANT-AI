try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
except ImportError:
    FastAPI = None

app = FastAPI() if FastAPI else None


@app.post('/execute') if app else (lambda x: x)
def execute(request):
    return {"goal": request, "status": "received"}


# skills status endpoint
if app:
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
