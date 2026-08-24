from fastapi import FastAPI

from .routers import branches, technicians, atms, service_calls, diagnostic_reports

app = FastAPI(
    title="CashCow",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.1.0"
)

app.include_router(branches.router)
app.include_router(technicians.router)
app.include_router(atms.router)
app.include_router(service_calls.router)
app.include_router(diagnostic_reports.router)

@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status", "OK"}