# NOVA-Core Local Model Provisioning

## Purpose

NOVA-Core uses a real local GGUF inference backend. The model weights are intentionally not stored in the ANT-AI or NOVA-Core source repositories.

## Provisioning

1. Obtain a GGUF model that you are legally permitted to use.
2. Place the model on the NOVA-Core host outside Git-tracked source files.
3. Set `NOVA_MODEL_PATH` to the absolute path of that GGUF file. `LLAMA_MODEL_PATH` is accepted as a compatibility fallback.
4. Set `NOVA_CONTEXT_SIZE` to the context window appropriate for the selected model; the default is `2048`.
5. Ensure the NOVA-Core environment has a compatible `llama-cpp-python` installation.
6. Restart the NOVA-Core service and inspect `/api/health` and `/api/diagnostics`.

## Readiness states

The local backend must report `artifact_present=true` before the model can load. It must report `loaded=true` after successful initialization. Missing artifacts or missing inference dependencies are reported as unavailable; the runtime must never simulate a model response merely because configuration exists.

## ANT integration

ANT can use NOVA-Core as the native runtime through `ANT_NOVA_CORE_URL`. Native NOVA requests do not require an external model API key. Remote provider credentials remain request-scoped and must not be persisted in NOVA-Core storage or logs.

## Security

- Do not commit GGUF files, model caches, or credentials.
- Keep model files outside the Git working tree when possible.
- Use a model whose license permits the intended deployment.
- Treat downloaded model artifacts as untrusted input until their provenance and integrity are checked.
