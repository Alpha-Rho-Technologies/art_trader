__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

import logging
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from random import getrandbits
from zoneinfo import ZoneInfo

import numpy as np
from pandas import DataFrame

from art_trader.abstract.common import Symbol

log = logging.getLogger(__name__)

MIDNIGHT: time = time(0, 0, 0)

# PRICE DATA INDICES
TIME = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
SPREAD = 5


def toDT(day) -> datetime:
    """
    Converts various types to a datetime object.

    Args:
        day (datetime, date, int, float, np.float64): The input date or timestamp.

    Returns:
        datetime: A datetime object converted from the input.

    Raises:
        TypeError: If an unsupported object type is passed.
    """
    if type(day) == datetime:
        return day
    elif type(day) == date:
        return datetime.combine(day, MIDNIGHT)
    elif type(day) in [int, float, np.float64]:
        return datetime.fromtimestamp(day)
    else:
        raise TypeError(f"Unsupported object of type {type(day)} was passed.")


def adjust_tz(day) -> datetime:
    """
    Converts a date to a datetime object adjusted for the UTC timezone.

    Args:
        day (datetime, date, int, float, np.float64): The input date or timestamp.

    Returns:
        datetime: A datetime object with UTC timezone information.

    Raises:
        TypeError: If an unsupported object type is passed.
    """
    return toDT(day).replace(tzinfo=ZoneInfo("UTC"))


def isMarketDay(day: date) -> bool:
    """
    Checks if a given date is a market trading day.

    Args:
        day (date): The date to check.

    Returns:
        bool: True if it's a market trading day, False otherwise.

    Raises:
        TypeError: If a non-date object is passed.
    """
    if type(day) != date:
        raise TypeError("Input must be a date object.")
    if day.weekday() < 5:
        if not ((day.month == 1 and day.day == 1) or (day.month == 12 and day.day == 25)):
            return True
    return False


def dateRange(start_date: date, end_date: date):
    """
    Generates a range of weekdays between two given dates.

    Args:
        start_date (date): The start date.
        end_date (date): The end date.

    Yields:
        datetime: A datetime object representing each weekday within the date range.

    Raises:
        TypeError: If non-date objects are passed as arguments.
    """
    if type(start_date) != date or type(end_date) != date:
        raise TypeError("Both start_date and end_date must be date objects.")
    for n in range(int((end_date - start_date).days)):
        day: datetime = start_date + timedelta(n)
        if isMarketDay(day):
            yield day


def getPrevMarketDay(day: date) -> date:
    """
    Returns the previous market trading date for a given date.

    Args:
        day (date): The input date.

    Returns:
        date: The previous market trading date.

    Raises:
        TypeError: If a non-date object is passed.
    """
    if type(day) != date:
        raise TypeError("Input must be a date object.")
    out = day - timedelta(days=1)
    while not isMarketDay(out):
        out = out - timedelta(days=1)
    return out


