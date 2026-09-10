# 🐜 ANT AI

**Autonomous Neural Taskforce**  
*One intelligence. One core. Dynamic internal capabilities. Governed execution.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active%20development-blue)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Node](https://img.shields.io/badge/node-18%2B-green)]()

ANT AI is a **unified adaptive intelligence platform**.  
It is not a collection of independent permanent agents.  
It is **one intelligence core** that can temporarily form specialized internal capabilities, execute them under governance, verify results, and recombine them into a single coherent response.

> Inspired by coordinated natural systems — one organism, many temporary specialized pathways.

---

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

---

## Key Features

| Feature                        | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **Unified Intelligence Core**  | Single reasoning identity with dynamic self-decomposition                   |
| **LLM Routing**                | Local (Ollama) + hosted (OpenRouter) with configurable model selection      |
| **Knowledge Hive Memory**      | Persistent, contextual memory across sessions and tasks                     |
| **Governance & Risk Engine**   | Pre-execution risk evaluation + post-execution verification                 |
| **Secure Audit Trail**         | Blockchain-inspired immutable logging of decisions and actions              |
| **Self-Improvement Loop**      | Learning from outcomes to improve future capability formation               |
| **Web Interface**              | Modern React + Vite + TypeScript frontend                                   |
| **Modular Runtime**            | Harness → Orchestrator → Capability Registry → Tools / Memory               |
| **Extensible Connectors**      | OpenRouter, Ollama, OmniRoute, and custom tool integrations                 |

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) (recommended for local models)
- Optional: OpenRouter API key for hosted models

### 1. Clone the repository

```bash
git clone https://github.com/djny45/ANT-AI.git
cd ANT-AI

2. Environment setup
cp .env.example .env
# Edit .env with your preferences
ANT_MODEL_PROVIDER=ollama          # or "openrouter"
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OPENROUTER_API_KEY=                # only if using OpenRouter
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
ANT_CORS_ORIGINS=http://localhost:3000,http://localhost:8000

Architecture Overview
┌─────────────────────────────────────────────────────────────┐
│                    ANT-AI Website (React)                   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                     Web Bridge / API Layer                  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    Harness + Runtime                        │
│  Orchestrator · Planner · Decision Engine · State Manager   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              ANT Intelligence Core                          │
│  Dynamic Capability Formation · Governance · Verification   │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   Research Cap.        Coding Cap.          Security Cap.
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│         Memory · Tools · Knowledge Graph · Audit Log        │
└─────────────────────────────────────────────────────────────┘

ANT-AI/
├── frontend/              # React + Vite + TypeScript web UI
├── web_bridge/            # Frontend ↔ Runtime communication
├── runtime/               # Core execution engine
├── ant_core/              # Orchestrator, planner, decision engine
├── intelligence/          # Model routers, connectors (Ollama, OpenRouter…)
├── memory/ & memory_v2/   # Knowledge hive & persistent memory
├── governance_engine/     # Risk & policy controls
├── security/ & security_v2/
├── knowledge_engine/      # Knowledge graph & retrieval
├── connectors/            # External tool & service integrations
├── harness/               # Execution boundary & lifecycle
├── docs/                  # Architecture, roadmaps, principles
├── tests/
└── ...

Development Status
Verified foundation
Unified graph execution boundary
Dynamic internal capability formation
Local Ollama model execution
Optional OpenRouter runtime
Governance and risk evaluation layer
Frontend foundation (React + TypeScript + Vite)
Active focus
End-to-end runtime execution cycle
Capability registry + agent engine binding
Memory context injection & outcome storage
Production hardening and monitoring
See docs/RUNTIME_EXECUTION_STATUS.md and related documents for the latest phase status.

Security
Report vulnerabilities privately to the maintainers.
All external tools, models, and code must pass security gates before integration.
See SECURITY.md and SECURITY_IMPROVEMENTS.md

License
This project is licensed under the MIT License.
See the LICENSE file for details.

Vision
ANT AI aims to become a complete, browser-accessible adaptive intelligence platform:
Users interact through a clean web interface.
Behind the scenes, a single governed intelligence dynamically specializes itself.
Every action is audited, verifiable, and continuously improving.
One intelligence. Adaptive. Governed. Evolving

