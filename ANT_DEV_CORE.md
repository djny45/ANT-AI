# ANT DEV CORE

## Purpose

ANT DEV CORE is the engineering intelligence layer for ANT CLAW.

Design principles:

- No emotion layer
- No personal preferences
- Objective software analysis
- Build verification first
- Minimal safe changes

## Current Capability

Implemented foundation:

- GitHub Actions failure detection workflow
- Build failure analysis entry point

## Planned Modules

```
ant_dev_core/

├── analyzer/
│   ├── KotlinAnalyzer
│   ├── GradleAnalyzer
│   └── DependencyGraph
│
├── repair/
│   ├── PatchGenerator
│   ├── RefactorEngine
│   └── RollbackManager
│
├── verification/
│   ├── BuildRunner
│   └── TestRunner
│
└── release/
    └── APKManager
```

## Operating Loop

```
Build
 ↓
Detect Error
 ↓
Analyze Cause
 ↓
Generate Patch
 ↓
Verify Build
 ↓
Report Result
```

## Safety Levels

Level 1: Analyze only

Level 2: Create suggested patches

Level 3: Create pull requests

Level 4: Autonomous merge after verification
