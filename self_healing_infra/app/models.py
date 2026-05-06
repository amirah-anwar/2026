"""Shared data models for infrastructure resources and events."""

from pydantic import BaseModel
from typing import Optional


class ServiceStatus(BaseModel):
    name: str
    is_up: bool
    latency_ms: int
    error_rate: float
    active_failure: Optional[str] = None