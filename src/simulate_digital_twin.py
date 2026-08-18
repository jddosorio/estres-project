#!/usr/bin/env python3
"""Generate the ideal (ground-truth) PROTEGE Digital Twin timeline.

This simulator does not generate or interpret RSSI.  It produces the exact
zone events and permanence intervals that the future BLE inference layer must
reconstruct.  All stored timestamps are UTC; shift construction uses the
America/Santiago civil timezone.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import uuid
from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
from zoneinfo import ZoneInfo


CHILE_TZ = ZoneInfo("America/Santiago")
SHIFT_PRESENCE_MINUTES = 9 * 60
LUNCH_MINUTES = 36
DAILY_LABOR_MINUTES = SHIFT_PRESENCE_MINUTES - LUNCH_MINUTES
ALGORITHM_VERSION = "digital-twin-ground-truth-v1"


ZONE_METADATA: Dict[str, Tuple[str, str, str]] = {
    "Z00": ("Undefined / Transit", "UNDEFINED", "UNKNOWN"),
    "Z01": ("Site access", "ACCESS", "SUPPORT"),
    "Z02": ("Change house", "CHANGE_HOUSE", "NON_PRODUCTIVE_PLANNED"),
    "Z03": ("Instructions", "INSTRUCTIONS", "NON_PRODUCTIVE_PLANNED"),
    "Z04": ("Tools", "TOOLS", "NON_PRODUCTIVE_INFERRED"),
    "Z05-A": ("Work zone A", "WORK_FACE", "PRODUCTIVE"),
    "Z05-B": ("Work zone B", "WORK_FACE", "PRODUCTIVE"),
    "Z05-C": ("Work zone C", "WORK_FACE", "PRODUCTIVE"),
    "Z06": ("Lunch", "LUNCH", "BREAK"),
}

WORK_ZONES = ("Z05-A", "Z05-B", "Z05-C")


@dataclass(frozen=True)
class TwinInterval:
    run_id: str
    worker_id: str
    tag_address: str
    shift_date: str
    interval_sequence: int
    zone_id: str
    activity_code: str
    productivity_class: str
    interval_start: str
    interval_end: str
    duration_seconds: int
    source: str = "DIGITAL_TWIN_GROUND_TRUTH"
    algorithm_version: str = ALGORITHM_VERSION


@dataclass(frozen=True)
class TwinEvent:
    run_id: str
    event_id: str
    worker_id: str
    tag_address: str
    shift_date: str
    interval_sequence: int
    zone_id: str
    event_time: str
    event_type: str
    event_reason: str = "IDEAL_GROUND_TRUTH"


def worker_identity(index: int) -> Tuple[str, str]:
    return (
        f"W-{index:03d}",
        f"BB:00:00:00:{(index // 256):02X}:{(index % 256):02X}",
    )


def utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds")


def add_segment(
    output: List[Tuple[str, datetime, datetime]],
    zone_id: str,
    start: datetime,
    minutes: int,
) -> datetime:
    if minutes <= 0:
        return start
    end = start + timedelta(minutes=minutes)
    output.append((zone_id, start, end))
    return end


def simulate_shift(day: date, worker_index: int, rng: random.Random) -> List[Tuple[str, datetime, datetime]]:
    """Build one exact nine-hour presence timeline with a 36-minute lunch."""
    jitter_minutes = max(-8, min(8, round(rng.gauss(0, 4))))
    start = datetime.combine(day, time(8, 0), tzinfo=CHILE_TZ) + timedelta(
        minutes=jitter_minutes
    )
    shift_end = start + timedelta(minutes=SHIFT_PRESENCE_MINUTES)

    access_in = rng.randint(3, 5)
    change_in = rng.randint(8, 15)
    instructions = rng.randint(10, 20)
    tools_in = rng.randint(5, 10)
    transit_minutes = [rng.randint(1, 3) for _ in range(7)]

    tools_out = rng.randint(3, 7)
    change_out = rng.randint(6, 10)
    access_out = rng.randint(3, 5)

    first_work_zone = rng.choice(WORK_ZONES)
    if rng.random() < 0.35:
        second_work_zone = rng.choice([zone for zone in WORK_ZONES if zone != first_work_zone])
    else:
        second_work_zone = first_work_zone

    segments: List[Tuple[str, datetime, datetime]] = []
    cursor = start
    cursor = add_segment(segments, "Z01", cursor, access_in)
    cursor = add_segment(segments, "Z00", cursor, transit_minutes[0])
    cursor = add_segment(segments, "Z02", cursor, change_in)
    cursor = add_segment(segments, "Z00", cursor, transit_minutes[1])
    cursor = add_segment(segments, "Z03", cursor, instructions)
    cursor = add_segment(segments, "Z00", cursor, transit_minutes[2])
    cursor = add_segment(segments, "Z04", cursor, tools_in)
    cursor = add_segment(segments, "Z00", cursor, transit_minutes[3])

    lunch_target = start + timedelta(minutes=240 + rng.randint(-10, 10))
    first_work_minutes = max(60, int((lunch_target - cursor).total_seconds() // 60))
    cursor = add_segment(segments, first_work_zone, cursor, first_work_minutes)
    cursor = add_segment(segments, "Z06", cursor, LUNCH_MINUTES)

    if second_work_zone != first_work_zone:
        cursor = add_segment(segments, "Z00", cursor, transit_minutes[4])

    reserved_tail = (
        transit_minutes[5]
        + tools_out
        + transit_minutes[6]
        + change_out
        + access_out
    )
    second_work_minutes = int((shift_end - cursor).total_seconds() // 60) - reserved_tail
    if second_work_minutes < 60:
        raise ValueError("Generated shift leaves insufficient time for the second work block")

    cursor = add_segment(segments, second_work_zone, cursor, second_work_minutes)
    cursor = add_segment(segments, "Z00", cursor, transit_minutes[5])
    cursor = add_segment(segments, "Z04", cursor, tools_out)
    cursor = add_segment(segments, "Z00", cursor, transit_minutes[6])
    cursor = add_segment(segments, "Z02", cursor, change_out)
    cursor = add_segment(segments, "Z01", cursor, access_out)

    if cursor != shift_end:
        raise AssertionError(f"Shift does not close at nine hours: {cursor=} {shift_end=}")
    return segments


def make_intervals_and_events(
    run_id: str,
    worker_id: str,
    tag_address: str,
    shift_date: date,
    segments: Sequence[Tuple[str, datetime, datetime]],
) -> Tuple[List[TwinInterval], List[TwinEvent]]:
    intervals: List[TwinInterval] = []
    events: List[TwinEvent] = []
    namespace = uuid.UUID(run_id)

    for sequence, (zone_id, start, end) in enumerate(segments, start=1):
        _, activity_code, productivity_class = ZONE_METADATA[zone_id]
        interval = TwinInterval(
            run_id=run_id,
            worker_id=worker_id,
            tag_address=tag_address,
            shift_date=shift_date.isoformat(),
            interval_sequence=sequence,
            zone_id=zone_id,
            activity_code=activity_code,
            productivity_class=productivity_class,
            interval_start=utc_iso(start),
            interval_end=utc_iso(end),
            duration_seconds=int((end - start).total_seconds()),
        )
        intervals.append(interval)

        for event_type, event_time in (("ENTER", start), ("EXIT", end)):
            event_name = (
                f"{worker_id}:{shift_date.isoformat()}:{sequence}:{zone_id}:{event_type}"
            )
            events.append(
                TwinEvent(
                    run_id=run_id,
                    event_id=str(uuid.uuid5(namespace, event_name)),
                    worker_id=worker_id,
                    tag_address=tag_address,
                    shift_date=shift_date.isoformat(),
                    interval_sequence=sequence,
                    zone_id=zone_id,
                    event_time=utc_iso(event_time),
                    event_type=event_type,
                )
            )
    return intervals, events


def daily_kpi(intervals: Sequence[TwinInterval]) -> Dict[str, object]:
    seconds_by_class: Dict[str, int] = {}
    for interval in intervals:
        seconds_by_class[interval.productivity_class] = (
            seconds_by_class.get(interval.productivity_class, 0)
            + interval.duration_seconds
        )

    presence_seconds = sum(item.duration_seconds for item in intervals)
    break_seconds = seconds_by_class.get("BREAK", 0)
    labor_seconds = presence_seconds - break_seconds
    productive_seconds = seconds_by_class.get("PRODUCTIVE", 0)

    return {
        "run_id": intervals[0].run_id,
        "shift_date": intervals[0].shift_date,
        "worker_id": intervals[0].worker_id,
        "tag_address": intervals[0].tag_address,
        "presence_seconds": presence_seconds,
        "labor_seconds": labor_seconds,
        "break_seconds": break_seconds,
        "productive_seconds": productive_seconds,
        "non_productive_planned_seconds": seconds_by_class.get(
            "NON_PRODUCTIVE_PLANNED", 0
        ),
        "non_productive_inferred_seconds": seconds_by_class.get(
            "NON_PRODUCTIVE_INFERRED", 0
        ),
        "support_seconds": seconds_by_class.get("SUPPORT", 0),
        "undefined_seconds": seconds_by_class.get("UNKNOWN", 0),
        "time_on_tools_presence_pct": round(
            100 * productive_seconds / presence_seconds, 2
        ),
        "time_on_tools_labor_pct": round(
            100 * productive_seconds / labor_seconds, 2
        ),
    }


def write_dataclasses(path: Path, rows: Iterable[object], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_dicts(path: Path, rows: Iterable[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate(
    output_dir: Path,
    start_date: date,
    days: int,
    workers: int,
    seed: int,
    absence_rate: float = 0.0,
) -> Dict[str, object]:
    rng = random.Random(seed)
    run_id = str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"protege-digital-twin:{start_date.isoformat()}:{days}:{workers}:{seed}",
        )
    )

    all_intervals: List[TwinInterval] = []
    all_events: List[TwinEvent] = []
    all_daily_kpis: List[Dict[str, object]] = []
    simulated_shifts = 0

    for day_offset in range(days):
        shift_date = start_date + timedelta(days=day_offset)
        if shift_date.weekday() >= 5:
            continue
        for worker_index in range(1, workers + 1):
            if rng.random() < absence_rate:
                continue
            worker_id, tag_address = worker_identity(worker_index)
            segments = simulate_shift(shift_date, worker_index, rng)
            intervals, events = make_intervals_and_events(
                run_id, worker_id, tag_address, shift_date, segments
            )
            all_intervals.extend(intervals)
            all_events.extend(events)
            all_daily_kpis.append(daily_kpi(intervals))
            simulated_shifts += 1

    write_dataclasses(
        output_dir / "twin_intervals.csv",
        all_intervals,
        list(TwinInterval.__dataclass_fields__),
    )
    write_dataclasses(
        output_dir / "twin_events.csv",
        all_events,
        list(TwinEvent.__dataclass_fields__),
    )
    if all_daily_kpis:
        write_dicts(
            output_dir / "twin_daily_kpis.csv",
            all_daily_kpis,
            list(all_daily_kpis[0]),
        )

    zone_rows = [
        {
            "zone_id": zone_id,
            "zone_name": values[0],
            "activity_code": values[1],
            "productivity_class": values[2],
        }
        for zone_id, values in ZONE_METADATA.items()
    ]
    write_dicts(
        output_dir / "twin_zones.csv",
        zone_rows,
        ["zone_id", "zone_name", "activity_code", "productivity_class"],
    )

    manifest = {
        "run_id": run_id,
        "model": "PROTEGE Digital Twin - ideal ground truth",
        "algorithm_version": ALGORITHM_VERSION,
        "seed": seed,
        "start_date": start_date.isoformat(),
        "calendar_days": days,
        "workers": workers,
        "absence_rate": absence_rate,
        "simulated_shifts": simulated_shifts,
        "presence_minutes_per_shift": SHIFT_PRESENCE_MINUTES,
        "lunch_minutes_per_shift": LUNCH_MINUTES,
        "labor_minutes_per_shift": DAILY_LABOR_MINUTES,
        "labor_hours_per_five_day_week": 42,
        "timezone": "America/Santiago",
        "timestamps_stored_as": "UTC",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "twin_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate ideal PROTEGE Digital Twin zone events and intervals"
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--start-date", type=parse_date, default=date(2026, 1, 5))
    parser.add_argument("--days", type=int, default=182)
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--absence-rate", type=float, default=0.0)
    args = parser.parse_args()

    result = generate(
        args.output_dir,
        args.start_date,
        args.days,
        args.workers,
        args.seed,
        args.absence_rate,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
