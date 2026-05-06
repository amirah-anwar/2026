"""Monitoring utilities for infrastructure health checks."""

from app.models import Alert


class MonitoringEngine:
    def __init__(self):
        self.alerts = []
        self.active_alert_keys = set()

    def evaluate_service(self, service):
        generated_alerts = []

        checks = []

        if not service.is_up:
            checks.append((
                "SERVICE_DOWN",
                "CRITICAL",
                "Service is DOWN"
            ))

        if service.latency_ms > 1000:
            checks.append((
                "HIGH_LATENCY",
                "HIGH",
                f"High latency detected: {service.latency_ms}ms"
            ))

        if service.error_rate > 0.5:
            checks.append((
                "HIGH_ERROR_RATE",
                "HIGH",
                f"High error rate detected: {service.error_rate}"
            ))

        if (
            service.active_failure and
            "dependency_failure" in service.active_failure
        ):
            checks.append((
                "DEPENDENCY_FAILURE",
                "CRITICAL",
                f"Cascading dependency issue: {service.active_failure}"
            ))

        for alert_type, severity, message in checks:
            dedup_key = f"{service.name}:{alert_type}"

            if dedup_key not in self.active_alert_keys:
                alert = Alert(
                    service=service.name,
                    severity=severity,
                    message=message
                )

                self.alerts.append(alert)
                self.active_alert_keys.add(dedup_key)
                generated_alerts.append(alert)

        return generated_alerts

    def evaluate_all_services(self, services):
        new_alerts = []

        for service in services:
            alerts = self.evaluate_service(service)
            new_alerts.extend(alerts)

        return new_alerts

    def get_alerts(self):
        return self.alerts

    def clear_alerts(self):
        self.alerts = []
        self.active_alert_keys.clear()