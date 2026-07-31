try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None

app = FastAPI() if FastAPI else None


@app.post('/execute') if app else (lambda x: x)
def execute(request):
    return {"goal": request, "status": "received"}
