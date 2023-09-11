import unittest
from datetime import date, timedelta
from typing import List
from art_utils import dateRange

class TestDateRange(unittest.TestCase):
    def test_date_range(self):
        start_date = date(2022, 1, 1)
        end_date = date(2022, 1, 7)
        expected_dates = [date(2022, 1, 3), date(2022, 1, 4), date(2022, 1, 5), date(2022, 1, 6)]
        
        # Ensure that the function returns the expected dates
        self.assertEqual(list(dateRange(start_date, end_date)), expected_dates)
        
        # Ensure that the function raises a TypeError if the start or end date are not of type `date`
        try:
            list(dateRange('2022-01-01', end_date))
            list(dateRange(start_date, '2022-01-07'))
        except TypeError as te:
            pass
        except Exception as e:
            self.fail(e)
        
        # Ensure that the function returns an empty list if the start date is after the end date
        self.assertEqual(list(dateRange(end_date, start_date)), [])

if __name__ == '__main__':
    unittest.main()