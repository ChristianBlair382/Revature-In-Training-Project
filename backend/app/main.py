# Run this from backend: fastapi dev app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import branches, technicians, atms, service_calls, diagnostic_reports, auth

app = FastAPI(
    title="CashCow",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # frontend endpoint
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