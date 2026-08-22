import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Database Engine
engine = create_engine("mysql+pymysql://root:anas4915??@localhost:3306/ev_fleet_telemetry_db")

# Aggregated Query: Calculate average SoH per cycle interval
query = """
SELECT 
    v.vehicle_model,
    v.battery_chemistry,
    FLOOR(t.charge_cycles / 25) * 25 AS cycle_bracket,
    ROUND(AVG(t.soh) * 100, 2) AS avg_soh_pct,
    ROUND(AVG(t.temperature_c), 2) AS avg_temp_c
FROM fact_telemetry t
JOIN dim_vehicles v ON t.vehicle_id = v.vehicle_id
GROUP BY v.vehicle_model, v.battery_chemistry, cycle_bracket
ORDER BY cycle_bracket ASC;
"""
df = pd.read_sql(query, con=engine)

# Plot Professional Degradation Curves
plt.figure(figsize=(11, 6))

for model in df['vehicle_model'].unique():
    subset = df[df['vehicle_model'] == model]
    plt.plot(
        subset['cycle_bracket'], 
        subset['avg_soh_pct'], 
        marker='o', 
        linewidth=2.2, 
        label=f"{model} ({subset['battery_chemistry'].iloc[0]})"
    )

# 80% Critical Battery Health Threshold Line
plt.axhline(y=80, color='red', linestyle='--', linewidth=1.5, label='Retirement Threshold (80% SoH)')

plt.title('EV Fleet Battery Degradation Trend: State of Health (SoH) vs Usage Cycles', fontsize=13, pad=12, fontweight='bold')
plt.xlabel('Charge Cycles (Normalized)', fontsize=11)
plt.ylabel('State of Health (%)', fontsize=11)
plt.ylim(30, 105)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower left', frameon=True)
plt.tight_layout()

plt.savefig('battery_degradation_trend.png', dpi=300)
print("Updated clean visualization: battery_degradation_trend.png")