class BrokerUtils(ABC):

    M10_TIMEFRAME: int
    HOURLY_TIMEFRAME: int
    DAILY_TIMEFRAME: int
    WEEKLY_TIMEFRAME: int
    MONTHLY_TIMEFRAME: int

    @abstractmethod
    def exists(symbol: Symbol) -> bool:
        """
        Checks whether a symbol exists.

        Args:
            symbol (Symbol): The symbol object to check for existence.

        Returns:
            bool: True if the symbol exists, False otherwise.
        """
        pass

    @abstractmethod
    def getRates(symbol: Symbol, timeframe: int, start: datetime, end: datetime) -> np.ndarray:
        """
        Returns an unformatted numpy.ndarray of the raw data for a specific symbol and timeframe.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            timeframe (int): The timeframe for data (e.g., M10, HOURLY, DAILY, etc.).
            start (datetime): The start date and time for data retrieval.
            end (datetime): The end date and time for data retrieval.

        Returns:
            np.ndarray: An array containing raw data for the specified parameters.
        """
        pass

    @abstractmethod
    def formatRates(array: np.ndarray) -> np.ndarray:
        """
        Abstract method to format raw price data.

        Args:
            array (np.ndarray): An unformatted numpy.ndarray of rate data.

        Returns:
            np.ndarray: Formatted rate data.
        """
        pass

    @classmethod
    def xr(cls, from_currency: str, to_currency: str, dt: datetime) -> float:
        """
        Get the exchange rate for the given pair of currencies at a given time.

        Args:
            from_currency (str): The currency to convert from.
            to_currency (str): The currency to convert to.
            dt (datetime): The datetime for which the rate is needed.

        Returns:
            float: Exchange rate between from_currency and to_currency at the specified datetime.
        """
        if from_currency == to_currency:
            return 1.
        
        dt = adjust_tz(dt)

        try:
            ticker = from_currency+to_currency+"-Z"
            if not c.exists(ticker):
                ticker = to_currency+from_currency+"-Z"
                if not c.exists(ticker):
                    raise Exception()
                return 1 / c.getHourlyData(ticker, dt, dt+timedelta(hours=1))[0][CLOSE]
            return c.getHourlyData(ticker, dt, dt+timedelta(hours=1))[0][CLOSE]
        except Exception as e:
            raise Exception(f"No exchange rate found for {from_currency}/{to_currency} | {e}")

    @classmethod
    def getData(cls, symbol: Symbol, timeframe: int, start: datetime, end: datetime) -> np.ndarray:
        """
        Get formatted data for a specific symbol, timeframe, and date range.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            timeframe (int): The timeframe for data (e.g., M10, HOURLY, DAILY, etc.).
            start (datetime): The start date and time for data retrieval.
            end (datetime): The end date and time for data retrieval.

        Returns:
            np.ndarray: Formatted rate data for the specified parameters.
        """
        out = cls.formatRates(cls.getRates(symbol, timeframe, start, end))
        return out

    @classmethod
    def getMonthlyData(cls, symbol: Symbol, start: date, end: date) -> np.ndarray:
        """
        Get formatted monthly data for a specific symbol and date range.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            start (date): The start date for data retrieval.
            end (date): The end date for data retrieval.

        Returns:
            np.ndarray: Formatted monthly rate data for the specified parameters.
        """
        return cls.getData(symbol, cls.MONTHLY_TIMEFRAME, start, end)

    @classmethod
    def getDailyData(cls, symbol: Symbol, start: date, end: date) -> np.ndarray:
        """
        Get formatted daily data for a specific symbol and date range.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            start (date): The start date for data retrieval.
            end (date): The end date for data retrieval.

        Returns:
            np.ndarray: Formatted daily rate data for the specified parameters.
        """
        return cls.getData(symbol, cls.DAILY_TIMEFRAME, start, end)

    @classmethod
    def getWeeklyData(cls, symbol: Symbol, start: date, end: date) -> np.ndarray:
        """
        Get formatted weekly data for a specific symbol and date range.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            start (date): The start date for data retrieval.
            end (date): The end date for data retrieval.

        Returns:
            np.ndarray: Formatted weekly rate data for the specified parameters.
        """
        return cls.getData(symbol, cls.WEEKLY_TIMEFRAME, start, end)

    @classmethod
    def getHourlyData(cls, symbol: Symbol, start: datetime, end: datetime) -> np.ndarray:
        """
        Get formatted hourly data for a specific symbol and date range.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            start (datetime): The start date and time for data retrieval.
            end (datetime): The end date and time for data retrieval.

        Returns:
            np.ndarray: Formatted hourly rate data for the specified parameters.
        """
        return cls.getData(symbol, cls.HOURLY_TIMEFRAME, start, end)

    @classmethod
    def getM10Data(cls, symbol: Symbol, start: datetime, end: datetime) -> np.ndarray:
        """
        Get formatted M10 (10-minute) data for a specific symbol and date range.

        Args:
            symbol (Symbol): The symbol object for which to fetch data.
            start (datetime): The start date and time for data retrieval.
            end (datetime): The end date and time for data retrieval.

        Returns:
            np.ndarray: Formatted M10 rate data for the specified parameters.
        """
        return cls.getData(symbol, cls.M10_TIMEFRAME, start, end)

    @classmethod
    def getPriceAction(cls, symbol: Symbol, day: date) -> np.ndarray:
        """
        Get formatted hourly price action data for a specific symbol and date.

        This method retrieves hourly price action data for the specified symbol and date,
        covering a 24-hour period from midnight to midnight on the given day.

        Args:
            symbol (Symbol): The symbol object for which to fetch price action data.
            day (date): The date for which to retrieve price action data.

        Returns:
            np.ndarray: Formatted hourly price action data as an array for the specified symbol and date.

        Raises:
            Exception: If the output contains too many rows (more than 24).
            Exception: If no price action data is found for the symbol on the specified day.
        """
        _start = datetime.combine(day, time())
        _end = _start + timedelta(hours=23)
        out = cls.getHourlyData(symbol, _start, _end)
        if len(out) > 24:
            raise Exception("output contains too many rows")
        if len(out) == 0:
            raise Exception(
                f"No price action found for {symbol.symbol} on {day}")
        return out
