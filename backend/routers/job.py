"""
GET    /api/job/{job_id}         - job status
GET    /api/job/{job_id}/result  - download result
DELETE /api/job/{job_id}         - delete job

Phase 2: full async video job management.
Phase 1: stub endpoints only.
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from models.schemas import JobResponse
from services.job_service import job_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str) -> JobResponse:
    """Get job status by job_id."""
    record = job_service.get(job_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "JOB_NOT_FOUND", "message": f"Job '{job_id}' not found"},
        )
    return JobResponse(
        job_id=record.job_id,
        status=record.status,
        progress=record.progress,
        created_at=record.created_at,
        updated_at=record.updated_at,
        error=record.error,
    )


@router.get("/{job_id}/result")
async def get_job_result(job_id: str) -> FileResponse:
    """Download the result file for a completed job."""
    from models.schemas import JobStatusEnum

    record = job_service.get(job_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "JOB_NOT_FOUND", "message": f"Job '{job_id}' not found"},
        )
    if record.status != JobStatusEnum.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "JOB_NOT_COMPLETED", "message": f"Job status is '{record.status}'"},
        )
    if record.output_path is None or not record.output_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "OUTPUT_MISSING", "message": "Output file not found"},
        )
    suffix = record.output_path.suffix.lstrip(".")
    media_type = "video/mp4" if suffix == "mp4" else "image/png"
    return FileResponse(
        path=str(record.output_path),
        media_type=media_type,
        filename=f"cocoro-face-{job_id}.{suffix}",
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: str) -> None:
    """Delete job record and associated temp files."""
    import shutil

    record = job_service.get(job_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "JOB_NOT_FOUND", "message": f"Job '{job_id}' not found"},
        )
    from config import settings

    job_dir = settings.temp_dir / job_id
    if job_dir.exists():
        shutil.rmtree(job_dir)
    job_service.delete(job_id)
