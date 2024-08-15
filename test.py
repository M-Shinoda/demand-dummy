from datetime import datetime, timedelta
import unittest

from usage_fee import unit_price
from util import is_time_overlap


class UsageFeeTest(unittest.TestCase):
    parking_name = "中央駐車場"

    def test_holiday_mornig(self):
        record = {
            "entryTime": "2023-01-01T08:00:00+09:00",
            "exitTime": "2023-01-01T09:01:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 300)

    def test_holiday_mornig_fixed_price(self):
        record = {
            "entryTime": "2023-01-01T08:00:00+09:00",
            "exitTime": "2023-01-01T17:00:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 1200)

    def test_weekday_mornig(self):
        record = {
            "entryTime": "2023-01-02T08:00:00+09:00",
            "exitTime": "2023-01-02T09:01:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 300)

    def test_weekday_mornig_no_fixed_price(self):
        record = {
            "entryTime": "2023-01-02T08:00:00+09:00",
            "exitTime": "2023-01-02T17:00:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 2200)

    def test_holiday_straddle_the_section_1(self):
        record = {
            "entryTime": "2023-01-02T17:23:00+09:00",
            "exitTime": "2023-01-02T21:46:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 1000)

    def test_holiday_straddle_the_section_2(self):
        record = {
            "entryTime": "2023-01-02T17:23:00+09:00",
            "exitTime": "2023-01-03T07:46:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 1000)

    def test_holiday_straddle_the_section_3(self):
        record = {
            "entryTime": "2023-01-02T17:23:00+09:00",
            "exitTime": "2023-01-03T08:46:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        result = unit_price(self.parking_name, entry_time, exit_time)
        self.assertEqual(result, 1200)


class IsTimeOverlapTest(unittest.TestCase):
    def test_time_overlap(self):
        record = {
            "entryTime": "2023-01-03T21:40:00+09:00",
            "exitTime": "2023-01-04T00:16:00+09:00",
        }
        entry_time = datetime.fromisoformat(record["entryTime"])
        exit_time = datetime.fromisoformat(record["exitTime"])
        target_datetime = datetime.fromisoformat("2023-01-03T22:00:00+09:00")

        # 22時
        self.assertTrue(is_time_overlap(entry_time, exit_time, target_datetime))

        # 23時
        target_datetime += timedelta(hours=1)
        self.assertTrue(is_time_overlap(entry_time, exit_time, target_datetime))

        # 0時
        target_datetime += timedelta(hours=1)
        self.assertTrue(is_time_overlap(entry_time, exit_time, target_datetime))

        # 1時
        target_datetime += timedelta(hours=1)
        self.assertFalse(is_time_overlap(entry_time, exit_time, target_datetime))

        # 2時
        target_datetime += timedelta(hours=1)
        self.assertFalse(is_time_overlap(entry_time, exit_time, target_datetime))

        # 3時
        target_datetime += timedelta(hours=1)
        self.assertFalse(is_time_overlap(entry_time, exit_time, target_datetime))


if __name__ == "__main__":
    unittest.main()
