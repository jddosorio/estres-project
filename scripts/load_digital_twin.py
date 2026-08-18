#!/usr/bin/env python3
"""Load one generated PROTEGE Digital Twin run into ClickHouse Cloud."""

from __future__ import annotations

import argparse
import csv
import json
import tomllib
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

import clickhouse_connect


BATCH_SIZE = 5000


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load_client(secrets_path: Path):
    with secrets_path.open("rb") as handle:
        config = tomllib.load(handle)["clickhouse"]
    return clickhouse_connect.get_client(
        host=config["host"],
        port=int(config.get("port", 8443)),
        username=config["username"],
        password=config["password"],
        database=config.get("database", "default"),
        secure=True,
    )


def chunks(rows: Iterable[Sequence[object]], size: int) -> Iterable[List[Sequence[object]]]:
    batch: List[Sequence[object]] = []
    for row in rows:
        batch.append(row)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def read_csv_rows(
    path: Path,
    converter: Callable[[Dict[str, str]], Sequence[object]],
) -> Iterable[Sequence[object]]:
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            yield converter(row)


def insert_batches(client, table: str, columns: Sequence[str], rows: Iterable[Sequence[object]]) -> int:
    inserted = 0
    for batch in chunks(rows, BATCH_SIZE):
        client.insert(table, batch, column_names=list(columns))
        inserted += len(batch)
        print(f"{table}: {inserted:,} rows inserted")
    return inserted


def existing_counts(client, run_id: uuid.UUID) -> Dict[str, int]:
    safe_run_id = str(run_id)
    tables = (
        "twin_runs",
        "twin_zone_events",
        "twin_permanence_intervals",
        "twin_daily_kpis",
    )
    return {
        table: int(
            client.query(
                f"SELECT count() FROM protege.{table} "
                f"WHERE run_id = toUUID('{safe_run_id}')"
            ).result_rows[0][0]
        )
        for table in tables
    }


def convert_event(row: Dict[str, str]) -> Tuple[object, ...]:
    return (
        uuid.UUID(row["run_id"]),
        uuid.UUID(row["event_id"]),
        row["worker_id"],
        row["tag_address"],
        date.fromisoformat(row["shift_date"]),
        int(row["interval_sequence"]),
        row["zone_id"],
        parse_datetime(row["event_time"]),
        row["event_type"],
        row["event_reason"],
    )


def convert_interval(row: Dict[str, str]) -> Tuple[object, ...]:
    return (
        uuid.UUID(row["run_id"]),
        row["worker_id"],
        row["tag_address"],
        date.fromisoformat(row["shift_date"]),
        int(row["interval_sequence"]),
        row["zone_id"],
        row["activity_code"],
        row["productivity_class"],
        parse_datetime(row["interval_start"]),
        parse_datetime(row["interval_end"]),
        int(row["duration_seconds"]),
        row["source"],
        row["algorithm_version"],
    )


def convert_daily_kpi(row: Dict[str, str]) -> Tuple[object, ...]:
    return (
        uuid.UUID(row["run_id"]),
        date.fromisoformat(row["shift_date"]),
        row["worker_id"],
        row["tag_address"],
        int(row["presence_seconds"]),
        int(row["labor_seconds"]),
        int(row["break_seconds"]),
        int(row["productive_seconds"]),
        int(row["non_productive_planned_seconds"]),
        int(row["non_productive_inferred_seconds"]),
        int(row["support_seconds"]),
        int(row["undefined_seconds"]),
        float(row["time_on_tools_presence_pct"]),
        float(row["time_on_tools_labor_pct"]),
    )


