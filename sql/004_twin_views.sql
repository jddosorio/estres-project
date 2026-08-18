CREATE OR REPLACE VIEW protege.v_twin_weekly_schedule_validation AS
SELECT
    run_id,
    worker_id,
    toMonday(shift_date) AS week_start,
    count() AS simulated_days,
    sum(presence_seconds) AS presence_seconds,
    sum(labor_seconds) AS labor_seconds,
    sum(break_seconds) AS break_seconds,
    round(labor_seconds / 3600, 2) AS labor_hours,
    round(presence_seconds / 3600, 2) AS presence_hours,
    round(avg(time_on_tools_labor_pct), 2) AS average_time_on_tools_labor_pct
FROM protege.twin_daily_kpis
GROUP BY run_id, worker_id, week_start;

CREATE OR REPLACE VIEW protege.v_twin_zone_summary AS
SELECT
    run_id,
    shift_date,
    worker_id,
    zone_id,
    sum(duration_seconds) AS duration_seconds,
    count() AS visits
FROM protege.twin_permanence_intervals
GROUP BY run_id, shift_date, worker_id, zone_id;

CREATE OR REPLACE VIEW protege.v_twin_transition_audit AS
SELECT
    run_id,
    worker_id,
    shift_date,
    countIf(event_type = 'ENTER') AS enter_events,
    countIf(event_type = 'EXIT') AS exit_events,
    enter_events - exit_events AS event_balance
FROM protege.twin_zone_events
GROUP BY run_id, worker_id, shift_date;
