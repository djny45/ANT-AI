# ANT DEV Duplicate Cleanup Protocol

## Objective

Keep ANT-AI repository clean by removing redundant code, documentation, and overlapping systems.

## Cleanup Rules

Before adding new files or features:

1. Search existing implementation.
2. Identify duplicates.
3. Keep one source of truth.
4. Merge useful information.
5. Remove obsolete copies.
6. Run build/tests after cleanup.

## Targets

Check:

- Duplicate classes
- Duplicate documentation
- Duplicate architecture plans
- Duplicate dependencies
- Unused files
- Dead code
- Repeated configuration

## Decision Rule

Keep:

- Working implementation
- Most complete design
- Best tested version

Remove:

- Old copies
- Empty placeholders
- Conflicting definitions

## ANT DEV REPORT

```
ANT DEV CLEANUP REPORT

Scanned:

Duplicates found:

Removed:

Merged:

Tests:

Status:
```
