__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

from abc import abstractmethod
import logging
from datetime import date, datetime
from typing import Tuple
import numpy as np
from pandas import DataFrame

from art_trader.abstract.common import Account, BaseTrader, Strategy, Symbol
from art_trader.abstract.utils import OPEN, CLOSE, HIGH, LOW, SPREAD, TIME, BrokerUtils, dateRange, getPrevMarketDay, toDT

log = logging.getLogger(__name__)


class BacktestAccount(Account):

    def __init__(self, initial_balance: float, currency: str) -> None:
        self._balance = initial_balance
        self._currency = currency

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, currency: str) -> None:
        self._currency = currency


class Backtester(BaseTrader):

    symbol_class = Symbol
    brokerUtil = BrokerUtils

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __init__(self, strategy: Strategy, tickers: list[str], start: date, end: date, account: BacktestAccount) -> None:
        self.strategy = strategy
        self.start = start
        self.end = end
        self.symbols = [self.symbol_class(x) for x in tickers]
        self.account = account

    def run_all_single_thread(self) -> DataFrame:
        """
        Runs the entire backtest and returns a DataFrame containing daily profit and balance.
        """
        dates = [x for x in dateRange(self.start, self.end)]
        results = []

        initial_date = toDT(getPrevMarketDay(self.start)).timestamp()
        initial_balance = self.account.balance
        results.append({"date": initial_date, "profit": 0, "balance": initial_balance})

        for date in dates:
            day_profit = 0
            for symbol in self.symbols:
                symbol_profit = self.simulate(symbol, date)
                day_profit += symbol_profit

            self.account.balance += day_profit

            results.append({"date": toDT(date).timestamp(), 
                            "profit": day_profit, 
                            "balance": self.account.balance})

        df = DataFrame(results, columns=["date", "profit", "balance"])
        df["date"] = df.date.apply(lambda x: date.fromtimestamp(x))
        return df.set_index("date")

    def simulate(self, symbol: Symbol, day: date) -> Tuple[float, bool]:
        """
        Simulates a trade and returns the profit
        """
        try:
            trade = self.trade(symbol, day)
            price_action = self.getPriceAction(symbol, day)
            return self.calcProfit(trade, price_action, symbol)
        except Exception as e:
            log.warn(
                f"failed to simulate {symbol.info.ticker} for {day} | {e}")
            return 0

    def trade(self, symbol: Symbol, day: datetime) -> dict:
        trade = super().trade(symbol, day)
        trade["day"] = day
        return trade

    def calcProfit(self, trade: dict, data: np.ndarray, symbol: Symbol) -> float:
        """
        Calculates the net profit for a trade given price data and other trade parameters.

        Always closes the trade if still open at end of parsing data.
        """

        def xr(hour):
            return self.brokerUtil.xr(symbol.info.currency_profit, self.account.currency, hour)

        executed = False
        exit_price = None

        multiplier = 1 if trade["is_long"] else -1

        for row in data:
            if not executed:
                if row[LOW] < trade["entry_price"] < row[HIGH]:
                    executed = True
                    entry_xr = xr(row[TIME])

            if executed:
                sl_hit = row[LOW] < trade["SL"] < row[HIGH]
                tp_hit = row[LOW] < trade["TP"] < row[HIGH]
                if tp_hit or sl_hit:
                    exit_xr = xr(row[TIME])
                    exit_price = trade["TP"] if tp_hit else trade["SL"]
                    break

        if not executed:
            return 0.

        if exit_price is None:
            exit_price = data[-1][CLOSE]
            exit_xr = xr(row[TIME])

        avg_xr = (entry_xr + exit_xr) / 2
        net = (exit_price - trade["entry_price"]) * trade["volume"] * \
            multiplier * symbol.info.trade_contract_size * avg_xr
        tx_fee = self.calc_tx_fee(trade["volume"])

        return net - tx_fee
    
    def getPriceAction(self, symbol: Symbol, day: datetime) -> np.ndarray:
        """
        Get the price data for trade backtesting on a specific day.

        This method retrieves the price data for the specified symbol and date,
        covering a 24-hour period from midnight to midnight on the given day.
        
        Args:
            symbol (Symbol): The symbol or instrument for which to fetch price data.
            day (datetime): The date for which to retrieve price data.

        Returns:
            np.ndarray: An array of price data for the specified symbol and date.

        Notes:
            Override this method if you require price data for a period longer than 24 hours.

        """
        return self.brokerUtil.getPriceAction(symbol, day)


    def calc_tx_fee(self, volume: float) -> float:
        """
        Calculate the transaction fee for a given trade volume.

        This method calculates the transaction fee for a trade with the specified volume.
        By default, it returns a transaction fee of 0, but can be overriden to implement
        a custom transaction fee structure.

        Args:
            volume (float): The volume of the trade for which to calculate the fee.

        Returns:
            float: The transaction fee for the trade.
        """
        return 0
