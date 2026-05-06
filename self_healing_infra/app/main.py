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