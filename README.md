# ANT-AI

## Autonomous Neural Team AI Platform

ANT-AI is a web-based AI assistant platform designed to provide users with a conversational AI experience through a dedicated website, similar to modern AI platforms such as ChatGPT and Claude.

Users interact with ANT-AI through the web interface. The website acts as the primary access layer while the intelligence system operates behind the scenes through ANT's agent architecture.

## Product Vision

```text
User
 |
 v
ANT-AI Website
 |
 v
Conversation Interface
 |
 v
ANT API Layer
 |
 v
ANT Web Bridge
 |
 v
ANT Runtime
 |
 v
Autonomous Agent Swarm
```

The goal is to create a complete AI platform where users can:

- Chat with ANT-AI through a browser
- Request tasks and workflows
- Interact with autonomous AI agents
- Access specialized intelligence modules
- Receive coordinated responses from multiple agents

## Core Architecture

```text
ANT-AI Website
      |
      v
Frontend (React + Vite + TypeScript)
      |
      v
ANT API Client
      |
      v
Web Bridge
      |
      v
ANT Runtime
      |
      v
Agent Swarm
      |
      +-- Commander Agent
      +-- Specialist Agents
      +-- Worker Agents
```

## Repository Structure

```text
ANT-AI/
|
├── frontend/          # User-facing AI website interface
├── web_bridge/        # Frontend and AI communication layer
├── runtime/           # Core AI execution system
├── agents/            # Autonomous agent modules
└── README.md
```

## Frontend Website

Built with:

- React
- TypeScript
- Vite

The frontend is the main user experience layer of ANT-AI.

Features:

- Chat-style AI interface foundation
- ANT architecture visualization
- Agent workflow presentation
- Web application deployment support
- Runtime connection preparation

Run locally:

```bash
cd frontend
npm install
npm run dev
```

Build:

```bash
npm run build
```

## Deployment

The ANT-AI website is designed for cloud deployment.

Recommended configuration:

- Platform: Vercel
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

## AI Runtime Flow

```text
Website User
      |
      v
ANT Conversation UI
      |
      v
ANT API
      |
      v
Web Bridge
      |
      v
ANT Runtime
      |
      v
Agent Intelligence Layer
```

The frontend and backend systems remain modular so the AI runtime can evolve independently.

## Development Status

Completed:

- [x] Frontend foundation
- [x] React component architecture
- [x] Vite setup
- [x] TypeScript configuration
- [x] Web deployment preparation

In progress:

- [ ] Production website deployment
- [ ] ANT API connection
- [ ] Real-time AI chat interface
- [ ] Agent monitoring dashboard
- [ ] Production autonomous workflows

## Vision

ANT-AI aims to become a complete browser-based AI platform where users communicate with an intelligent agent system through a simple website interface, while a coordinated swarm of specialized agents works behind the scenes.