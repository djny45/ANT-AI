# ANT AI Runtime Execution Status

## Production target

The web application is no longer treated as a UI-only prototype. The production
path is:

Browser → Vercel `/api/chat` → ANT unified graph → OpenRouter → governed tools
→ verification → response.

Coding and testing capabilities can now invoke the ANT sandbox as a model tool.
The tool is allow-listed to workspace file operations and Python syntax checks.

## Implemented production path

- FastAPI Vercel entrypoint with explicit model selection.
- Unified graph execution boundary.
- Governance decision before capability execution.
- OpenRouter connector with bounded model tool-call loop.
- Per-execution sandbox workspace.
- Path traversal and file-size/file-count limits.
- Sandbox operations: `list_files`, `read_file`, `write_file`, `check_python`.
- Optional authenticated remote sandbox service for production isolation.
- Runtime health reports whether the remote sandbox is configured.
- Sandbox tool-call counts are included in verification metadata.

## Deployment architecture

### Web/API

Deploy the repository's frontend and `api/chat.py` through Vercel.
Set the OpenRouter credentials as server/client-appropriate environment variables
(the browser-supplied API key remains request-scoped and must never be committed).

### Dedicated sandbox

For production isolation, build `sandbox/Dockerfile` and deploy it as a separate
container/service. Configure:

- `ANT_SANDBOX_URL` — internal HTTPS URL of the sandbox service.
- `ANT_SANDBOX_TOKEN` — shared secret stored only on the server side.
- `ANT_SANDBOX_ROOT=/workspace` on the sandbox service.
- `ANT_MAX_SANDBOX_TOOL_CALLS=3` on the ANT API.

The Vercel runtime automatically uses the remote sandbox when `ANT_SANDBOX_URL`
is configured. Without it, coding/testing uses a bounded `/tmp` workspace for
lightweight development behavior; this fallback is not a substitute for a
separately isolated production execution service.

## Remaining production hardening

1. Attach a persistent database/memory backend instead of process-local memory.
2. Deploy the dedicated sandbox service with platform-level network isolation,
   CPU/memory limits, request timeouts, and ephemeral workspace cleanup.
3. Configure Vercel production environment variables and verify `/api/chat/health`.
4. Run the end-to-end production acceptance suite with a real OpenRouter key.
5. Add centralized telemetry/alerting and retention policies.

## Engineering rule

Keep one intelligence identity. Temporary capabilities may use governed tools,
but they must not become independent permanent agents or bypass verification.
