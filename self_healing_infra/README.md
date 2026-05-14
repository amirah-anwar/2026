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

## Day 3 Features

Added monitoring and alerting engine.

Current monitoring capabilities:
- Detect crashed services
- Detect high latency
- Detect high error rates
- Generate severity-based alerts
- Store historical alerts

## Alert Severity Levels

- CRITICAL
- HIGH

## Day 4 Features

Added intelligent dependency-aware monitoring.

New capabilities:
- Service dependency graph
- Cascading failure simulation
- Dependency-based degradation
- Alert deduplication
- Smarter severity classification

## Example Dependency Chain

auth-service
    ↓
payment-service
    ↓
notification-service

# Day 5 — AI Root Cause Analysis Engine

## Overview

Day 5 introduced AI-assisted incident analysis capabilities into the Self-Healing Infrastructure Simulator.

The system can now:
- analyze infrastructure alerts
- summarize incidents
- infer probable root causes
- recommend remediation actions

This transforms the project from a monitoring simulator into an AI-assisted operations platform.

---

# Features Added

## AI Root Cause Analysis

Added an AI analysis engine capable of:
- interpreting infrastructure alerts
- identifying likely upstream failures
- explaining cascading service degradation
- recommending recovery actions

Example analysis output:

```json
{
  "summary": "Auth service failure caused cascading dependency degradation.",
  "root_cause": "auth-service crashed",
  "recommended_action": "Restart auth-service and verify downstream recovery."
}

# Day 6 — Self-Healing Action Engine

## Overview

Day 6 introduced autonomous remediation capabilities into the Self-Healing Infrastructure Simulator.

The system can now:
- detect infrastructure failures
- determine recovery actions
- automatically recover services
- validate post-recovery health
- maintain recovery audit logs

This transforms the project from an AI-assisted monitoring platform into a self-healing infrastructure system.

---

# Features Added

## Self-Healing Engine

Implemented an autonomous remediation engine capable of:
- evaluating infrastructure alerts
- determining corrective actions
- executing recovery workflows

Current supported actions:
- restart failed services
- investigate dependency failures

---

# Autonomous Recovery Workflow

### POST `/self-heal`

The recovery workflow now performs:

1. dependency evaluation
2. monitoring analysis
3. alert collection
4. remediation planning
5. automated action execution
6. post-recovery validation

Response includes:
- detected alerts
- planned recovery actions
- execution results
- updated system health state

---

# Safety Controls

Added operational safety mechanisms:
- confidence-based execution thresholds
- selective action execution
- controlled recovery behavior

These controls prevent unsafe automated remediation.

---

# Recovery Logging

Implemented recovery audit logging.

### GET `/recovery-log`

Returns:
- executed remediation actions
- affected services
- recovery status
- action history

This enables operational auditing and debugging.

---

# Automatic Alert Cleanup

Implemented:
- stale alert clearing
- post-recovery monitoring
- dependency state cleanup

Alerts now accurately reflect current infrastructure health after remediation.

---

# Dependency Recovery Handling

Improved cascading failure recovery behavior.

When upstream services recover:
- dependent services automatically stabilize
- latency resets
- error rates normalize
- dependency failure states clear

Example:

```text
auth-service crashes
        ↓
payment-service degrades
        ↓
notification-service degrades
        ↓
self-heal recovers auth-service
        ↓
dependent services stabilize