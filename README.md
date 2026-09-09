# ANT-AI

## Autonomous Neural Team AI Framework

ANT-AI is a hierarchical AI agent framework designed for orchestrating autonomous agents through a scalable swarm architecture.

The project combines:

- Agent orchestration
- Runtime execution layers
- Web interface control
- API bridge communication
- Modular AI workflows

## Architecture

```text
User Interface
      |
      v
Frontend (React + Vite + TypeScript)
      |
      v
ANT Web Bridge
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
├── frontend/          # React + TypeScript web interface
├── web_bridge/        # Frontend/runtime communication layer
├── runtime/           # Core execution engine
├── agents/            # Autonomous agent modules
└── README.md
```

## Frontend

Built with:

- React
- TypeScript
- Vite

Frontend includes:

- ANT architecture visualization
- Agent workflow presentation
- Component-based UI structure
- Vercel deployment configuration
- Runtime integration preparation

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

Frontend deployment target:

- Vercel
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

## Runtime Integration

Connection architecture:

```text
Frontend
   |
   v
ANT API Client
   |
   v
web_bridge
   |
   v
ANT Runtime
   |
   v
Agent Swarm
```

Backend/runtime architecture remains modular and independent from the frontend layer.

## Development Status

Completed:

- [x] Frontend foundation
- [x] React component architecture
- [x] Vite configuration
- [x] TypeScript configuration
- [x] Vercel deployment setup

In progress:

- [ ] Final production build validation
- [ ] Runtime API connection
- [ ] Live agent monitoring dashboard
- [ ] Production agent orchestration

## Vision

ANT-AI aims to provide a flexible foundation for building autonomous AI systems where multiple specialized agents collaborate through a coordinated intelligence layer.