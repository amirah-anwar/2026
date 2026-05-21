from dataclasses import dataclass
from typing import Optional


@dataclass
class Cluster:
    name: str
    region: str
    cpu_available: int
    gpu_available: int
    memory_available: int
    cost_per_hour: float
    latency_ms: int


@dataclass
class Workload:
    name: str
    cpu_required: int
    gpu_required: int
    memory_required: int
    preferred_region: Optional[str]
    max_latency_ms: int