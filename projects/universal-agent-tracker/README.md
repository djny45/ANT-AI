# Universal AI Agent Tracker (UAAT)

A VPS-hosted, open-source-first directory for discovering **publicly documented AI agent projects** and monitoring explicitly configured, publicly reachable service endpoints.

> **Observability boundary:** repository discovery is not proof that an agent is running. An HTTP response is not proof that an AI agent is executing. UAAT keeps source activity, endpoint availability, and opt-in execution telemetry separate.

## MVP scope

- FastAPI service with health and agent-list endpoints.
- GitHub public repository discovery using the official REST API.
- PostgreSQL persistence.
- Configurable scheduled discovery.
- Explicitly registered endpoint checks with bounded timeouts and SSRF safeguards.
- Docker Compose deployment for a single VPS.
- No LLM API required.

Hugging Face and other registries, alert delivery, authentication, richer dashboard UI, and OpenTelemetry ingestion are follow-up milestones—not claimed as implemented in this bootstrap.

## Architecture

```
GitHub REST API ──> discovery worker ──> PostgreSQL
                                          │
Configured public endpoints ──> checker ──┤
                                          v
                                    FastAPI JSON API
                                          │
                                  reverse proxy / UI
```

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Set a strong `POSTGRES_PASSWORD` and optionally `GITHUB_TOKEN`.
3. Run:

```bash
docker compose up --build -d
docker compose logs -f api
```

The API is exposed on `127.0.0.1:8000` by default. Put it behind an authenticated reverse proxy with TLS before exposing it publicly. Do not publish PostgreSQL or Redis ports to the internet.

- Health: `GET /health`
- List agents: `GET /api/agents`
- Trigger discovery: `POST /api/discovery/github` (protect this endpoint before public deployment)
- OpenAPI docs: `/docs` (disable or protect in production)

## Configuration

See `.env.example`. A GitHub token is optional but recommended for higher API limits. Use a least-privilege token and never commit real credentials.

## Safety and data handling

- Only index public source metadata.
- Endpoint checks must be explicitly configured and must not target loopback, private, link-local, multicast, or reserved IP ranges.
- Do not execute discovered repositories, agent code, or downloaded artifacts.
- Treat repository descriptions and API responses as untrusted data.
- Respect API rate limits, source terms, and robots/access policies.
- Store source URLs and observation timestamps for provenance.
- Keep credentials out of logs and database records.

## Status semantics

- `UNKNOWN`: no trustworthy runtime observation.
- `RESPONSIVE`: configured endpoint responded to a safe HTTP check.
- `UNAVAILABLE`: repeated checks failed.
- `TELEMETRY_ACTIVE`: reserved for future opt-in instrumentation; not inferred from public metadata.

## Development

```bash
python -m venv .venv
# activate the environment, then:
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The local development configuration must provide a PostgreSQL URL. Run tests before deployment and add migration management before making schema changes in production.

## Roadmap

1. Harden MVP: tests, migrations, auth, audit logging, backup/restore.
2. Add Hugging Face Hub and documented public registry connectors.
3. Add worker queue, backoff, and source-specific checkpoints.
4. Add opt-in OpenTelemetry ingestion for participating agent operators.
5. Add dashboard, filtering, historical charts, and alert channels.
6. Add retention policies and operational metrics.

## Limitations

No system can enumerate every AI agent globally. Private deployments, closed platforms, unindexed projects, and uninstrumented runtimes are not observable. Discovery coverage depends on source APIs, query strategy, rate limits, and source terms.
