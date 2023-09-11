import unittest
from datetime import date
from art_utils import isMarketDay

class TestIsMarketDay(unittest.TestCase):
    def test_market_day(self):
        market_day = date(2020, 1, 2)  # January 2nd, 2020
        self.assertTrue(isMarketDay(market_day))

    def test_weekend(self):
        weekend_day = date(2020, 1, 5)  # January 5th, 2020 (Saturday)
        self.assertFalse(isMarketDay(weekend_day))

    def test_new_years_day(self):
        new_years_day = date(2020, 1, 1)
        self.assertFalse(isMarketDay(new_years_day))

    def test_christmas_day(self):
        christmas_day = date(2020, 12, 25)
        self.assertFalse(isMarketDay(christmas_day))

if __name__ == '__main__':
    unittest.main()
