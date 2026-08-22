# EV Battery Telemetry Pipeline & Health Analytics

A project to ingest, structure, and analyze real-world Electric Vehicle (EV) battery IoT sensor data across multiple car models and battery chemistries.

## What this project does
- Cleans and structures raw IoT telemetry logs into a relational database.
- Normalizes vehicle metadata (`dim_vehicles`) and telemetry readings (`fact_telemetry`).
- Loads processed datasets into MySQL using SQLAlchemy.
- Tracks State of Health (SoH) degradation across 600+ charge cycles using SQL analytics (Window Functions, CTEs).
- Visualizes battery health trends and individual vehicle performance using Matplotlib and an interactive Plotly dashboard.

## Database Schema
- **dim_vehicles**: `vehicle_id`, `vehicle_model`, `battery_capacity_kwh`, `battery_chemistry`
- **fact_telemetry**: `telemetry_id`, `vehicle_id`, `recorded_at`, `soc`, `soh`, `voltage_v`, `current_a`, `temperature_c`, `charge_cycles`, `failure_risk_score`

## Degradation Analysis
![Battery Degradation Trend](https://raw.githubusercontent.com/anas27sudo/ev-battery-iot-pipeline/main/battery_degradation_trend.png)

## Key Observations
- Batteries maintained ~88-90% health across extended cycles, staying well above the critical 80% retirement threshold.
- Blade-LFP and standard LFP packs showed lower failure risk scores and better thermal resilience compared to NMC packs under repetitive cycling.

## Tech Stack
- Python (Pandas, SQLAlchemy, Matplotlib, Plotly)
- MySQL