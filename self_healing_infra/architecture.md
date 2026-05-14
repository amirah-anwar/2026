# Architecture Overview

## Components

### 1. Service Simulator
Simulates distributed infrastructure services and runtime failures.

### 2. Monitoring Engine
Evaluates service health and generates alerts.

### 3. AI Root Cause Analyzer
Performs incident summarization and remediation recommendations.

### 4. Self-Healing Engine
Executes autonomous recovery actions.

### 5. Recovery Log
Stores recovery audit history.

---

# High-Level Flow

```text
Failure Injection
        ↓
Service Degradation
        ↓
Monitoring Engine
        ↓
Alert Generation
        ↓
AI Root Cause Analysis
        ↓
Self-Healing Engine
        ↓
Recovery Execution
        ↓
Post-Recovery Validation