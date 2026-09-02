# Run this from backend: fastapi dev app/main.py

import os
from app.config import settings
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import branches, technicians, atms, service_calls, diagnostic_reports, auth

FRONTEND_ORIGIN = settings.frontend_origin
# os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

app = FastAPI(
    title="CashCow",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN], # frontend endpoint
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(branches.router)
app.include_router(technicians.router)
app.include_router(atms.router)
app.include_router(service_calls.router)
app.include_router(diagnostic_reports.router)
app.include_router(auth.router)

@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status", "OK"}

# Endpoint to check the version number
@app.get("/version", tags=["health"])
async def version() -> dict[str, str]:
    return {"version": app.version}

# --- TEMPORARY DEBUG ROUTES — REMOVE BEFORE SHIPPING ---
# Unauthenticated DB access. Delete this whole block once the DB name is fixed.

def _admin_db_url() -> str:
    # Same creds as DATABASE_URL, but pointed at the guaranteed-to-exist
    # 'postgres' maintenance database instead of the app database name.
    full_url = os.environ["DATABASE_URL"]
    base, _, _ = full_url.rpartition("/")
    return f"{base}/postgres"

@app.get("/debug/list-dbs", tags=["debug"])
async def debug_list_dbs():
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(_admin_db_url())
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT datname FROM pg_database WHERE datistemplate = false")
        )
        names = [row[0] for row in result]
    await engine.dispose()
    return {"databases": names}

@app.post("/debug/create-db/{name}", tags=["debug"])
async def debug_create_db(name: str):
    # Basic guard against SQL injection via the identifier — Postgres
    # identifiers can't be parameterized normally, so validate manually.
    if not name.replace("_", "").replace("-", "").isalnum():
        return {"error": "invalid database name"}
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(_admin_db_url(), isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text(f'CREATE DATABASE "{name}"'))
    await engine.dispose()
    return {"created": name}
# --- END TEMPORARY DEBUG ROUTES ---