def validate_files(input_dir: Path) -> Dict[str, object]:
    required = (
        "twin_manifest.json",
        "twin_events.csv",
        "twin_intervals.csv",
        "twin_daily_kpis.csv",
    )
    missing = [name for name in required if not (input_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing Digital Twin files: {', '.join(missing)}")
    return json.loads((input_dir / "twin_manifest.json").read_text(encoding="utf-8"))


def load_run(input_dir: Path, secrets_path: Path) -> None:
    manifest = validate_files(input_dir)
    run_id = uuid.UUID(str(manifest["run_id"]))
    client = load_client(secrets_path)

    try:
        client.command("SELECT 1")
        counts = existing_counts(client, run_id)
        if any(counts.values()):
            formatted = ", ".join(f"{name}={count}" for name, count in counts.items())
            raise RuntimeError(
                f"Run {run_id} already has data ({formatted}). "
                "No rows were inserted."
            )

        event_columns = (
            "run_id", "event_id", "worker_id", "tag_address", "shift_date",
            "interval_sequence", "zone_id", "event_time", "event_type", "event_reason",
        )
        interval_columns = (
            "run_id", "worker_id", "tag_address", "shift_date", "interval_sequence",
            "zone_id", "activity_code", "productivity_class", "interval_start",
            "interval_end", "duration_seconds", "source", "algorithm_version",
        )
        kpi_columns = (
            "run_id", "shift_date", "worker_id", "tag_address", "presence_seconds",
            "labor_seconds", "break_seconds", "productive_seconds",
            "non_productive_planned_seconds", "non_productive_inferred_seconds",
            "support_seconds", "undefined_seconds", "time_on_tools_presence_pct",
            "time_on_tools_labor_pct",
        )

        inserted_events = insert_batches(
            client,
            "protege.twin_zone_events",
            event_columns,
            read_csv_rows(input_dir / "twin_events.csv", convert_event),
        )
        inserted_intervals = insert_batches(
            client,
            "protege.twin_permanence_intervals",
            interval_columns,
            read_csv_rows(input_dir / "twin_intervals.csv", convert_interval),
        )
        inserted_kpis = insert_batches(
            client,
            "protege.twin_daily_kpis",
            kpi_columns,
            read_csv_rows(input_dir / "twin_daily_kpis.csv", convert_daily_kpi),
        )

        run_columns = (
            "run_id", "model_name", "algorithm_version", "seed", "start_date",
            "calendar_days", "workers", "simulated_shifts",
            "presence_minutes_per_shift", "lunch_minutes_per_shift",
            "labor_minutes_per_shift", "timezone",
        )
        run_row = (
            run_id,
            manifest["model"],
            manifest["algorithm_version"],
            int(manifest["seed"]),
            date.fromisoformat(str(manifest["start_date"])),
            int(manifest["calendar_days"]),
            int(manifest["workers"]),
            int(manifest["simulated_shifts"]),
            int(manifest["presence_minutes_per_shift"]),
            int(manifest["lunch_minutes_per_shift"]),
            int(manifest["labor_minutes_per_shift"]),
            manifest["timezone"],
        )
        client.insert("protege.twin_runs", [run_row], column_names=list(run_columns))

        final_counts = existing_counts(client, run_id)
        expected = {
            "twin_runs": 1,
            "twin_zone_events": inserted_events,
            "twin_permanence_intervals": inserted_intervals,
            "twin_daily_kpis": inserted_kpis,
        }
        if final_counts != expected:
            raise RuntimeError(f"Final count mismatch: expected={expected}, actual={final_counts}")

        invalid_days = int(
            client.query(
                "SELECT count() FROM protege.twin_daily_kpis "
                f"WHERE run_id = toUUID('{run_id}') AND "
                "(presence_seconds != 32400 OR labor_seconds != 30240 "
                "OR break_seconds != 2160)"
            ).result_rows[0][0]
        )
        event_balance = client.query(
            "SELECT countIf(event_type = 'ENTER') - countIf(event_type = 'EXIT') "
            "FROM protege.twin_zone_events "
            f"WHERE run_id = toUUID('{run_id}')"
        ).result_rows[0][0]

        if invalid_days != 0 or int(event_balance) != 0:
            raise RuntimeError(
                f"Validation failed: invalid_days={invalid_days}, "
                f"event_balance={event_balance}"
            )

        print("\nDigital Twin load completed successfully")
        print(f"run_id: {run_id}")
        for table, count in final_counts.items():
            print(f"{table}: {count:,}")
        print("daily schedule validation: OK")
        print("ENTER/EXIT balance: OK")
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("sample_data/digital_twin_6m"),
    )
    parser.add_argument(
        "--secrets",
        type=Path,
        default=Path(".streamlit/secrets.toml"),
    )
    args = parser.parse_args()
    load_run(args.input_dir, args.secrets)
