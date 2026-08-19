"""FastAPI surface for ANT_X_OS.

Optional dependencies are imported defensively, but every failed import is
logged and recorded so the degraded state is observable instead of silent.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

DEGRADED_COMPONENTS: List[Dict[str, str]] = []


def _record_degraded(component: str, error: BaseException) -> None:
    """Log and remember an optional component that failed to load."""
    logger.warning(
        "ANT_X_OS API running degraded: %s unavailable (%s: %s)",
        component,
        type(error).__name__,
        error,
        exc_info=True,
    )
    DEGRADED_COMPONENTS.append({
        "component": component,
        "error_type": type(error).__name__,
        "error": str(error),
    })


try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
except ImportError as error:  # pragma: no cover - depends on environment
    _record_degraded("fastapi", error)
    FastAPI = None
    HTTPException = None
    JSONResponse = None

app = FastAPI() if FastAPI else None

if app:
    try:
        from ANT_X_OS.skills.registry import registry
    except Exception as error:
        _record_degraded("skills.registry", error)
        registry = None

    try:
        from ANT_X_OS.core.memory import Memory
        _memory = Memory()
    except Exception as error:
        _record_degraded("core.memory", error)
        _memory = None

    try:
        from ant_langgraph.integration_pipeline import run_pipeline
    except Exception as error:
        _record_degraded("ant_langgraph.integration_pipeline", error)
        run_pipeline = None

    @app.post('/execute')
    async def execute(request: Dict[str, Any]):
        """Execute a request through the workflow pipeline.

        Pipeline failures are propagated as HTTP 500 with the error type and
        message rather than being reported as a successful response.
        """
        if run_pipeline is None:
            return {"goal": request, "status": "received", "degraded": DEGRADED_COMPONENTS}

        try:
            result = await run_pipeline(request)
        except Exception as error:
            logger.exception("Workflow pipeline failed for request: %s", request)
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "workflow execution failed",
                    "error_type": type(error).__name__,
                    "error": str(error),
                },
            ) from error

        return result

    @app.get('/skills/status')
    def skills_status():
        errors: List[Dict[str, str]] = list(DEGRADED_COMPONENTS)

        active: List[str] = []
        if registry:
            try:
                active = registry.active_skills()
            except Exception as error:
                logger.exception("Failed to read active skills from registry")
                errors.append({
                    "component": "skills.registry.active_skills",
                    "error_type": type(error).__name__,
                    "error": str(error),
                })

        validation_results: List[Any] = []
        if _memory:
            try:
                validation_results = _memory.retrieve_workflows()
            except Exception as error:
                logger.exception("Failed to retrieve workflows from memory")
                errors.append({
                    "component": "core.memory.retrieve_workflows",
                    "error_type": type(error).__name__,
                    "error": str(error),
                })

        return JSONResponse({
            "active_skills": active,
            "agents_using_skills": {},
            "validation_results": validation_results,
            "errors": errors,
            "status": "degraded" if errors else "ok",
        })
