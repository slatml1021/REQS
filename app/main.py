"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.requirements import router as requirements_router


app = FastAPI(title="REQS API", version="0.1.0")
app.include_router(requirements_router, prefix="/api/v1")
