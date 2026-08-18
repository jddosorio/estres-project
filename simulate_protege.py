#!/usr/bin/env python3
"""Generate reproducible BLE scans for a simulated PROTEGE shift."""

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

GATEWAYS = {
    "Z01": "AA:00:00:00:00:01",
    "Z02": "AA:00:00:00:00:02",
    "Z03": "AA:00:00:00:00:03",
    "Z04": "AA:00:00:00:00:04",
    "Z05": "AA:00:00:00:00:05",
}

ROUTE = [
    ("Z01", 3), ("Z02", 10), ("Z03", 15), ("Z04", 8),
    ("Z05", 90), ("Z04", 6), ("Z05", 75), ("Z02", 8), ("Z01", 3),
]


def simulate(output: Path, seed: int = 42) -> None:
    random.seed(seed)
    start = datetime(2026, 8, 18, 11, 0, tzinfo=timezone.utc)
    tag = "BB:00:00:00:00:01"
    sequence = 0
    rows = []
    now = start
    for true_zone, minutes in ROUTE:
        for _ in range(minutes * 6):
            for zone_id, gateway in GATEWAYS.items():
                base = -55 if zone_id == true_zone else -92
                rssi = round(random.gauss(base, 4))
                if random.random() < 0.97:
                    rows.append((now.isoformat(), gateway, tag, rssi, sequence))
                    sequence += 1
            now += timedelta(seconds=10)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["event_time", "gateway_address", "tag_address", "rssi_dbm", "sequence_no"])
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    simulate(args.output, args.seed)

