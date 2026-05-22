# AI Infrastructure Planning & Placement Agent

## Overview

Infrastructure placement platform that recommends workload placement based on:

- capacity
- latency
- cost
- forecasting
- self-healing migration

## Features

### Placement engine

Scores infrastructure clusters using:

- capacity
- latency
- cost

### Capacity forecasting

Forecasts CPU and GPU growth.

### Self healing

Detects predicted exhaustion and recommends migration.

### API

FastAPI backend.

### Dashboard

Streamlit visualization.

### Docker

Containerized deployment.

## Architecture

Dashboard

↓

FastAPI

↓

Placement Engine

↓

Capacity Forecast Engine

↓

Self Healing Engine

↓

Infrastructure Data



## How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run dashboard.py