__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

import logging
from zoneinfo import ZoneInfo

import MetaTrader5 as mt5
import numpy as np

from art_trader.abstract.common import Strategy, Symbol, SymbolInfo
from art_trader.abstract.utils import BrokerUtils, adjust_tz

log = logging.getLogger(__name__)

MT5_TZ = ZoneInfo("EET")


class MT5Utils(BrokerUtils):

    M10_TIMEFRAME = mt5.TIMEFRAME_M10
    HOURLY_TIMEFRAME = mt5.TIMEFRAME_H1
    DAILY_TIMEFRAME = mt5.TIMEFRAME_D1
    WEEKLY_TIMEFRAME = mt5.TIMEFRAME_W1
    MONTHLY_TIMEFRAME = mt5.TIMEFRAME_MN1

    def exists(symbol: Symbol) -> bool:
        if mt5.symbol_info(symbol.info.ticker) == None:
            return False
        return True

    def getRates(symbol: Symbol, timeframe, start, end) -> np.ndarray:
        _start = adjust_tz(start)
        _end = adjust_tz(end)
        rates = mt5.copy_rates_range(symbol.info.ticker, timeframe, _start, _end)
        return rates

    def formatRates(rates: np.ndarray) -> np.ndarray:
        if len(rates) == 0:
            return rates
        try:
            all = np.array([[x for x in item] for item in rates])
            out = np.delete(all, [5, 7], 1)  # delete colmuns 5 and 7
            return out
        except Exception as e:
            raise Exception(f"Error when formatting np.ndarray | {e}")


class MT5SymbolInfo(SymbolInfo):

    def __init__(self, ticker: str):

        # TODO change this because it makes it impossible to
        # create a mock class for unit testing purposes
        info = mt5.symbol_info(ticker)

        if info == None:
            raise Exception(f"Unable to find ticker={ticker}")

        self.ticker = info.name
        self.currency_profit = info.currency_profit
        self.volume_step = info.volume_step
        self.trade_contract_size = info.trade_contract_size
        self.volume_max = info.volume_max


class MT5Symbol(Symbol):

    def __init__(self, ticker: str) -> None:
        self.info = MT5SymbolInfo(ticker)

    @property
    def spread(self) -> float:
        return mt5.symbol_info(self.info.ticker).spread


class MT5Strategy(Strategy):

    broker_utils = MT5Utils
