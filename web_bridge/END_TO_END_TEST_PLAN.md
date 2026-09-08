# ANT Website Agent Experiment - End To End Test Plan

## Goal
Validate the experimental connection between a Vercel website and the existing ANT runtime.

## Flow

User
↓
Vercel Frontend
↓
Web Bridge API
↓
ANT Adapter
↓
ANT Runtime
↓
Response

## Validation Steps

1. Send a test task from the website.
2. Confirm API receives the request.
3. Confirm adapter routes the request to ANT.
4. Confirm ANT returns a response.
5. Display the result in the website UI.

## Scope

- Experimental deployment only.
- Existing ANT core remains unchanged.
- No replacement of existing autonomy modules.
