USE ev_fleet_telemetry_db;


-- ==========================================================
-- 1. DATASET VERIFICATION
-- ==========================================================


SELECT COUNT(*) AS total_telemetry_records FROM fact_telemetry;


-- ==========================================================
-- 2. STATE OF HEALTH (SoH) vs CHARGE CYCLES (BRACKETED)
-- ==========================================================


SELECT 
    v.vehicle_model,
    v.battery_chemistry,
    FLOOR(t.charge_cycles / 50) * 50 AS cycle_bracket,
    ROUND(AVG(t.soh) * 100, 2) AS avg_soh_pct,
    ROUND(AVG(t.temperature_c), 2) AS avg_operating_temp,
    ROUND(AVG(t.voltage_v), 2) AS avg_voltage
FROM fact_telemetry t
JOIN dim_vehicles v ON t.vehicle_id = v.vehicle_id
GROUP BY v.vehicle_model, v.battery_chemistry, cycle_bracket
ORDER BY v.vehicle_model, cycle_bracket ASC;


-- ==========================================================
-- 3. TOP HIGH STRESS ANOMALY EVENTS (CTE + WINDOW FUNCTION)
-- ==========================================================


WITH RankedStressEvents AS (
    SELECT 
        v.vehicle_model,
        t.recorded_at,
        t.temperature_c,
        t.voltage_v,
        t.failure_risk_score,
        DENSE_RANK() OVER (PARTITION BY t.vehicle_id ORDER BY t.failure_risk_score DESC) AS risk_rank
    FROM fact_telemetry t
    JOIN dim_vehicles v ON t.vehicle_id = v.vehicle_id
    WHERE t.temperature_c > 40.0
)
SELECT * 
FROM RankedStressEvents 
WHERE risk_rank <= 3;


-- ==========================================================
-- 4. OVERALL FLEET PERFORMANCE & RELIABILITY RANKING
-- ==========================================================
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
    DENSE_RANK() OVER (ORDER BY AVG(t.failure_risk_score) ASC, AVG(t.soh) DESC) AS overall_rank
FROM dim_vehicles v
JOIN fact_telemetry t ON v.vehicle_id = t.vehicle_id
GROUP BY v.vehicle_id, v.vehicle_model, v.battery_chemistry, v.battery_capacity_kwh
ORDER BY overall_rank ASC;