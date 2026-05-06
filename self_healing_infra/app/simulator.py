"""Simulation utilities for infrastructure events."""

import random
from app.models import ServiceStatus


class ServiceSimulator:
    def __init__(self):
        self.services = {
            "auth-service": {
                "is_up": True,
                "latency_ms": 80,
                "error_rate": 0.01
            },
            "payment-service": {
                "is_up": True,
                "latency_ms": 120,
                "error_rate": 0.02
            },
            "notification-service": {
                "is_up": True,
                "latency_ms": 60,
                "error_rate": 0.01
            }
        }

    def get_all_services(self):
        return [
            ServiceStatus(
                name=name,
                is_up=data["is_up"],
                latency_ms=data["latency_ms"],
                error_rate=data["error_rate"]
            )
            for name, data in self.services.items()
        ]

    def get_service(self, name):
        if name not in self.services:
            return None

        data = self.services[name]

        return ServiceStatus(
            name=name,
            is_up=data["is_up"],
            latency_ms=data["latency_ms"],
            error_rate=data["error_rate"]
        )

    def inject_random_behavior(self):
        for service in self.services.values():
            service["latency_ms"] += random.randint(-10, 20)
            service["latency_ms"] = max(20, service["latency_ms"])

            service["error_rate"] += random.uniform(-0.005, 0.01)
            service["error_rate"] = max(0.0, min(service["error_rate"], 1.0))