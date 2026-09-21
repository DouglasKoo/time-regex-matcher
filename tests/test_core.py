"""Tests for the time regex matcher."""

import unittest

from time_regex_matcher import extract_times


class ExtractTimesTests(unittest.TestCase):
    """Tests for :func:`extract_times`."""

    def test_extracts_single_24_hour_time(self):
        self.assertEqual(extract_times("Meet at 14:30"), ["14:30"])

    def test_extracts_multiple_times(self):
        self.assertEqual(
            extract_times("Start at 9:00 and end at 17:45"), ["09:00", "17:45"]
        )

    def test_handles_hour_only_24_hour_time(self):
        self.assertEqual(extract_times("Arrive by 08:00"), ["08:00"])

    def test_extracts_12_hour_am_time(self):
        self.assertEqual(extract_times("Breakfast at 7:30am"), ["07:30"])

    def test_extracts_12_hour_pm_time_with_space(self):
        self.assertEqual(extract_times("Dinner at 7:30 PM"), ["19:30"])

    def test_extracts_hour_only_12_hour_time(self):
        self.assertEqual(extract_times("Lunch at 12 pm"), ["12:00"])

    def test_handles_midnight_special_case(self):
        self.assertEqual(extract_times("Open from 12 am to 12 pm"), ["00:00", "12:00"])

    def test_handles_noon_special_case(self):
        self.assertEqual(extract_times("Meeting at 12 pm"), ["12:00"])

    def test_handles_case_insensitive_am_pm(self):
        self.assertEqual(
            extract_times("At 3:05aM and 4:10Pm"), ["03:05", "16:10"]
        )

    def test_handles_am_pm_with_periods(self):
        self.assertEqual(
            extract_times("At 5:15 A.M. and 6:20 P.M."), ["05:15", "18:20"]
        )

    def test_ignores_invalid_times(self):
        self.assertEqual(extract_times("Not a time: 25:00 or 12:60"), [])

    def test_ignores_times_embedded_in_longer_numbers(self):
        self.assertEqual(extract_times("The number 123:456 is not a time"), [])

    def test_extracts_time_with_leading_zero_hour(self):
        self.assertEqual(extract_times("Wake at 07:05"), ["07:05"])

    def test_returns_empty_list_when_no_times(self):
        self.assertEqual(extract_times("No clock times here"), [])


if __name__ == "__main__":
    unittest.main()
