# ANT Website Agent Experiment

## Goal

Connect the ANT runtime with a simple website interface for experimental testing.

## Prototype Flow

```text
User
 ↓
Vercel Website
 ↓
Agent API Bridge
 ↓
ANT Runtime
 ↓
Task Execution
 ↓
Website Response
```

## Scope

- Experimental prototype only
- No full production deployment
- No rebuild of ANT core
- Reuse existing runtime modules

## Deployment Model

Frontend:
- Vercel

Backend/runtime:
- ANT API bridge
- Cloud/VPS/local test runtime

## Validation Goals

1. Website can send a task
2. ANT receives the task
3. Agent produces a response
4. Result is displayed on the website
