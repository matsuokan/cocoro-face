"""
In-memory job store for Phase 1.
Phase 2 will replace this with SQLite persistence.
"""
from __future__ import annotations

import threading
from typing import Optional

from models.schemas import JobRecord


class JobService:
    """Thread-safe in-memory job registry."""

    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = threading.Lock()

    def create(self, record: JobRecord) -> JobRecord:
        with self._lock:
            self._jobs[record.job_id] = record
        return record

    def get(self, job_id: str) -> Optional[JobRecord]:
        with self._lock:
            return self._jobs.get(job_id)

    def update(self, record: JobRecord) -> Optional[JobRecord]:
        with self._lock:
            if record.job_id not in self._jobs:
                return None
            self._jobs[record.job_id] = record
        return record

    def delete(self, job_id: str) -> bool:
        with self._lock:
            if job_id not in self._jobs:
                return False
            del self._jobs[job_id]
        return True

    def all_jobs(self) -> list[JobRecord]:
        with self._lock:
            return list(self._jobs.values())


# Module-level singleton
job_service = JobService()
