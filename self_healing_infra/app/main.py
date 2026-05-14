"""Entry point for the self-healing infrastructure app."""

from fastapi import FastAPI, HTTPException
from app.simulator import ServiceSimulator
from app.monitor import MonitoringEngine
from app.ai_engine import AIRootCauseAnalyzer
from app.healing_engine import SelfHealingEngine
from app.recovery_log import RecoveryLog

recovery_log = RecoveryLog()

app = FastAPI(title="Self-Healing Infrastructure Simulator")

simulator = ServiceSimulator()
monitor = MonitoringEngine()
ai_engine = AIRootCauseAnalyzer()
healing_engine = SelfHealingEngine()

@app.get("/")
def root():
    return {"message": "Self-Healing Infrastructure Simulator is running"}


@app.get("/services")
def get_services():
    simulator.inject_random_behavior()
    return simulator.get_all_services()


@app.get("/services/{service_name}")
def get_service(service_name: str):
    service = simulator.get_service(service_name)

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@app.post("/inject/{service_name}/{failure_type}")
def inject_failure(service_name: str, failure_type: str):
    service = simulator.inject_failure(service_name, failure_type)

    if service is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid service name or failure type"
        )

    return {
        "message": f"Injected {failure_type} into {service_name}",
        "service": service
    }


@app.post("/recover/{service_name}")
def recover_service(service_name: str):
    service = simulator.recover_service(service_name)

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return {
        "message": f"Recovered {service_name}",
        "service": service
    }


@app.get("/monitor")
def monitor_services():
    simulator.apply_dependency_failures()

    services = simulator.get_all_services()
    new_alerts = monitor.evaluate_all_services(services)

    return {
        "services_checked": len(services),
        "new_alerts_generated": len(new_alerts),
        "new_alerts": new_alerts,
        "active_alerts_count": len(monitor.get_alerts()),
        "active_alerts": monitor.get_alerts(),
    }


@app.get("/alerts")
def get_alerts():
    simulator.apply_dependency_failures()

    services = simulator.get_all_services()
    monitor.evaluate_all_services(services)

    return monitor.get_alerts()


@app.delete("/alerts")
def clear_alerts():
    monitor.clear_alerts()

    return {
        "message": "All alerts cleared"
    }


@app.get("/analyze")
def analyze_incident():
    simulator.apply_dependency_failures()
    services = simulator.get_all_services()
    monitor.evaluate_all_services(services)
    alerts = monitor.get_alerts()

    analysis = ai_engine.analyze_alerts(alerts)

    return {
        "total_alerts": len(alerts),
        "alerts": alerts,
        "ai_analysis": analysis
    }


@app.post("/self-heal")
def self_heal():
    simulator.apply_dependency_failures()

    services = simulator.get_all_services()
    monitor.evaluate_all_services(services)

    alerts = monitor.get_alerts()

    actions = healing_engine.determine_actions(alerts)

    results = healing_engine.execute_actions(
        actions,
        simulator
    )

    for result in results:
        recovery_log.add_entry(result)

    # Clear old stale alerts after healing
    monitor.clear_alerts()

    # Re-check current system state after healing
    simulator.apply_dependency_failures()
    updated_services = simulator.get_all_services()
    new_alerts = monitor.evaluate_all_services(updated_services)

    return {
        "alerts_detected_before_healing": len(alerts),
        "actions_planned": actions,
        "execution_results": results,
        "alerts_after_healing": new_alerts,
        "active_alerts_count": len(monitor.get_alerts()),
        "active_alerts": monitor.get_alerts(),
    }


@app.get("/recovery-log")
def get_recovery_log():
    return recovery_log.get_entries()