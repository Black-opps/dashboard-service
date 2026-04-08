from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import summary, health, cashflow
app = FastAPI(
    title="Dashboard Service",
    description="Analytics orchestration layer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary.router)
app.include_router(cashflow.router)
app.include_router(health.router)


@app.get("/")
async def root():
    return {"service": "dashboard-service", "status": "running"}
