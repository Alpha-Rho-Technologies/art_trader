import unittest
from datetime import date, datetime, timedelta
import numpy as np

from art_utils import BrokerUtils, dateRange
from mt5_common import MT5_TZ, MT5Utils as x
from testing_wrapper import init_mt5, mt5

TICKER = "EURUSD-Z"

class BrokerUtilsTest(unittest.TestCase):

    def test_getDF(self):
        start = datetime(2022, 11, 2)
        end = datetime(2022, 11, 3)
        df = x.getDF(TICKER, mt5.TIMEFRAME_D1, start, end)
        self.assertFalse(len(df)==0, "df was empty")

    def test_formatDF(self):
        start = datetime(2022, 11, 2)
        end = datetime(2022, 11, 3)
        df = x.getDF(TICKER, mt5.TIMEFRAME_D1, start, end)
        if len(df)==0:
            raise Exception("Dataframe not meant to be empty")
        df = x.formatDF(df)
        if len(df.columns) != 5:
            self.fail(f"Wrong number of columns: {len(df.columns)}")
        else:
            if not df.columns.values.tolist() == ["time", "open", "high", "low", "close"]:
                self.fail(f"Wrong column names: {df.columns.values.tolist()}")

    def test_xr(self):
        day = date(2022, 11, 2)
        self.assertEqual(x.xr("EUR", "EUR", day), 1.)
        self.assertEqual(type(x.xr("USD", "EUR", day)), np.float64)
        self.assertTrue(x.xr("GBP", "USD", day) > 0)

    def test_getMonthlyData(self):
        start = date(2022, 9, 1)
        end = date(2022, 11, 1)
        df = x.getMonthlyData(TICKER, start, end) 
        if len(df)==0:
            raise Exception("Dataframe not meant to be empty")
        self.assertEqual(date.fromtimestamp(df[0][0]), start.replace(day=1))
        self.assertEqual(date.fromtimestamp(df[-1][0]), end.replace(day=1))

    def test_getDailyData(self):
        start = date(2022, 11, 2)
        end = date(2022, 11, 4)
        df = x.getDailyData(TICKER, start, end) 
        if len(df)==0:
            raise Exception("Dataframe not meant to be empty")
        self.assertEqual(date.fromtimestamp(df[0][0]), start)
        self.assertEqual(date.fromtimestamp(df[-1][0]), end)

    def test_getHourlyData(self):
        start = datetime(2022, 11, 2, 2, 0)
        end = datetime(2022, 11, 3, 8, 0)
        df = x.getHourlyData(TICKER, start, end)
        if len(df)==0:
            raise Exception("Dataframe not meant to be empty")
        self.assertEqual(date.fromtimestamp(df[0][0]), start.date())
        self.assertEqual(date.fromtimestamp(df[-1][0]), end.date())
        self.assertEqual(len(df)-1, (end-start).total_seconds()/3600)

    def test_getClose(self):
        day = datetime.now(tz=MT5_TZ).date()-timedelta(days=1)
        price = x.getClose(TICKER, day)
        self.assertEqual(type(price), np.float64)
        self.assertTrue(price > 0)
        self.assertEqual(price, mt5.symbol_info(TICKER).session_close)

    def test_getPriceAction(self):
        day = date(2022, 11, 2)
        df = x.getPriceAction(TICKER, day)
        if len(df)==0:
            raise Exception("Dataframe not meant to be empty")
        self.assertEqual(date.fromtimestamp(df[0][0]), day)
        self.assertEqual(date.fromtimestamp(df[-1][0])  , day)

        for day in dateRange(date(2020, 1, 1), date(2021, 1, 1)):
            try:
                df = x.getPriceAction(TICKER, day)
                self.assertEqual(len(df), 24)
            except AssertionError as ae:
                print(f"price action for {day} has wrong length | {ae}")
            except Exception as e:
                self.fail(f"{day} | {e}")


init_mt5()
if __name__ == '__main__':
    unittest.main()