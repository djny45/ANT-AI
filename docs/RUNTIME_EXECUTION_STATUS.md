# ANT AI Runtime Execution Status

## Production target

The web application is no longer treated as a UI-only prototype. The production
path is:

Browser → Vercel `/api/chat` → ANT unified graph → OpenRouter → governed tools
→ verification → response.

Coding and testing capabilities can invoke the ANT sandbox as a model tool.
The tool is allow-listed to workspace file operations and Python syntax checks.

## Implemented production path

- FastAPI Vercel entrypoint with explicit model selection.
- Unified graph execution boundary.
- Governance decision before capability execution.
- OpenRouter connector with bounded model tool-call loop.
- Per-execution sandbox workspace.
- Path traversal and file-size/file-count limits.
- Sandbox operations: `list_files`, `read_file`, `write_file`, `check_python`.
- Vercel-managed ephemeral sandbox support for Vercel deployments.
- Optional authenticated dedicated sandbox service for deployments that require a separate execution boundary.
- Runtime health reports the effective sandbox configuration state.
- Sandbox tool-call counts are included in verification metadata.
- Coding/testing sandbox lifecycle is closed after each capability execution.

## Deployment architecture

### Web/API

Deploy the repository's frontend and `api/chat.py` through Vercel.
Set the OpenRouter credentials as server/client-appropriate environment variables
(the browser-supplied API key remains request-scoped and must never be committed).

On Vercel, `sandbox/client.py` selects the Vercel Sandbox SDK automatically when
no `ANT_SANDBOX_URL` is configured. Each coding/testing capability creates an
execution-scoped sandbox with `persistent=False`, clones the public ANT repository
as read-only-by-policy input, uses a separate writable workspace, and stops the
sandbox when execution completes.

### Dedicated sandbox (optional)

When a separately deployed sandbox service is preferred, build `sandbox/Dockerfile`
and deploy it as a separate service. Configure:

- `ANT_SANDBOX_URL` — internal HTTPS URL of the sandbox service.
- `ANT_SANDBOX_TOKEN` — shared secret stored only on the server side.
- `ANT_SANDBOX_ROOT=/workspace` on the sandbox service.
- `ANT_MAX_SANDBOX_TOOL_CALLS=3` on the ANT API.

The Vercel runtime uses the dedicated service when `ANT_SANDBOX_URL` is explicitly
configured. Otherwise, Vercel deployments use the managed ephemeral sandbox path.
Outside Vercel and without a remote URL, coding/testing uses a bounded local
workspace for development; this fallback is not a substitute for production
isolation.

## Remaining production hardening

1. Attach a persistent database/memory backend instead of process-local memory.
2. Validate production Vercel environment configuration and `/api/chat/health`.
3. Run the end-to-end production acceptance suite with a real OpenRouter key.
4. Add centralized telemetry/alerting and retention policies.
5. If required by the deployment threat model, use the dedicated sandbox service
   with platform-level network isolation, CPU/memory limits, request timeouts,
   and ephemeral workspace cleanup.

## Engineering rule

Keep one intelligence identity. Temporary capabilities may use governed tools,
but they must not become independent permanent agents or bypass verification.
