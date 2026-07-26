# 🐜 ANT DEV Repository Consolidation

## Final Direction

ANT DEV stays as a GitHub engineering agent system.

It is not part of the APK release.

## Single Source of Truth

Keep:

- ANT_DEV_CORE documentation
- ANT DEV workflows
- Build/test automation
- Error reports

## Cleanup Rules

Remove or archive only when confirmed:

- Duplicate agent workflows
- Duplicate dashboards
- Old experimental files
- Unused generated reports

## Engineering Pipeline

```
GitHub Change
      ↓
ANT DEV Scan
      ↓
Error Detection
      ↓
Code Patch
      ↓
Build Test
      ↓
Report
```

## Agent Responsibilities

Code Agent:
- Kotlin fixes
- Refactoring
- Architecture checks

Build Agent:
- Gradle checks
- APK verification

Research Agent:
- Track AI engineering trends
- Review useful open-source patterns

Test Agent:
- Validate changes

Security Agent:
- Dependency and secret review

## Rule

No uncontrolled automatic deletion. Every removal must be verified to avoid breaking the application.
