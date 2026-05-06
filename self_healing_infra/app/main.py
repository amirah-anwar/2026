"""Entry point for the self-healing infrastructure app."""

from fastapi import FastAPI, HTTPException
from app.simulator import ServiceSimulator

app = FastAPI(title="Self-Healing Infrastructure Simulator")

simulator = ServiceSimulator()


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