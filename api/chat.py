"""Vercel entrypoint for the ANT chat API.

This adapter exposes the existing FastAPI application at /api/chat so the
Vite frontend can use a same-origin API when deployed to Vercel.
"""

from backend.app import app

__all__ = ["app"]
