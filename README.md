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
![AI](https://img.shields.io/badge/local%20AI-Ollama-red)
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

## Current Prototype

Verified foundation currently present in the repository:

- Unified graph execution boundary
- Dynamic internal capability formation
- Local Ollama model execution
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
Ollama / Model Runtime
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

```text
Simple Request
      ↓
ANT Intelligence
      ↓
Direct Reasoning
      ↓
Verify
      ↓
Response
```

### Parallel internal work

```text
             ANT Intelligence
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    Capability   Capability   Capability
        └───────────┼───────────┘
                    ↓
                 Verify
```

Parallel execution is used only when internal work is independent. The intelligence remains unified.

---

## Governance

Important operations pass through the governance layer:

```text
Request
  ↓
Risk Evaluation
  ↓
Permission / Governance
  ↓
Execution
  ↓
Verification
  ↓
Audit
```

Optimization must never bypass governance or verification.

---

## Memory

The prototype supports a memory lifecycle around execution:

```text
Request
  ↓
Relevant Context
  ↓
ANT Intelligence
  ↓
Verified Result
  ↓
Experience Storage
```

The current execution memory is lightweight and process-local. Persistent production memory is a future deployment milestone.

---

## Local AI

ANT AI supports free/open-source local inference through **Ollama**.

Example environment configuration:

```text
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=30
ANT_CORS_ORIGINS=http://localhost:3000
```

No paid model API is required for the basic prototype.

---

## Technology Stack

- Python
- FastAPI
- Graph-based workflow execution
- Ollama
- Static web frontend under `website/`
- Security and governance components
- GitHub Actions
- Docker/deployment configuration already present in the repository

---

## Repository Structure

The active prototype is centered on these areas:

```text
ANT-AI/
├── ant_core/              # Core planning, decision and state components
├── ant_langgraph/         # Graph execution and integration boundary
├── backend/               # FastAPI application
├── governance_engine/     # Governance and risk controls
├── intelligence/          # Model and intelligence utilities
├── memory/                # Memory implementations
├── security/              # Security controls
├── tests/                 # Automated tests
├── tools/                 # Tool infrastructure
├── website/               # Current web interface
├── docs/                  # Architecture and release documentation
└── .github/               # CI/security workflows
```

The repository also contains legacy and experimental components that are being reduced carefully as dependencies are verified.

---

## Development

```bash
git clone https://github.com/djny45/ANT-AI.git
cd ANT-AI
```

Copy `.env.example` to your local environment and configure an available Ollama model.

The FastAPI application is under `backend/` and the current web interface is under `website/`.

Run tests with:

```bash
pytest
```

The integration suite uses a model test double for deterministic testing and therefore does not require a running Ollama server for those tests.

---

## Roadmap

### Prototype completion

- [x] Unified intelligence graph foundation
- [x] Dynamic internal capability formation
- [x] Local model execution
- [x] Governance integration
- [x] Verification
- [x] Website/API connection
- [x] Fast-path execution
- [x] Parallel internal capability execution
- [x] Deterministic integration tests
- [ ] Persistent production memory
- [ ] Full runtime CI verification
- [ ] Production deployment
- [ ] VPS end-to-end validation

### Future optimization

- Semantic memory retrieval
- Adaptive model selection
- Workflow checkpointing
- Recovery automation
- Performance learning from real execution data

Development will prioritize measured reliability and performance rather than architectural proliferation.

---

## Security

Never commit API keys, credentials, tokens, or production secrets.

Production hardening should include authentication, authorization, least-privilege tool access, rate limiting, dependency scanning, persistent audit storage, and rollback procedures.

---

## License

MIT License.

---

## ANT AI Technologies

**One intelligence. Dynamic specialization. Governed execution. Continuous improvement.**

Repository: https://github.com/djny45/ANT-AI
