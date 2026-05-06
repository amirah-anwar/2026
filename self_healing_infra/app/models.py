"""Shared data models for infrastructure resources and events."""

from pydantic import BaseModel
from typing import List, Optional


class ServiceStatus(BaseModel):
    name: str
    is_up: bool
    latency_ms: int
    error_rate: float
    active_failure: Optional[str] = None
    dependencies: List[str] = []


class Alert(BaseModel):
    service: str
    severity: str
    message: str