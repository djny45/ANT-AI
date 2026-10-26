# Implementation Status

This document distinguishes committed code from planned capabilities.

## Implemented in the bootstrap

- FastAPI app with `/health`, `/api/agents`, `/api/discovery/github`, and `/api/observations`.
- SQLAlchemy models for discovered repositories and observations.
- GitHub repository search connector using the official REST API.
- Optional GitHub token from server-side environment configuration.
- Periodic GitHub discovery job with a minimum 15-minute interval.
- Docker Compose deployment with PostgreSQL on an internal network and API port bound to localhost.
- Initial unit tests for timestamp parsing and GitHub request headers.

## Not implemented yet

- Runtime endpoint registration and active health checking.
- Endpoint SSRF protection and monitoring allowlists.
- Observation creation from monitoring jobs.
- Authentication / authorization for administrative routes.
- Database migrations; the bootstrap currently creates tables on startup.
- Alert delivery, dashboard frontend, OpenTelemetry ingestion, and Hugging Face connector.
- Automated CI execution and a verified VPS deployment.

## Before public deployment

1. Add authentication to discovery and all administrative endpoints.
2. Add endpoint monitoring only with strict SSRF controls, redirect handling, DNS/IP validation, and explicit registration.
3. Add migrations, automated tests, backup/restore validation, and request rate limiting.
4. Place the API behind TLS and an authenticated reverse proxy; do not expose the database.
5. Run the tests and inspect logs in the actual VPS environment.
6. Confirm API source limits and applicable terms before increasing discovery frequency.

## Accuracy policy

A public repository is a discovered project candidate, not proof of an autonomous agent. A successful HTTP check indicates only that an endpoint responded. Runtime execution requires explicit telemetry from a participating agent or operator.
