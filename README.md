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

```
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

```
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

Frontend features:

- ANT architecture visualization
- Agent workflow presentation
- Runtime connection ready
- Vercel deployment support

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

Planned production flow:

```
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

## Development Roadmap

- [x] Frontend foundation
- [x] React component architecture
- [x] Vite build configuration
- [x] TypeScript configuration
- [ ] Runtime API connection
- [ ] Live agent monitoring dashboard
- [ ] Production agent orchestration

## Vision

ANT-AI aims to provide a flexible foundation for building autonomous AI systems where multiple specialized agents collaborate through a coordinated intelligence layer.
