from datetime import datetime
import unittest
from unittest.mock import MagicMock

import numpy as np

from testing_wrapper import init_mt5, mt5

from art_testing import BacktestAccount
from mt5_common import MT5Symbol, MT5SymbolInfo
from mt5_trading import MT5Order, MT5Trader, MT5TradingStrategy


class MockOrder:
    def __init__(self, ticket, symbol, order_type, price_open, volume=None, volume_current=None):
        self.ticket = ticket
        self.symbol = symbol
        self.type = order_type
        self.price_open = price_open
        self.volume = volume
        self.volume_current = volume_current

class MockMT5Order(MT5Order):
    def __init__(self, ticket, symbol, order_type, price_open, volume=None, volume_current=None):
        o = MockOrder(ticket, symbol, order_type, price_open, volume, volume_current)
        super().__init__(o)

class MT5TraderTest(unittest.TestCase):

    a: BacktestAccount
    s: MT5TradingStrategy
    t: MT5Trader

    def setUp(self) -> None:

        self.a = BacktestAccount(balance=100_000, currency="EUR")
        self.s = MT5TradingStrategy(0.1, 1, 60, self.a)
        self.t = MT5Trader(self.s)

    def test_trade(self):
        symbol = MT5Symbol(ticker="EURUSD-Z", is_long=True)
        action = self.t.trade(symbol)

        # check that a dict is returned
        self.assertEqual(type(action), dict)

        expected_types = {
            "action": int,
            "symbol": str,
            "volume": float,
            "type": int,
            "price": float,
            "sl": float,
            "tp": float,
            "deviation": int,
            "magic": int,
            "comment": str,
            "type_time": int,
            "type_filling": int
        }

        # check that the right keys are present
        self.assertEqual(sorted(action.keys()), sorted(expected_types.keys()))

        # check that the value types are correct
        types_list = [type(value) for value in action.values()]
        expected_types_list = [value for value in expected_types.values()]
        self.assertEqual(types_list, expected_types_list)

        # check no empty strings or <=0 values
        for value in action.values():
            if type(value) is str:
                self.assertNotEqual(value, "")
            else:
                self.assertTrue(value > 0)

        # for static values, check they are as expected
        expected_values = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol.info.ticker,
            "deviation": 20,
            "magic": 234000,
            "comment": "ART script OPEN",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }
        for key, value in expected_values.items():
            self.assertEqual(value, action[key])

    def test_close(self):
        order = MockMT5Order(
            ticket=1234, 
            symbol='EURUSD-Z', 
            order_type=1, 
            price_open=1.2345, 
            volume=5.4321
        )
        action = self.t.close(order)

        # check that a dict is returned
        self.assertEqual(type(action), dict)

        expected_types = {
            "action": int,
            "position": int,
            "symbol": str,
            "volume": float,
            "type": int,
            "price": float,
            "deviation": int,
            "magic": int,
            "comment": str,
            "type_time": int,
            "type_filling": int
        }

        # check that the right keys are present
        self.assertEqual(sorted(action.keys()), sorted(expected_types.keys()))

        # check that the value types are correct
        types_list = [type(value) for value in action.values()]
        expected_types_list = [value for value in expected_types.values()]
        self.assertEqual(types_list, expected_types_list)

        # check no empty strings or <0 values
        for value in action.values():
            if type(value) is str:
                self.assertNotEqual(value, "")
            else:
                self.assertTrue(value >= 0)

        # for static values, check they are as expected
        expected_values = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": order.ticket,
            "symbol": order.symbol,
            "volume": order.volume,
            "deviation": 20,
            "magic": 234000,
            "comment": "ART script CLOSE",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        for key, value in expected_values.items():
            self.assertEqual(value, action[key])

    def test_cancel(self):
        order = MockMT5Order(
            ticket=1234, 
            symbol='EURUSD-Z', 
            order_type=1, 
            price_open=1.2345, 
            volume=5.4321
        )
        action = self.t.cancel(order)

        # check that a dict is returned
        self.assertEqual(type(action), dict)

        expected_types = {
            "order": int,
            "action": int,
            "symbol": str
        }

        # check that the right keys are present
        self.assertEqual(sorted(action.keys()), sorted(expected_types.keys()))

        # check that the value types are correct
        types_list = [type(value) for value in action.values()]
        expected_types_list = [value for value in expected_types.values()]
        self.assertEqual(types_list, expected_types_list)

        # check no empty strings or <=0 values
        for value in action.values():
            if type(value) is str:
                self.assertNotEqual(value, "")
            else:
                self.assertTrue(value > 0)

        # for static values, check they are as expected
        expected_values = {
            "order": order.ticket,
            "action": mt5.TRADE_ACTION_REMOVE,
            "symbol": order.symbol
        }
        for key, value in expected_values.items():
            self.assertEqual(value, action[key])

if __name__ == '__main__':
    init_mt5()
    unittest.main()
