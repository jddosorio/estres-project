CREATE OR REPLACE VIEW protege.v_worker_daily_kpi AS
SELECT
    shift_date,
    worker_id,
    dateDiff('second', min(interval_start), max(interval_end)) AS presence_seconds,
    sum(duration_seconds) AS located_seconds,
    sumIf(duration_seconds, productivity_class = 'PRODUCTIVE') AS productive_seconds,
    sumIf(duration_seconds, productivity_class IN
        ('NON_PRODUCTIVE_PLANNED', 'NON_PRODUCTIVE_INFERRED')) AS non_productive_seconds,
    sumIf(duration_seconds, productivity_class = 'SUPPORT') AS support_seconds,
    greatest(presence_seconds - located_seconds, 0) +
        sumIf(duration_seconds, productivity_class = 'UNKNOWN') AS unknown_seconds,
    round(100 * productive_seconds / nullIf(presence_seconds, 0), 2) AS time_on_tools_pct,
    round(100 * (presence_seconds - unknown_seconds) / nullIf(presence_seconds, 0), 2) AS coverage_pct,
    sumIf(duration_seconds, activity_code = 'CHANGE_HOUSE') AS change_house_seconds,
    sumIf(duration_seconds, activity_code = 'INSTRUCTIONS') AS instructions_seconds,
    sumIf(duration_seconds, activity_code = 'TOOLS') AS tools_area_seconds,
    sumIf(duration_seconds, activity_code = 'WORK_FACE') AS work_face_seconds
FROM protege.worker_zone_intervals
GROUP BY shift_date, worker_id;
