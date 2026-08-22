import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# 1. Database Connection
engine = create_engine("mysql+pymysql://root:anas4915??@localhost:3306/ev_fleet_telemetry_db")

# 2. Fetch Aggregated Telemetry
query = """
SELECT 
    v.vehicle_model,
    v.battery_chemistry,
    FLOOR(t.charge_cycles / 25) * 25 AS cycle_bracket,
    ROUND(AVG(t.soh) * 100, 2) AS avg_soh_pct,
    ROUND(AVG(t.temperature_c), 2) AS avg_temp_c,
    ROUND(AVG(t.failure_risk_score), 4) AS avg_risk
FROM fact_telemetry t
JOIN dim_vehicles v ON t.vehicle_id = v.vehicle_id
GROUP BY v.vehicle_model, v.battery_chemistry, cycle_bracket
ORDER BY cycle_bracket ASC;
"""
df = pd.read_sql(query, con=engine)

# 3. Create Interactive Multi-Model Plotly Figure
fig = go.Figure()
models = df['vehicle_model'].unique()

# Add a trace for each car model
for model in models:
    subset = df[df['vehicle_model'] == model]
    chem = subset['battery_chemistry'].iloc[0]
    fig.add_trace(go.Scatter(
        x=subset['cycle_bracket'],
        y=subset['avg_soh_pct'],
        mode='lines+markers',
        name=f"{model} ({chem})",
        visible=True,
        hovertemplate="<b>Cycle:</b> %{x}<br><b>SoH:</b> %{y}%<br><b>Avg Temp:</b> " + subset['avg_temp_c'].astype(str) + "°C<extra></extra>"
    ))

# 4. Add 80% Threshold Line
fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Retirement Threshold (80% SoH)")

# 5. Build Dropdown Buttons for Single Model Selection
buttons = [
    dict(
        label="All Models (Overview)",
        method="update",
        args=[{"visible": [True] * len(models)}, {"title": "Fleet Overview: All EV Battery Degradation Trends"}]
    )
]

for i, model in enumerate(models):
    visibility = [False] * len(models)
    visibility[i] = True
    buttons.append(
        dict(
            label=f"🚗 {model}",
            method="update",
            args=[{"visible": visibility}, {"title": f"Battery Health Analysis: {model}"}]
        )
    )

fig.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.0,
        xanchor="left",
        y=1.18,
        yanchor="top"
    )],
    title="Fleet Overview: All EV Battery Degradation Trends",
    xaxis_title="Charge Cycles (Normalized)",
    yaxis_title="State of Health (SoH %)",
    yaxis=dict(range=[30, 105]),
    template="plotly_white",
    hovermode="x unified"
)

# 6. Save as Interactive HTML file
fig.write_html("battery_interactive_dashboard.html")
print("Saved: battery_interactive_dashboard.html - Open this file in your browser to interact!")