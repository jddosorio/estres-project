#!/usr/bin/env python3
"""Infer stable worker-zone intervals from BLE RSSI scans."""

import argparse
import csv
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Scan:
    event_time: datetime
    gateway_address: str
    tag_address: str
    rssi_dbm: int


@dataclass(frozen=True)
class Interval:
    tag_address: str
    zone_id: str
    start: datetime
    end: datetime
    confidence: float

    @property
    def duration_seconds(self) -> int:
        return max(0, int((self.end - self.start).total_seconds()))


def floor_time(value: datetime, seconds: int) -> datetime:
    epoch = int(value.timestamp())
    return datetime.fromtimestamp(epoch - epoch % seconds, tz=value.tzinfo)


def window_scores(
    scans: Iterable[Scan], gateways: Dict[str, str], window_seconds: int = 5
) -> Dict[Tuple[str, datetime], Dict[str, float]]:
    grouped: Dict[Tuple[str, datetime, str], List[int]] = defaultdict(list)
    for scan in scans:
        zone = gateways.get(scan.gateway_address.upper())
        if zone:
            window = floor_time(scan.event_time, window_seconds)
            grouped[(scan.tag_address.upper(), window, zone)].append(scan.rssi_dbm)
    scores: Dict[Tuple[str, datetime], Dict[str, float]] = defaultdict(dict)
    for (tag, window, zone), values in grouped.items():
        scores[(tag, window)][zone] = float(statistics.median(values))
    return scores


def infer_intervals(
    scans: Iterable[Scan],
    gateways: Dict[str, str],
    window_seconds: int = 5,
    min_rssi_dbm: int = -85,
    hysteresis_db: int = 6,
    confirm_windows: int = 3,
    timeout_seconds: int = 30,
) -> List[Interval]:
    scores = window_scores(scans, gateways, window_seconds)
    by_tag: Dict[str, List[Tuple[datetime, Dict[str, float]]]] = defaultdict(list)
    for (tag, window), zone_scores in scores.items():
        by_tag[tag].append((window, zone_scores))

    result: List[Interval] = []
    for tag, windows in by_tag.items():
        windows.sort(key=lambda item: item[0])
        current: Optional[str] = None
        current_start: Optional[datetime] = None
        confidence_values: List[float] = []
        candidate: Optional[str] = None
        candidate_count = 0
        previous_window: Optional[datetime] = None

        for window, zone_scores in windows:
            if previous_window and (window - previous_window).total_seconds() > timeout_seconds:
                if current and current_start:
                    result.append(Interval(tag, current, current_start,
                                           previous_window + timedelta(seconds=window_seconds),
                                           min(confidence_values or [0.0])))
                current, current_start, candidate = None, None, None
                candidate_count, confidence_values = 0, []

            best_zone, best_rssi = max(zone_scores.items(), key=lambda item: item[1])
            valid = best_rssi >= min_rssi_dbm
            current_rssi = zone_scores.get(current, -127) if current else -127
            if current and best_zone != current and best_rssi < current_rssi + hysteresis_db:
                best_zone, best_rssi = current, current_rssi
            proposed = best_zone if valid else None

            if current is None:
                if proposed == candidate:
                    candidate_count += 1
                else:
                    candidate, candidate_count = proposed, 1
                if candidate and candidate_count >= confirm_windows:
                    current = candidate
                    current_start = window - timedelta(seconds=(confirm_windows - 1) * window_seconds)
                    confidence_values = [max(0.0, min(1.0, (best_rssi - min_rssi_dbm) / 30.0))]
                    candidate, candidate_count = None, 0
            elif proposed == current:
                candidate, candidate_count = None, 0
                confidence_values.append(max(0.0, min(1.0, (best_rssi - min_rssi_dbm) / 30.0)))
            elif proposed:
                if proposed == candidate:
                    candidate_count += 1
                else:
                    candidate, candidate_count = proposed, 1
                if candidate_count >= confirm_windows and current_start:
                    change_at = window - timedelta(seconds=(confirm_windows - 1) * window_seconds)
                    result.append(Interval(tag, current, current_start, change_at,
                                           min(confidence_values or [0.0])))
                    current, current_start = candidate, change_at
                    confidence_values = [max(0.0, min(1.0, (best_rssi - min_rssi_dbm) / 30.0))]
                    candidate, candidate_count = None, 0
            previous_window = window

        if current and current_start and previous_window:
            result.append(Interval(tag, current, current_start,
                                   previous_window + timedelta(seconds=window_seconds),
                                   min(confidence_values or [0.0])))
    return result


def load_gateways(path: Path) -> Dict[str, str]:
    with path.open(encoding="utf-8") as handle:
        return {row["gateway_address"].upper(): row["zone_id"] for row in csv.DictReader(handle)}


def load_scans(path: Path) -> List[Scan]:
    with path.open(encoding="utf-8") as handle:
        return [Scan(datetime.fromisoformat(row["event_time"]), row["gateway_address"].upper(),
                     row["tag_address"].upper(), int(row["rssi_dbm"]))
                for row in csv.DictReader(handle)]


def write_intervals(path: Path, intervals: Iterable[Interval]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["tag_address", "zone_id", "interval_start", "interval_end",
                         "duration_seconds", "confidence"])
        for item in intervals:
            writer.writerow([item.tag_address, item.zone_id, item.start.isoformat(),
                             item.end.isoformat(), item.duration_seconds,
                             f"{item.confidence:.3f}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scans", type=Path, required=True)
    parser.add_argument("--gateways", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_intervals(args.output, infer_intervals(load_scans(args.scans), load_gateways(args.gateways)))

