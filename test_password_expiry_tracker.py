import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from datetime import date
from main import check_users


class TestPasswordExpiry(unittest.TestCase):
    def test_expired_and_ok(self):
        rows = [{"username": "old", "last_changed": "2026-01-01", "max_age_days": "90"},
                {"username": "new", "last_changed": "2026-10-20", "max_age_days": "90"}]
        out = check_users(rows, date(2026, 10, 27), 7)
        self.assertEqual(out[0]["username"], "old")
        self.assertEqual(out[0]["status"], "expired")
        self.assertEqual(out[1]["status"], "ok")

    def test_expiring_soon_threshold(self):
        rows = [{"username": "soon", "last_changed": "2026-10-01", "max_age_days": "30"}]
        out = check_users(rows, date(2026, 10, 27), 7)
        self.assertEqual(out[0]["status"], "expiring-soon")
        self.assertEqual(out[0]["days_left"], 4)

    def test_sorted_by_days_left(self):
        rows = [{"username": "b", "last_changed": "2026-10-20", "max_age_days": "90"},
                {"username": "a", "last_changed": "2026-01-01", "max_age_days": "90"}]
        out = check_users(rows, date(2026, 10, 27), 7)
        self.assertEqual([r["username"] for r in out], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
