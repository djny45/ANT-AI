![ANT AI Logo](logo.png)

# ANT AI Technologies
## Unified Adaptive Intelligence Operating System

**One intelligence. One core. Dynamic internal capabilities. Governed execution.**

ANT AI is a nature-inspired AI platform built around a single unified intelligence core. When a task requires different kinds of work, the core temporarily divides its own cognition into specialized internal capabilities, executes them, verifies the results, and recombines them into one response.

> ANT AI is not a collection of independent AI agents. It is one intelligence that dynamically specializes itself.

<p align="center">

![Status](https://img.shields.io/badge/status-development-orange)
![Architecture](https://img.shields.io/badge/architecture-unified%20intelligence-blue)
![Workflow](https://img.shields.io/badge/workflow-graph--based-green)
![Frontend](https://img.shields.io/badge/frontend-Next.js-black)
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

The internal capabilities above are temporary cognitive pathways of the same ANT intelligence. They are not independent permanent intelligences.

### Adaptive execution

- **Simple task:** direct fast path with minimal internal decomposition.
- **Focused task:** form only the capability required.
- **Complex task:** form multiple independent capabilities and execute them concurrently when safe.
- **Sensitive task:** apply governance before execution and verification afterward.
- **Repeated work:** use available memory context to avoid unnecessary processing.

---

## Current Prototype

The repository currently contains the following verified foundation:

- Unified graph execution boundary
- Dynamic internal capability formation
- Local Ollama model execution
- Governance and risk evaluation
- Result verification
- Process-local memory lifecycle
- Audit events and execution IDs
- FastAPI backend
- Web frontend integration
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

Parallel execution is used only when the internal work is independent. The intelligence remains unified.

---

## Governance

Important operations pass through the existing governance layer:

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

The optimization layer must never bypass governance or verification.

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

The current implementation uses lightweight process-local storage. Persistent production memory is a future deployment milestone.

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
- Next.js
- Graph-based workflow execution
- Ollama
- PostgreSQL-ready persistence architecture
- Redis-ready infrastructure
- Docker-ready deployment direction
- GitHub Actions for CI

---

## Repository Structure

```text
ANT-AI/
├── ant_core/              # Unified intelligence coordination
├── ant_langgraph/         # Graph execution boundary
├── capabilities/          # Internal capability definitions
├── memory/                # Memory systems and adapters
├── governance/            # Risk and permission controls
├── security/              # Security components
├── backend/               # FastAPI services
├── frontend/              # Website
├── database/              # Persistence layer
├── tools/                 # Tool integrations
├── tests/                 # Automated tests
├── deployment/            # Deployment configuration
└── docs/                  # Documentation
```

---

## Development

```bash
git clone https://github.com/djny45/ANT-AI.git
cd ANT-AI
```

Copy `.env.example` to your local environment configuration and provide an available Ollama model.

Run the backend and frontend using the project's current development configuration.

Run tests with:

```bash
pytest
```

The integration suite uses a model test double, so those tests do not require a running Ollama server.

---

## Roadmap

### Prototype completion

- [x] Unified intelligence graph foundation
- [x] Dynamic capability formation
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

### Future

- Semantic memory retrieval
- Advanced model routing
- Workflow checkpointing
- Recovery automation
- Performance learning from real execution data

Scale will follow measured reliability rather than architectural proliferation.

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
