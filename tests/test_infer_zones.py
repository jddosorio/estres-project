import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from infer_zones import Scan, infer_intervals  # noqa: E402


class InferZonesTest(unittest.TestCase):
    def test_requires_three_windows_and_changes_zone(self):
        start = datetime(2026, 8, 18, tzinfo=timezone.utc)
        scans = []
        for index in range(8):
            gateway = "GW1" if index < 4 else "GW2"
            scans.append(Scan(start + timedelta(seconds=index * 5), gateway, "TAG1", -55))
        intervals = infer_intervals(scans, {"GW1": "Z01", "GW2": "Z05"})
        self.assertEqual([item.zone_id for item in intervals], ["Z01", "Z05"])
        self.assertEqual(sum(item.duration_seconds for item in intervals), 40)

    def test_rejects_weak_signal(self):
        start = datetime(2026, 8, 18, tzinfo=timezone.utc)
        scans = [Scan(start + timedelta(seconds=i * 5), "GW1", "TAG1", -95) for i in range(4)]
        self.assertEqual(infer_intervals(scans, {"GW1": "Z01"}), [])


if __name__ == "__main__":
    unittest.main()

