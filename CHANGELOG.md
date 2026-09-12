# ANT AI Changelog

## 0.3.0 — NOVA-Core integration

### Runtime
- Integrated NOVA-Core as the native intelligence runtime.
- Added real local GGUF inference support through NOVA-Core.
- Added provider-neutral model API profiles.
- Native NOVA Core requires no external API key.
- External providers remain request-scoped and user-selected.

### Security
- API credentials are not persisted by the runtime.
- Native Google/Gemini credentials use request headers rather than URL query parameters.
- Removed legacy local-provider validation paths from the active test surface.

### Execution
- ANT remains the governance, planner, audit, verification, and sandbox control plane.
- NOVA-Core provides the cognitive runtime, memory, and local/cloud model execution.
- Coding and testing continue to use ANT sandbox controls until a shared remote tool-call contract is available.
