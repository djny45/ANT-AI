# ANT-AI Frontend

Modern React + TypeScript interface for the ANT-AI ecosystem.

## Stack

- React
- TypeScript
- Vite
- Component-based architecture

## Structure

```text
frontend/
├── src/
│   ├── components/   # UI components
│   ├── data/         # Project configuration data
│   ├── lib/          # Utility functions
│   ├── App.tsx
│   └── main.tsx
├── public/
├── package.json
└── vite.config.ts
```

## Development

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

Build production version:

```bash
npm run build
```

## Integration

The frontend is designed to connect with the existing ANT-AI backend through the API/web bridge layer.

```text
Frontend
   ↓
API Layer
   ↓
ANT web_bridge
   ↓
ANT Runtime
   ↓
Agents
```

The frontend remains independent from backend runtime internals, allowing the ANT-AI system to evolve modularly.
