FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ANT_SANDBOX_ROOT=/workspace

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

RUN useradd --create-home --uid 10001 ant \
    && mkdir -p /workspace \
    && chown -R ant:ant /app /workspace
USER ant

EXPOSE 8080
CMD ["uvicorn", "sandbox.service:app", "--host", "0.0.0.0", "--port", "8080"]
