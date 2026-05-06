"""Simulation utilities for infrastructure events."""

import random
from app.models import ServiceStatus


class ServiceSimulator:
    def __init__(self):
        self.services = {
            "auth-service": {
                "is_up": True,
                "latency_ms": 80,
                "error_rate": 0.01,
                "active_failure": None,
            },
            "payment-service": {
                "is_up": True,
                "latency_ms": 120,
                "error_rate": 0.02,
                "active_failure": None,
            },
            "notification-service": {
                "is_up": True,
                "latency_ms": 60,
                "error_rate": 0.01,
                "active_failure": None,
            },
        }

    def get_all_services(self):
        return [
            self._to_status(name, data)
            for name, data in self.services.items()
        ]

    def get_service(self, name):
        if name not in self.services:
            return None
        return self._to_status(name, self.services[name])

    def _to_status(self, name, data):
        return ServiceStatus(
            name=name,
            is_up=data["is_up"],
            latency_ms=data["latency_ms"],
            error_rate=data["error_rate"],
            active_failure=data["active_failure"],
        )

    def inject_random_behavior(self):
        for service in self.services.values():
            if service["active_failure"] is not None:
                continue

            service["latency_ms"] += random.randint(-10, 20)
            service["latency_ms"] = max(20, service["latency_ms"])

            service["error_rate"] += random.uniform(-0.005, 0.01)
            service["error_rate"] = max(0.0, min(service["error_rate"], 1.0))

    def inject_failure(self, service_name, failure_type):
        if service_name not in self.services:
            return None

        service = self.services[service_name]

        if failure_type == "crash":
            service["is_up"] = False
            service["active_failure"] = "crash"

        elif failure_type == "latency_spike":
            service["latency_ms"] = 2000
            service["active_failure"] = "latency_spike"

        elif failure_type == "high_error_rate":
            service["error_rate"] = 0.75
            service["active_failure"] = "high_error_rate"

        else:
            return None

        return self._to_status(service_name, service)

    def recover_service(self, service_name):
        if service_name not in self.services:
            return None

        service = self.services[service_name]
        service["is_up"] = True
        service["latency_ms"] = random.randint(50, 150)
        service["error_rate"] = round(random.uniform(0.01, 0.03), 3)
        service["active_failure"] = None

        return self._to_status(service_name, service)