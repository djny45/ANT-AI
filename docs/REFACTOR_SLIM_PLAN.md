# ANT AI Slim Refactor Plan

## Objective
Reduce repository complexity while preserving functionality.

## Phase 1: Consolidate

Move toward:

```
ant/
 core.py
 agents.py
 memory.py
 workflow.py
 security.py
 connectors.py

apk/
 builder.py
 scanner.py
 release.py

android/
 app/
 ui/
```

## Phase 2: Cleanup

Remove only:
- duplicate implementations
- unused dependencies
- abandoned experiments
- temporary files

## Phase 3: Validate

Before removing anything:
- check imports
- check workflows
- run tests
- verify build pipeline

## Rule
No feature removal without replacement.
