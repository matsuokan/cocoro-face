"""
Centralised configuration via pydantic-settings.
All environment variables are read here and nowhere else.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Paths
    temp_dir: Path = Path("/tmp/cocoro-face")
    facefusion_dir: Path = Path("/home/mdl/facefusion")
    facefusion_config: Path = Path("../facefusion.ini")

    # Limits
    max_image_size_mb: int = 10
    max_video_size_mb: int = 500

    # CORS
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://192.168.50.112:5173",
    ]

    # Logging
    log_level: str = "INFO"

    # App
    app_version: str = "0.1.0"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def max_image_bytes(self) -> int:
        return self.max_image_size_mb * 1024 * 1024

    @property
    def max_video_bytes(self) -> int:
        return self.max_video_size_mb * 1024 * 1024


settings = Settings()
