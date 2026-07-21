# ANT AI Slim Mode

Goal: maximum capability with minimum footprint.

## Keep

- Core runtime
- Agent orchestration
- Memory engine
- Workflow engine
- Security gate
- APK factory
- Release automation

## Remove

- Duplicate modules
- Unused examples
- Temporary files
- Repeated documentation
- Unnecessary dependencies

## Design Rules

- One module per responsibility
- Lazy load heavy systems
- Shared configuration
- Minimal dependencies
- Production-first structure

## Target Layout

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
