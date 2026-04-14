"""
Pydantic models for request/response schemas.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

PixelBoost = Literal["512x512", "1024x1024"]

FaceSelectorOrder = Literal[
    "left-right",
    "right-left",
    "top-bottom",
    "bottom-top",
    "large-small",
    "small-large",
    "best-worst",
    "worst-best",
]


class JobStatusEnum(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------

class SwapImageOptions(BaseModel):
    enhance: bool = True
    pixel_boost: PixelBoost = "1024x1024"
    face_selector_order: FaceSelectorOrder = "best-worst"


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class JobResponse(BaseModel):
    job_id: str
    status: JobStatusEnum
    progress: int = Field(default=0, ge=0, le=100)
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: Optional[str] = None


# ---------------------------------------------------------------------------
# Internal dataclass (not exposed to API directly)
# ---------------------------------------------------------------------------

@dataclass
class FusionResult:
    success: bool
    output_path: Path
    stderr: str
    returncode: int


@dataclass
class JobRecord:
    job_id: str
    status: JobStatusEnum = JobStatusEnum.QUEUED
    progress: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    output_path: Optional[Path] = None
