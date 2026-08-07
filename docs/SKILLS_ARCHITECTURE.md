# SKILLS ARCHITECTURE

Master Agent
    |
Skill Selector
    |
Graph Engine
    |
Agent Nodes
    |
Memory

This document describes the ANT-X engineering skills layer added to the codebase.

Overview:
- A lightweight skills framework was added under ANT_X_OS/skills.
- Skills are objects with name, description, rules and a validate() method and an execute() stub.
- A registry holds available skills and supports simple search and listing.
- A selector heuristically maps tasks to required skills.
- The master runtime was extended to select skills for tasks before delegating to agents.
- A simple GraphEngine adapter was added so nodes receive task, state, and skills.
- Memory now supports storing workflows, including which skills were selected and verification results.
- A dashboard endpoint GET /skills/status exposes active skills (when FastAPI is installed).

Design notes:
- The framework is intentionally lightweight and non-invasive. It does not alter existing agent interfaces — skills are attached to task dicts as a `skills` key.
- The skills loader registers a set of builtin engineering heuristics and core skills (coding, review, debugging, security, deployment).
- Future work: richer skill discovery, permission checks, skill execution orchestration, and persistent vector memory integration.
