import unittest
from datetime import date, timedelta
from art_utils import getPrevMarketDay

class TestGetPrevMarketDay(unittest.TestCase):
    def test_get_prev_market_day(self):
        day = date(2022, 12, 18)
        expected_prev_market_day = date(2022, 12, 16)
        
        # Ensure that the function returns the expected previous market day
        self.assertEqual(getPrevMarketDay(day), expected_prev_market_day)
        
        # Ensure that the function raises a TypeError if the input is not of type `date`
        self.assertRaises(TypeError, getPrevMarketDay, '2022-01-06')
        self.assertRaises(TypeError, getPrevMarketDay, 123)
        

if __name__ == '__main__':
    unittest.main()
