"""
POST /api/swap/image  - synchronous image face swap
POST /api/swap/video  - async video face swap (Phase 2)
"""
from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from config import settings
from models.schemas import FaceSelectorOrder, PixelBoost
from services.facefusion_service import FaceFusionService

logger = logging.getLogger(__name__)
router = APIRouter()
_service = FaceFusionService()

# Allowed MIME types
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


def _validate_image(file: UploadFile, max_bytes: int) -> None:
    if file.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_FILE_TYPE",
                "message": f"File type '{file.content_type}' is not allowed. "
                           f"Allowed: {', '.join(_ALLOWED_IMAGE_TYPES)}",
            },
        )
    if file.size and file.size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "FILE_TOO_LARGE",
                "message": f"File exceeds maximum size of {settings.max_image_size_mb}MB",
            },
        )


@router.post("/image")
async def swap_image(
    source_image: UploadFile,
    target_image: UploadFile,
    enhance: Annotated[bool, Form()] = True,
    pixel_boost: Annotated[PixelBoost, Form()] = "1024x1024",
    face_selector_order: Annotated[FaceSelectorOrder, Form()] = "best-worst",
) -> FileResponse:
    """
    Synchronous face swap: upload source face + target image → receive swapped PNG.
    """
    _validate_image(source_image, settings.max_image_bytes)
    _validate_image(target_image, settings.max_image_bytes)

    job_id = str(uuid.uuid4())
    job_dir = settings.temp_dir / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    # Save uploads
    source_ext = (source_image.filename or "source.jpg").rsplit(".", 1)[-1]
    target_ext = (target_image.filename or "target.jpg").rsplit(".", 1)[-1]
    source_path = job_dir / f"source.{source_ext}"
    target_path = job_dir / f"target.{target_ext}"
    output_path = job_dir / "output.png"

    source_path.write_bytes(await source_image.read())
    target_path.write_bytes(await target_image.read())

    logger.info("swap_image job_id=%s enhance=%s pixel_boost=%s", job_id, enhance, pixel_boost)

    result = _service.run_image_swap(
        source_path=source_path,
        target_path=target_path,
        output_path=output_path,
        enhance=enhance,
        pixel_boost=pixel_boost,
        face_selector_order=face_selector_order,
    )

    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "FACEFUSION_ERROR",
                "message": "FaceFusion processing failed",
                "detail": result.stderr[-2000:],  # last 2000 chars only
            },
        )

    return FileResponse(
        path=str(output_path),
        media_type="image/png",
        filename=f"cocoro-face-{job_id}.png",
    )
