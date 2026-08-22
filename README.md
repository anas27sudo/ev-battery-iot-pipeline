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

### Fleet Overview
![Battery Degradation Trend](https://raw.githubusercontent.com/anas27sudo/ev-battery-iot-pipeline/main/battery_degradation_trend.png)

### 🔗 Interactive Fleet Dashboard
**[Click Here to Launch Interactive Dashboard (Filter by Car Model)](https://anas27sudo.github.io/ev-battery-iot-pipeline/battery_interactive_dashboard.html)**

## Key Observations
- Batteries maintained ~88-90% health across extended cycles, staying well above the critical 80% retirement threshold.
- Blade-LFP and standard LFP packs showed lower failure risk scores and better thermal resilience compared to NMC packs under repetitive cycling.

## Fleet Performance & Battery Health Benchmark (SQL Analytics)

Below is the aggregated SQL analysis evaluating State of Health (SoH), operating temperatures, and risk ranking across each vehicle model and battery chemistry:

| Vehicle Model | Chemistry | Battery Capacity | Total Records | Avg SoH (%) | Min SoH (%) | Avg Temp (°C) | Max Temp (°C) | Avg Failure Risk | Overall Rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MG ZS EV** | NMC | 51.1 kWh | 10,000 | 88.41% | 40.01% | 33.25 | 59.99 | 0.0940 | **1** |
| **Tesla Model 3** | NMC | 75.0 kWh | 10,000 | 88.03% | 40.00% | 33.41 | 59.98 | 0.0955 | **2** |
| **BYD Seal** | Blade-LFP | 82.5 kWh | 10,000 | 88.19% | 40.00% | 33.45 | 59.99 | 0.0998 | **3** |
| **Hyundai Ioniq 5** | NMC | 77.4 kWh | 10,000 | 88.30% | 40.01% | 33.29 | 60.00 | 0.1007 | **4** |
| **Nissan Leaf** | LFP | 40.0 kWh | 10,000 | 87.99% | 40.01% | 33.55 | 59.97 | 0.1023 | **5** |

## Tech Stack
- Python (Pandas, SQLAlchemy, Matplotlib, Plotly)
- MySQL