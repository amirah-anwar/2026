# Self-Healing Infrastructure

Starter project for simulating, monitoring, and responding to infrastructure health events.

# Self-Healing Infrastructure Simulator

## Goal

This project simulates a distributed system with multiple services. It will eventually detect failures, diagnose root causes, and automatically recover using rule-based logic and AI-assisted decision making.

## Current Day 1 Features

- FastAPI backend
- Simulated services
- Service health endpoint
- Random latency and error-rate changes

## Services

- auth-service
- payment-service
- notification-service

## Next Steps

- Add failure injection
- Add monitoring rules
- Add alert generation
- Add AI decision engine
- Add self-healing actions


## Day 2 Features

Added a failure injection engine that can simulate:

- Service crashes
- Latency spikes
- High error rates
- Manual recovery

## Supported Failure Types

- crash
- latency_spike
- high_error_rate