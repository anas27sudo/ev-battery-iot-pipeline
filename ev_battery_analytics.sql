USE ev_fleet_telemetry_db;

SELECT 
    v.vehicle_model,
    v.battery_chemistry,
    v.battery_capacity_kwh,
    COUNT(t.telemetry_id) AS total_records,
    ROUND(AVG(t.soh) * 100, 2) AS avg_soh_pct,
    ROUND(MIN(t.soh) * 100, 2) AS min_soh_pct,
    ROUND(AVG(t.temperature_c), 2) AS avg_operating_temp_c,
    ROUND(MAX(t.temperature_c), 2) AS max_operating_temp_c,
    ROUND(AVG(t.failure_risk_score), 4) AS avg_failure_risk,
    -- Rank based on minimum risk and maximum SoH retention
    DENSE_RANK() OVER (ORDER BY AVG(t.failure_risk_score) ASC, AVG(t.soh) DESC) AS overall_rank
FROM dim_vehicles v
JOIN fact_telemetry t ON v.vehicle_id = t.vehicle_id
GROUP BY v.vehicle_id, v.vehicle_model, v.battery_chemistry, v.battery_capacity_kwh
ORDER BY overall_rank ASC;