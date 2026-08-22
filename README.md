![ANT AI Logo](logo.png)

# ANT AI Technologies
## Unified Adaptive Intelligence Operating System

**One intelligence. One core. Dynamic internal capabilities. Governed execution.**

ANT AI is a nature-inspired AI platform built around a single unified intelligence core. When a task requires different kinds of work, the core can temporarily divide its cognition into specialized internal capabilities, execute them, verify the results, and recombine them into one response.

> ANT AI is not a collection of independent AI agents. It is one intelligence that dynamically specializes itself.

<p align="center">

![Status](https://img.shields.io/badge/status-development-orange)
![Architecture](https://img.shields.io/badge/architecture-unified%20intelligence-blue)
![Workflow](https://img.shields.io/badge/workflow-graph--based-green)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
![AI](https://img.shields.io/badge/model%20runtime-Ollama%20%7C%20OpenRouter-red)
![License](https://img.shields.io/badge/license-MIT-purple)

</p>

---

## How ANT AI Works

```text
                         USER
                           ↓
                 ONE ANT INTELLIGENCE
                           ↓
                    Understand Task
                           ↓
                         Plan
                           ↓
              Dynamic Self-Decomposition
                           ↓
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          Research      Coding       Security
        capability    capability    capability
             └─────────────┼─────────────┘
                           ↓
                    Unified Execution
                           ↓
                   Governance + Verify
                           ↓
                        Memory
                           ↓
                      ONE RESPONSE
```

The internal capabilities are temporary cognitive pathways of the same ANT intelligence. They are not independent permanent intelligences.

### Adaptive execution

- **Simple task:** direct fast path with minimal processing.
- **Focused task:** form only the capability required.
- **Complex task:** form multiple independent capabilities and execute them concurrently when safe.
- **Sensitive task:** apply governance before execution and verification afterward.
- **Repeated work:** use available memory context to reduce unnecessary processing.

---

## Model Runtime

ANT keeps a single model boundary inside the unified intelligence. The runtime can be configured for local or hosted inference without changing the intelligence architecture.

### Local development

```text
ANT_MODEL_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

### OpenRouter development/evaluation

```text
ANT_MODEL_PROVIDER=openrouter
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
OPENROUTER_API_KEY=your_key
```

The OpenRouter Nemotron route is an optional hosted development/evaluation runtime. The API key must remain in the local environment and must never be committed to GitHub.

---

## Current Prototype

Verified foundation currently present in the repository:

- Unified graph execution boundary
- Dynamic internal capability formation
- Local Ollama model execution
- Optional OpenRouter Nemotron model runtime
- Governance and risk evaluation
- Result verification
- Process-local memory lifecycle
- Audit events and execution IDs
- FastAPI backend
- Web frontend/API integration
- Fast-path execution for simple requests
- Parallel execution for independent internal capabilities
- Deterministic integration tests

Production persistence, full deployment automation, and real-runtime validation remain development work.

---

## Execution Pipeline

```text
Browser
  ↓
FastAPI
  ↓
ANT Intelligence Core
  ↓
Understand
  ↓
Plan
  ↓
Dynamic Capability Formation
  ↓
Governance
  ↓
Configured Model Runtime
  ↓
Verification
  ↓
Memory
  ↓
Audit
  ↓
Response
```

---

## Performance Model

ANT AI is designed to minimize unnecessary model work.

### Fast path

Simple requests avoid unnecessary internal capability formation.

### Parallel internal capabilities

Independent temporary capabilities may execute concurrently while remaining part of the same ANT intelligence execution context.

### Model runtime selection

The configured runtime is recorded in execution metadata so latency and reliability can be measured without creating additional intelligence identities.

---

## Security Principles

- Environment-based secrets
- Restricted CORS configuration
- Governance before execution
- Verification after execution
- Audit metadata for execution tracking
- No API keys committed to the repository
- Internal capabilities do not bypass the central intelligence controls

---

## Development Status

**Private prototype / development stage.**

The core architecture is being validated before public production deployment. The next major milestone is reliable end-to-end browser → API → model → verification → memory execution followed by deployment hardening.
