import unittest
import numpy as np
from art_utils import calcProfit

import unittest
import numpy as np

class TestCalcProfit(unittest.TestCase):
    def test_long_trade_profit(self):
        # setup
        trade = {'price': 100, 'tp': 120, 'sl': 80, 'volume': 1}
        data = np.array([[1, 100, 105, 95, 100],
                         [2, 101, 106, 96, 101],
                         [3, 102, 107, 97, 102],
                         [4, 103, 108, 98, 103],
                         [5, 104, 109, 99, 104],
                         [6, 105, 110, 100, 105],
                         [7, 106, 111, 101, 106],
                         [8, 107, 112, 102, 107],
                         [9, 108, 113, 103, 108],
                         [10, 109, 114, 104, 109]])
        # execute
        result = calcProfit(trade, data, True)
        # assert
        self.assertEqual(result, 9)

    def test_short_trade_profit(self):
        # setup
        trade = {'price': 100, 'tp': 80, 'sl': 120, 'volume': 1}
        data = np.array([[1, 100, 105, 95, 100],
                         [2, 101, 106, 96, 101],
                         [3, 102, 107, 97, 102],
                         [4, 103, 108, 98, 103],
                         [5, 104, 109, 99, 104],
                         [6, 105, 110, 100, 105],
                         [7, 106, 111, 101, 106],
                         [8, 107, 112, 102, 107],
                         [9, 108, 113, 103, 108],
                         [10, 109, 114, 104, 109]])
        # execute
        result = calcProfit(trade, data, False)
        # assert
        self.assertEqual(result, -9)

    def test_trade_at_tp(self):
        # setup
        trade = {'price': 100, 'tp': 120, 'sl': 80, 'volume': 1}
        data = np.array([[1, 100, 105, 95, 100],
                         [2, 101, 106, 96, 101],
                         [3, 102, 107, 97, 102],
                         [4, 103, 108, 98, 103],
                         [5, 104, 109, 99, 104],
                         [6, 105, 110, 100, 105],
                         [7, 106, 111, 101, 106],
                         [8, 107, 121, 105, 107],
                         [9, 108, 113, 103, 108],
                         [10, 119, 119, 119, 119]])
        # execute
        result = calcProfit(trade, data, True)
        # assert
        self.assertEqual(result, 20)

    def test_trade_at_sl(self):
        # setup
        trade = {'price': 100, 'tp': 120, 'sl': 80, 'volume': 1}
        data = np.array([[1, 100, 105, 95, 100],
                         [2, 101, 106, 96, 101],
                         [3, 102, 107, 103, 102],
                         [5, 104, 109, 99, 104],
                         [6, 105, 110, 100, 105],
                         [7, 106, 111, 79, 106],
                         [8, 107, 112, 102, 107],
                         [9, 108, 113, 103, 108],
                         [10, 109, 114, 104, 109]])
        # execute
        result = calcProfit(trade, data, True)
        # assert
        self.assertEqual(result, -20)

if __name__ == '__main__':
        unittest.main()
