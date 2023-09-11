import unittest
from datetime import date

import art_utils as x


class ArtUtilsTest(unittest.TestCase):

    def test_isHit(self):
        pass

    def test_calcProfit(self):
        pass

    def test_isMarketDay(self):
        self.assertTrue(x.isMarketDay(date(2022, 12, 5))) # monday
        self.assertTrue(x.isMarketDay(date(2022, 12, 6))) # tuesday
        self.assertTrue(x.isMarketDay(date(2022, 12, 7))) # wednesday
        self.assertTrue(x.isMarketDay(date(2022, 12, 8))) # thursday
        self.assertTrue(x.isMarketDay(date(2022, 12, 9))) # friday

        self.assertFalse(x.isMarketDay(date(2022, 12, 10))) # saturday
        self.assertFalse(x.isMarketDay(date(2022, 12, 11))) # sunday

        self.assertFalse(x.isMarketDay(date(2022, 1, 1))) # new year's
        self.assertFalse(x.isMarketDay(date(2022, 12, 25))) # christmas
        

    def test_dateRange(self):
        days = [d for d in x.dateRange(date(2021, 1, 1), date(2022, 1, 1))]
        self.assertAlmostEqual(len(days), 5*52)
        for day in days:
            self.assertEqual(type(day), date)

        monday = date(2022, 12, 5)
        monday2 = date(2022, 12, 12)
        week = [d for d in x.dateRange(monday, monday2)]
        self.assertEqual(len(week), 5)

if __name__ == '__main__':
    unittest.main()