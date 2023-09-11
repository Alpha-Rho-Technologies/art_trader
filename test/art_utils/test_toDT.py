
import unittest
from datetime import date, datetime

import numpy as np
from pytz import utc
from art_utils import toDT


class TestToDT(unittest.TestCase):
    def test_toDT_datetime(self):
        # test input of type datetime
        dt = datetime.now()
        self.assertEqual(toDT(dt), dt)
        self.assertIsInstance(toDT(dt), datetime)

    def test_toDT_date(self):
        # test input of type date
        d = date.today()
        year, month, day = d.year, d.month, d.day
        expected_output = datetime(year, month, day, 0, 0, 0)
        self.assertEqual(toDT(d), expected_output)
        self.assertIsInstance(toDT(d), datetime)

    def test_toDT_int(self):
        # test input of type int
        i = 1234567890
        expected_output = datetime(2009, 2, 13, 23, 31, 30)
        self.assertEqual(toDT(i), expected_output)
        self.assertIsInstance(toDT(i), datetime)

    def test_toDT_float(self):
        # test input of type float
        f = 1234567890.123456
        expected_output = datetime(2009, 2, 13, 23, 31, 30, 123456)
        self.assertEqual(toDT(f), expected_output)
        self.assertIsInstance(toDT(f), datetime)

    def test_toDT_npfloat(self):
        # test input of type np.float64
        nf = np.float64(1234567890.123456)
        expected_output = datetime(2009, 2, 13, 23, 31, 30, 123456)
        self.assertEqual(toDT(nf), expected_output)
        self.assertIsInstance(toDT(nf), datetime)

    def test_toDT_invalid(self):
        # test input of invalid type
        invalid_inputs = [None, "string", [1, 2, 3]]
        for i in invalid_inputs:
            self.assertRaises(TypeError, toDT, i)

    def test_timezone_preserved(self):
        dt = datetime.now(tz=utc)
        result = toDT(dt)
        self.assertEqual(result.tzinfo, dt.tzinfo)


if __name__ == '__main__':
    unittest.main()