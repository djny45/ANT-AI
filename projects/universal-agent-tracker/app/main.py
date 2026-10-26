from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, Query
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("uaat")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./uaat-dev.db"
    github_token: str = ""
    discovery_interval_minutes: int = 30
    github_search_query: str = "topic:ai-agent"


settings = Settings()
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_type: Mapped[str] = mapped_column(String(40), default="github")
    source_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, default="")
    stars: Mapped[int] = mapped_column(Integer, default=0)
    language: Mapped[str | None] = mapped_column(String(100), nullable=True)
    license_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    runtime_status: Mapped[str] = mapped_column(String(32), default="UNKNOWN")
    classification: Mapped[str] = mapped_column(String(32), default="candidate")


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[int] = mapped_column(Integer, index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    observation_type: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(32))
    detail: Mapped[str] = mapped_column(Text, default="")


Base.metadata.create_all(bind=engine)
scheduler = AsyncIOScheduler()


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Universal-Agent-Tracker/0.1",
    }
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    return headers


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


async def discover_github() -> dict[str, Any]:
    """Discover public repository candidates; this does not claim they are running agents."""
    params = {"q": settings.github_search_query, "sort": "updated", "order": "desc", "per_page": 50}
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=False) as client:
        response = await client.get(
            "https://api.github.com/search/repositories",
            params=params,
            headers=github_headers(),
        )
    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        raise HTTPException(status_code=429, detail="GitHub API rate limit reached; retry after reset.")
    if response.status_code >= 400:
        logger.warning("GitHub discovery failed with status %s", response.status_code)
        raise HTTPException(status_code=502, detail=f"GitHub discovery failed (HTTP {response.status_code}).")

    payload = response.json()
    items = payload.get("items", [])
    now = datetime.now(timezone.utc)
    inserted = 0
    updated = 0

    with SessionLocal() as session:
        for item in items:
            source_id = str(item.get("id", ""))
            name = str(item.get("full_name") or item.get("name") or "unknown")[:255]
            source_url = str(item.get("html_url") or "")
            if not source_id or not source_url.startswith("https://github.com/"):
                continue
            record = session.scalar(select(Agent).where(Agent.source_id == source_id))
            license_info = item.get("license") or {}
            values = {
                "source_type": "github",
                "source_id": source_id,
                "name": name,
                "source_url": source_url,
                "description": str(item.get("description") or "")[:10000],
                "stars": int(item.get("stargazers_count") or 0),
                "language": item.get("language"),
                "license_name": license_info.get("spdx_id") if isinstance(license_info, dict) else None,
                "source_updated_at": parse_datetime(item.get("updated_at")),
                "last_seen_at": now,
            }
            if record is None:
                session.add(Agent(**values))
                inserted += 1
            else:
                for key, value in values.items():
                    setattr(record, key, value)
                updated += 1
        session.commit()

    logger.info("GitHub discovery completed: inserted=%s updated=%s received=%s", inserted, updated, len(items))
    return {"source": "github", "received": len(items), "inserted": inserted, "updated": updated, "checked_at": now.isoformat()}


async def scheduled_discovery() -> None:
    try:
        await discover_github()
    except Exception:
        logger.exception("Scheduled GitHub discovery failed")


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.discovery_interval_minutes > 0:
        scheduler.add_job(
            scheduled_discovery,
            "interval",
            minutes=max(15, settings.discovery_interval_minutes),
            id="github-discovery",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
        )
        scheduler.start()
    yield
    if scheduler.running:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="Universal AI Agent Tracker",
    version="0.1.0",
    description="Public AI agent project discovery and observability metadata. Discovery is not proof of runtime execution.",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return {"status": "ok", "database": "ok"}
    except Exception as exc:
        logger.error("Health check database failure: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Database unavailable") from exc


@app.get("/api/agents")
def list_agents(
    search: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> dict[str, Any]:
    with SessionLocal() as session:
        query = select(Agent)
        if search:
            query = query.where(Agent.name.ilike(f"%{search}%"))
        query = query.order_by(Agent.stars.desc(), Agent.name.asc()).limit(limit).offset(offset)
        rows = session.scalars(query).all()
        return {
            "items": [
                {
                    "id": row.id,
                    "name": row.name,
                    "source_type": row.source_type,
                    "source_url": row.source_url,
                    "description": row.description,
                    "stars": row.stars,
                    "language": row.language,
                    "license": row.license_name,
                    "source_updated_at": row.source_updated_at.isoformat() if row.source_updated_at else None,
                    "last_seen_at": row.last_seen_at.isoformat() if row.last_seen_at else None,
                    "runtime_status": row.runtime_status,
                    "classification": row.classification,
                }
                for row in rows
            ],
            "limit": limit,
            "offset": offset,
        }


@app.post("/api/discovery/github")
async def run_github_discovery() -> dict[str, Any]:
    # Keep this route private or protect it with authentication before public exposure.
    return await discover_github()


@app.get("/api/observations")
def list_observations(
    agent_id: int = Query(ge=1),
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, Any]:
    with SessionLocal() as session:
        rows = session.scalars(
            select(Observation)
            .where(Observation.agent_id == agent_id)
            .order_by(Observation.observed_at.desc())
            .limit(limit)
        ).all()
        return {
            "items": [
                {
                    "id": row.id,
                    "agent_id": row.agent_id,
                    "observed_at": row.observed_at.isoformat(),
                    "type": row.observation_type,
                    "status": row.status,
                    "detail": row.detail,
                }
                for row in rows
            ]
        }
