# NOVA-Core local model provisioning

ANT-AI can use NOVA-Core as its native runtime. The native NOVA path is local and does not require an external model API key, but it requires an actual GGUF model artifact and the `llama-cpp-python` runtime.

## Runtime contract

Set `NOVA_MODEL_PATH` on the NOVA-Core service to the GGUF file that should be loaded. If it is not set, NOVA-Core falls back to:

```text
models/nova-core.gguf
```

The local backend reports `standby` when the artifact is missing or `llama-cpp-python` is unavailable. It does not simulate a successful model response.

## Provisioning rule

Do **not** commit model weights to this repository. Model artifacts can be large and may carry separate licensing terms. Provision a model outside Git and point `NOVA_MODEL_PATH` at the provisioned file.

ANT-AI now ignores `*.gguf` files so a locally provisioned model is not accidentally committed.

## Validation checklist

1. Provision a GGUF model that you are licensed to use.
2. Install the NOVA-Core runtime dependencies, including `llama-cpp-python`.
3. Set `NOVA_MODEL_PATH` to the provisioned GGUF path.
4. Start NOVA-Core and check `/api/health` or diagnostics.
5. Confirm the local model status reports `artifact_present: true` and `loaded: true` after the first inference.
6. Configure ANT with `ANT_NOVA_CORE_URL` pointing to the NOVA-Core API base URL.
7. Select **NOVA Core** in ANT's API configuration and send a test message.
8. Separately test an external provider profile to verify the provider-neutral fallback path.

## Security boundary

External provider credentials remain request-scoped. Native NOVA operation should not require a cloud API key. Never put model API keys or other secrets into `VITE_*` variables or source-controlled files.

## Current engineering state

The software integration is implemented, but this repository does not bundle a `nova-core.gguf` model. Native inference therefore remains dependent on deployment-time model provisioning.
