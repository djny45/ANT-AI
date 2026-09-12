# 🐜 ANT AI

**Autonomous Neural Taskforce**  
*One intelligence. One core. Dynamic internal capabilities. Governed execution.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20runtime%20integration-blue)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Node](https://img.shields.io/badge/node-18%2B-green)]()

ANT AI is a **unified adaptive intelligence platform**. It is **one intelligence core** that can temporarily form specialized internal capabilities, execute them under governance, verify results, and recombine them into a single coherent response.

## Production web runtime

The production web path is:

`Browser → Vercel /api/chat → ANT Intelligence Graph → user-selected Model API → governed tools → verification → response`

The web runtime accepts an explicitly selected provider, model, endpoint, and API key from the active API profile. There is no mandatory model aggregator and ANT does not silently switch providers. Coding and testing capabilities can use a bounded ANT sandbox through the model tool-call interface. On Vercel, ANT uses an execution-scoped, explicitly ephemeral sandbox by default. A separately hosted authenticated sandbox remains supported when `ANT_SANDBOX_URL` is configured.

## Core Principle

User Request
↓
ANT Intelligence Core
↓
Problem Understanding + Planning
↓
Dynamic Capability Formation
↓
Temporary Internal Capabilities
(Research · Coding · Security · Analysis · Testing …)
↓
Governed Parallel / Sequential Execution
↓
Verification + Risk Evaluation
↓
Memory Update
↓
Unified Final Response

### Hard Architecture Invariants

1. **One intelligence identity** — all capabilities belong to the same ANT execution context.
2. **Temporary specialization** — capabilities are formed for the current task and dissolve afterward.
3. **Shared context** — memory, governance, and state are common.
4. **Central governance** — no capability bypasses permission, risk, or verification controls.
5. **Unified result** — outputs are recombined into one verified response.
6. **No permanent agent registry** — the system does not rely on independent long-lived agents voting or competing.

## Key Features

| Feature | Description |
|---|---|
| **Unified Intelligence Core** | Single reasoning identity with dynamic self-decomposition |
| **Model API Profiles** | Store multiple provider/model/API-key profiles and explicitly select one |
| **Provider-Neutral Routing** | Direct model API transport with custom endpoint support; no mandatory aggregator |
| **Knowledge Hive Memory** | Memory adapter boundary ready for persistent backend integration |
| **Governance & Risk Engine** | Pre-execution risk evaluation + post-execution verification |
| **Secure Audit Trail** | Audit events for execution lifecycle |
| **Sandbox Tooling** | Governed per-run workspace for coding/testing with ephemeral Vercel Sandbox support |
| **Web Interface** | Modern React + Vite + TypeScript frontend |
| **Modular Runtime** | Harness → Orchestrator → Capability Registry → Tools / Memory |

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- A model provider API key for the model you want to use

### 1. Clone the repository

```bash
git clone https://github.com/djny45/ANT-AI.git
cd ANT-AI
```

### 2. Environment setup

```bash
cp .env.example .env
# Configure ANT infrastructure settings in .env
```

Model credentials are configured in the web application's **API Configuration** section. Profiles support common provider endpoints and a custom OpenAI-compatible endpoint. Never place a browser model secret in source code.

### 3. Web deployment

The repository is configured for Vercel. The frontend uses the same-origin `/api` route by default. The active browser API profile supplies the provider, model, endpoint, and key for each request. Never place a server-only secret in a `VITE_*` variable.

On Vercel, coding/testing executions use the Vercel Sandbox SDK automatically and create an ephemeral sandbox for each capability execution. Set `ANT_SANDBOX_URL` only when intentionally routing execution to a separately deployed sandbox service.

### 4. Dedicated sandbox deployment (optional)

Build `sandbox/Dockerfile` as a separate service when a dedicated execution boundary is preferred. Set `ANT_SANDBOX_TOKEN` on the sandbox service and set both `ANT_SANDBOX_URL` and `ANT_SANDBOX_TOKEN` on the ANT API. The API will then route coding/testing sandbox tool calls to that authenticated service instead of the Vercel-managed sandbox.

See `docs/RUNTIME_EXECUTION_STATUS.md` for the production deployment checklist.

## Repository layout

```text
ANT-AI/
├── frontend/              # React + Vite + TypeScript web UI
├── api/                   # Vercel FastAPI entrypoints
├── ant_langgraph/         # Unified execution graph and API bridge
├── intelligence/          # Provider-neutral model API connector
├── sandbox/               # Governed sandbox runtime + Vercel/dedicated adapters
├── skills/                # Capability compatibility adapters
├── runtime/               # Core runtime infrastructure
├── ant_core/              # Orchestrator, planner, decision engine
├── memory/ & memory_v2/   # Knowledge hive & persistent memory
├── governance_engine/     # Risk & policy controls
├── security/ & security_v2/
├── knowledge_engine/      # Knowledge graph & retrieval
├── connectors/            # External tool & service integrations
├── harness/               # Execution boundary & lifecycle
├── docs/                  # Architecture and deployment status
└── tests/
```

## Current status

### Production runtime integration

- Vercel web/API path implemented.
- Explicit user-selected model API profile.
- Provider-neutral model API connector with common native adapters and custom endpoint support.
- Unified graph execution boundary.
- Governance before capability execution.
- Tool-call loop with a bounded tool-call budget for compatible APIs.
- Coding/testing capabilities bound to the ANT sandbox tool.
- Per-execution workspace with path and resource limits.
- Vercel-managed ephemeral sandbox support.
- Optional authenticated dedicated sandbox service.
- Health endpoint reports sandbox configuration state.

### Remaining production hardening

- Persistent database-backed memory.
- Platform-level sandbox network/process isolation and resource limits.
- Production environment configuration and end-to-end acceptance testing.
- Centralized telemetry and alerting.

## Security

Report vulnerabilities privately to the maintainers.
All external tools, models, and code must pass security gates before integration.
See `SECURITY.md` and `SECURITY_IMPROVEMENTS.md`.

## License

This project is licensed under the MIT License. See `LICENSE`.

## Vision

ANT AI aims to become a complete, browser-accessible adaptive intelligence platform:
users interact through a clean web interface; behind the scenes, a single governed
intelligence dynamically specializes itself; every action is audited, verifiable,
and continuously improving.

**One intelligence. Adaptive. Governed. Evolving.**
