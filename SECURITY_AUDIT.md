# ANT AI Security Audit

Scope: full repository scan for hardcoded secrets, injection flaws, unvalidated
input, insecure dependencies, permissive CORS, exposed debug endpoints and
missing authentication.

## Fixed in this pass

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 1 | Critical | `/execute` and `/skills/status` were unauthenticated, unvalidated and unthrottled. `/skills/status` also leaked internal memory/workflow state. Now behind an `X-API-Key` check (constant-time compare, key from `ANT_API_KEY`, request refused with 503 when unset), a per-client rate limit, a typed/length-bounded request model and `InputValidator`. | `ANT_X_OS/api/server.py` |
| 2 | Critical | Rate limiter deadlocked: `allow()` held a non-reentrant `threading.Lock` and then called `block_client()`, which re-acquired the same lock. Any global-limit breach froze the request thread permanently. Blocking now uses a lock-free internal helper. | `security/rate_limiter.py` |
| 3 | High | Hardcoded PostgreSQL username and password in the release validation suite. Now read from `DATABASE_URL`, with the check reporting a clear failure when unset. | `tests/validation/pre_release_checks.py` |
| 4 | High | `.env` was tracked by git despite being listed in `.gitignore`, so any local secrets would be committed on the next `git add`. Removed from the index. | `.env`, `.gitignore` |
| 5 | High | Credentials were stored as unsalted SHA-256 and compared non-constant-time (rainbow-table and timing exposure). Now PBKDF2-HMAC-SHA256 (200k iterations) with a per-identity random salt and `hmac.compare_digest`. | `security/zero_trust_engine.py` |
| 6 | Medium | Workflow command injection: `${{ inputs.tag }}` was interpolated directly into a `run:` shell script. Now passed through the `env:` block and quoted. | `.github/workflows/release-apk.yml` |
| 7 | Medium | Eight workflows had no `permissions:` block, so they inherited the repository default token scope. All now declare `contents: read`. | `.github/workflows/*` |
| 8 | Medium | Backend dependencies were completely unpinned (`fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`), allowing installation of versions with known CVEs. Minimum secure versions now specified. | `backend/requirements.txt` |
| 9 | Low | No CORS policy existed on the API. An explicit allowlist is now read from `ANT_ALLOWED_ORIGINS` (empty by default, credentials only enabled when origins are configured), with security response headers and disabled OpenAPI/docs routes. | `ANT_X_OS/api/server.py` |

## Findings not fixed here

These need product decisions or infrastructure access, so they are reported
rather than changed:

- **nginx serves plaintext HTTP only** (`devops/nginx/conf.d/default.conf`). The
  TLS server block is commented out and there is no HSTS header or HTTP→HTTPS
  redirect. The config also references `limit_req` zones (`general_limit`,
  `api_limit`) that are not defined in any committed `nginx.conf`, so nginx will
  fail to start as-is.
- **`ZeroTrustEngine._verify_action_signature` is trust-on-first-use**: the first
  time an action string is seen it is recorded and accepted, so action
  verification can never fail. It provides no tamper protection; actions should
  be signed by the caller or checked against an allowlist.
- **`InputValidator` is denylist-based**. Regex patterns for XSS/SQLi are easy to
  bypass; it is defense in depth only. Parameterized queries and
  context-specific output encoding remain required. (`core_state/sqlite_state.py`
  correctly uses bound parameters — no SQL injection was found in the codebase.)
- **`SecurityGateway._validate_permissions` ignores the connector type** and only
  checks that permission strings are well known, so `required_permissions` is
  never enforced.
- **Android app has no network security config** and defaults to a cleartext
  `http://localhost:11434` Ollama endpoint (`android_app/.../OllamaClient.kt`,
  `ModelSettings.kt`). Add an explicit `networkSecurityConfig` restricting
  cleartext to loopback.
- **`security_v2/` duplicates `security/`** with non-functional stubs
  (`ZeroTrustEngine.check` always returns `review_required`). Importing the wrong
  module silently disables verification; the duplicates should be deleted.
- **`security-scan.yml` is a placeholder** that only echoes strings, so the
  "security gate" on pull requests always passes. Wire in a real SAST/dependency
  scanner (e.g. `pip-audit`, CodeQL, Gradle dependency check).
- **`ant-dev-live-dashboard.yml`, `ant-swarm-army-x10.yml` and
  `ant-swarm-intelligence.yml` are not valid YAML** and cannot run.

## Verified clean

- No live API keys, tokens or private keys committed; connectors read from
  `os.getenv` and workflows use GitHub secrets.
- No `eval`, `exec`, `os.system`, `shell=True` or `pickle.loads` on
  attacker-controlled data.
- No string-interpolated SQL; the only SQL in the repo uses bound parameters.
- No `innerHTML`/`document.write` sinks with user data in the website assets.
