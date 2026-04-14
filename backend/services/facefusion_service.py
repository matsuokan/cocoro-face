"""
FaceFusion subprocess wrapper.
This is the SOLE entry point to the FaceFusion CLI.
Do NOT call FaceFusion from any other module.
"""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from config import settings
from models.schemas import FaceSelectorOrder, FusionResult, PixelBoost

logger = logging.getLogger(__name__)

# FaceFusion CLI invocation:
#   python -m facefusion headless-run \
#     --config-path <facefusion.ini> \
#     --source-paths <source> \
#     --target-path <target> \
#     --output-path <output> \
#     [--face-swapper-pixel-boost 1024x1024] \
#     [--face-selector-order best-worst]
#
# The processors and models are defined in facefusion.ini.


class FaceFusionService:
    """Wraps the FaceFusion headless CLI as a subprocess."""

    def __init__(self) -> None:
        self._config_path = settings.facefusion_config.resolve()
        self._facefusion_dir = settings.facefusion_dir

    def _build_base_cmd(self) -> list[str]:
        return [
            "python",
            "-m",
            "facefusion",
            "headless-run",
            "--config-path",
            str(self._config_path),
        ]

    def run_image_swap(
        self,
        source_path: Path,
        target_path: Path,
        output_path: Path,
        enhance: bool = True,
        pixel_boost: PixelBoost = "1024x1024",
        face_selector_order: FaceSelectorOrder = "best-worst",
    ) -> FusionResult:
        """
        Run face swap on a single image.

        Args:
            source_path: Path to source face image.
            target_path: Path to target image.
            output_path: Desired output path (will be created by FaceFusion).
            enhance:    Whether to apply GFPGAN face enhancement.
            pixel_boost: Resolution for face swap.
            face_selector_order: How to order detected faces.

        Returns:
            FusionResult with success flag and output path.
        """
        cmd = self._build_base_cmd() + [
            "--source-paths", str(source_path),
            "--target-path", str(target_path),
            "--output-path", str(output_path),
            "--face-swapper-pixel-boost", pixel_boost,
            "--face-selector-order", face_selector_order,
        ]

        if not enhance:
            # Override processors to skip face_enhancer and expression_restorer
            cmd += ["--processors", "face_swapper"]

        logger.debug("FaceFusion cmd: %s", " ".join(cmd))

        try:
            proc = subprocess.run(
                cmd,
                cwd=str(self._facefusion_dir),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max for image
            )
        except subprocess.TimeoutExpired as exc:
            logger.error("FaceFusion timed out: %s", exc)
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr="FaceFusion process timed out after 300 seconds",
                returncode=-1,
            )
        except OSError as exc:
            logger.error("FaceFusion failed to start: %s", exc)
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr=str(exc),
                returncode=-1,
            )

        if proc.returncode != 0:
            logger.error(
                "FaceFusion exited with code %d\nstderr: %s",
                proc.returncode,
                proc.stderr,
            )
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr=proc.stderr,
                returncode=proc.returncode,
            )

        if not output_path.exists():
            logger.error("FaceFusion returned 0 but output file missing: %s", output_path)
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr="Output file not found after FaceFusion completed",
                returncode=0,
            )

        logger.info("FaceFusion completed successfully: %s", output_path)
        return FusionResult(
            success=True,
            output_path=output_path,
            stderr=proc.stderr,
            returncode=0,
        )

    def run_video_swap(
        self,
        source_path: Path,
        target_path: Path,
        output_path: Path,
        enhance: bool = True,
        pixel_boost: PixelBoost = "1024x1024",
        progress_callback: "Callable[[int], None] | None" = None,
    ) -> FusionResult:
        """
        Run face swap on a video (Phase 2).
        progress_callback(n) is called with 0-100 progress percent.
        """
        from typing import Callable  # local import to avoid forward ref issues

        cmd = self._build_base_cmd() + [
            "--source-paths", str(source_path),
            "--target-path", str(target_path),
            "--output-path", str(output_path),
            "--face-swapper-pixel-boost", pixel_boost,
        ]

        if not enhance:
            cmd += ["--processors", "face_swapper"]

        logger.debug("FaceFusion video cmd: %s", " ".join(cmd))

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(self._facefusion_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            assert proc.stdout is not None
            assert proc.stderr is not None

            stderr_lines: list[str] = []
            for line in proc.stdout:
                line = line.strip()
                if progress_callback and "%" in line:
                    # Parse progress from lines like "Processing: 42%"
                    try:
                        pct = int(line.split("%")[0].split()[-1])
                        progress_callback(min(pct, 100))
                    except (ValueError, IndexError):
                        pass

            proc.wait(timeout=3600)  # 1 hour max for video
            stderr_out = proc.stderr.read()

        except subprocess.TimeoutExpired as exc:
            proc.kill()
            logger.error("FaceFusion video timed out: %s", exc)
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr="FaceFusion video process timed out",
                returncode=-1,
            )
        except OSError as exc:
            logger.error("FaceFusion video failed to start: %s", exc)
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr=str(exc),
                returncode=-1,
            )

        if proc.returncode != 0:
            logger.error("FaceFusion video exited %d: %s", proc.returncode, stderr_out)
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr=stderr_out,
                returncode=proc.returncode,
            )

        if not output_path.exists():
            return FusionResult(
                success=False,
                output_path=output_path,
                stderr="Output video file not found after FaceFusion completed",
                returncode=0,
            )

        logger.info("FaceFusion video completed: %s", output_path)
        return FusionResult(
            success=True,
            output_path=output_path,
            stderr=stderr_out,
            returncode=0,
        )
