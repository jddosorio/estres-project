import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from simulate_digital_twin import (  # noqa: E402
    DAILY_LABOR_MINUTES,
    LUNCH_MINUTES,
    SHIFT_PRESENCE_MINUTES,
    generate,
    make_intervals_and_events,
    simulate_shift,
    worker_identity,
)

import random  # noqa: E402


class DigitalTwinTest(unittest.TestCase):
    def test_shift_has_nine_hours_and_36_minute_lunch(self):
        segments = simulate_shift(date(2026, 1, 5), 1, random.Random(42))
        presence_seconds = int((segments[-1][2] - segments[0][1]).total_seconds())
        lunch_seconds = sum(
            int((end - start).total_seconds())
            for zone, start, end in segments
            if zone == "Z06"
        )

        self.assertEqual(presence_seconds, SHIFT_PRESENCE_MINUTES * 60)
        self.assertEqual(lunch_seconds, LUNCH_MINUTES * 60)
        self.assertEqual(presence_seconds - lunch_seconds, DAILY_LABOR_MINUTES * 60)

    def test_intervals_are_contiguous_and_events_are_balanced(self):
        shift_date = date(2026, 1, 5)
        segments = simulate_shift(shift_date, 1, random.Random(7))
        worker_id, tag_address = worker_identity(1)
        run_id = "11111111-1111-5111-8111-111111111111"
        intervals, events = make_intervals_and_events(
            run_id, worker_id, tag_address, shift_date, segments
        )

        for current, following in zip(intervals, intervals[1:]):
            self.assertEqual(
                datetime.fromisoformat(current.interval_end),
                datetime.fromisoformat(following.interval_start),
            )

        self.assertEqual(len(events), 2 * len(intervals))
        self.assertEqual(
            sum(event.event_type == "ENTER" for event in events),
            sum(event.event_type == "EXIT" for event in events),
        )

    def test_five_day_week_contains_42_labor_hours(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = generate(
                Path(directory),
                start_date=date(2026, 1, 5),
                days=7,
                workers=1,
                seed=42,
            )
            self.assertEqual(manifest["simulated_shifts"], 5)

            import csv

            with (Path(directory) / "twin_daily_kpis.csv").open(encoding="utf-8") as handle:
                labor_seconds = sum(int(row["labor_seconds"]) for row in csv.DictReader(handle))
            self.assertEqual(labor_seconds, 42 * 3600)


if __name__ == "__main__":
    unittest.main()
