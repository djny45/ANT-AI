# ANT Website Agent Experiment Status

## Objective
Connect the existing ANT runtime to a Vercel-hosted experimental website.

## Architecture

Website (Vercel)
        |
        v
Web Bridge API
        |
        v
ANT Adapter
        |
        v
Existing ANT Runtime

## Rules

- Keep ANT core unchanged.
- Use a thin integration layer.
- Prototype deployment only.
- Production security hardening comes later.

## Next Steps

1. Identify runtime entry point.
2. Connect adapter to execution flow.
3. Add minimal endpoint test.
4. Validate website-to-agent communication.
