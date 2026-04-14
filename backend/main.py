"""
cocoro-face - FastAPI Backend Entry Point
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import job, swap

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle."""
    logger.info("cocoro-face backend starting up")
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    yield
    logger.info("cocoro-face backend shutting down")


app = FastAPI(
    title="cocoro-face API",
    version=settings.app_version,
    description="Local face swap API powered by FaceFusion 3.6.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(swap.router, prefix="/api/swap", tags=["swap"])
app.include_router(job.router, prefix="/api/job", tags=["job"])


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.get("/health", tags=["health"])
async def health() -> dict:
    return {
        "status": "ok",
        "version": settings.app_version,
        "gpu": "RTX PRO 6000",
        "cuda": "12.8",
    }
