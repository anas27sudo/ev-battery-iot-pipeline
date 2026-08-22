import pandas as pd
import numpy as np

# 1. Load Data
print("Loading raw dataset from data folder...")
df = pd.read_csv('data/ev_iot_raw_telemetry.csv')

# 2. Add Unique Identifiers & Vehicle Mapping
df.reset_index(inplace=True)
df.rename(columns={'index': 'telemetry_id'}, inplace=True)
df['telemetry_id'] = df['telemetry_id'] + 1

# Assign synthetic Vehicle IDs to simulate a 5-vehicle fleet
df['vehicle_id'] = (df['telemetry_id'] % 5) + 1

# 3. Create Vehicles Dimension Table
vehicles_df = pd.DataFrame({
    'vehicle_id': [1, 2, 3, 4, 5],
    'vehicle_model': ['Tesla Model 3', 'Nissan Leaf', 'BYD Seal', 'MG ZS EV', 'Hyundai Ioniq 5'],
    'battery_capacity_kwh': [75.0, 40.0, 82.5, 51.1, 77.4],
    'battery_chemistry': ['NMC', 'LFP', 'Blade-LFP', 'NMC', 'NMC']
})
vehicles_df.to_csv('data/dim_vehicles.csv', index=False)

# 4. Clean & Filter Fact Telemetry Data
telemetry_cols = [
    'telemetry_id', 'vehicle_id', 'Timestamp', 'SoC', 'SoH', 
    'Battery_Voltage', 'Battery_Current', 'Battery_Temperature', 
    'Charge_Cycles', 'Failure_Probability'
]
telemetry_df = df[telemetry_cols].copy()

# Rename columns to standard SQL snake_case
telemetry_df.columns = [
    'telemetry_id', 'vehicle_id', 'recorded_at', 'soc', 'soh', 
    'voltage_v', 'current_a', 'temperature_c', 
    'charge_cycles', 'failure_risk_score'
]

# Take first 50,000 records for fast database loading
telemetry_df.head(50000).to_csv('data/fact_telemetry.csv', index=False)
print("ETL complete: Saved data/dim_vehicles.csv and data/fact_telemetry.csv")