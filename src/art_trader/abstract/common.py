__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

from abc import ABC, abstractmethod
from datetime import datetime


class SymbolInfo(ABC):
    """
    Represents static information about a financial asset (e.g., stock, currency pair, etc.)

    This class is meant to be extended to include non-variable attributes like name, currency denomination, etc.
    """

    ticker: str
    currency_profit: str
    trade_contract_size: int

    def __repr__(self) -> str:
        return str(self.__dict__)


class Symbol(ABC):
    """
    Represents variable information about a financial asset.

    This class is meant to be extended to include variable attributes like current price, historical prices,
    or any other dynamic information relevant to the asset.

    Attributes:
        info (SymbolInfo): An instance of SymbolInfo containing the asset's static information.
    """

    info: SymbolInfo

    def __repr__(self) -> str:
        return str(self.__dict__)


class Account(ABC):
    """
    Account is an abstract base class that represents a financial account.
    This class is meant to be extended to include relevant attributes and custom
    behavior for retrieving account data.

    Attributes:
        balance (float): An abstract property that must be implemented to return
                         the balance of the account.
        currency (str): An abstract property that must be implemented to return
                        the currency (eg: "USD") of the account.
    """

    @property
    @abstractmethod
    def balance(self) -> float:
        pass

    @property
    @abstractmethod
    def currency(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self.__dict__)


class Trade(ABC):
    """
    Represents a financial trade.

    Attributes:
        ticker (str): The ticker symbol for the asset being traded.
        is_long (bool): True if the trade is a long position, False if short.
        entry_price (float): The price at which the asset is bought or sold short.
        TP (float): The take profit price for the trade.
        SL (float): The stop loss price for the trade.
        volume (float): The volume or quantity of the asset being traded.
    """

    def __init__(self, ticker: str, is_long: bool, entry_price: float, TP: float, SL: float, volume: float):
        self.ticker = ticker
        self.is_long = is_long
        self.entry_price = entry_price
        self.TP = TP
        self.SL = SL
        self.volume = volume

    
    def as_dict(self) -> dict:
        return {
            'ticker': self.ticker,
            'is_long': self.is_long,
            'entry_price': self.entry_price,
            'TP': self.TP,
            'SL': self.SL,
            'volume': self.volume
        }
    
    def __repr__(self) -> str:
        return str(self.as_dict())



class Strategy(ABC):

    @abstractmethod
    def strat(self, symbol: Symbol, day: datetime) -> Trade:
        """
        Abstract method for implementing a trading strategy. Must be overridden by subclasses.

        Parameters:
        - symbol (Symbol): The financial symbol or instrument to trade.
        - day (datetime): The date for which the trading strategy is being applied.

        Returns:
        Trade: An object containing trade data.
        """
        pass

    def __repr__(self) -> str:
        return str(self.__dict__)


class BaseTrader(ABC):
    """
    BaseTrader is an abstract base class that serves as a common interface for
    trading and backtesting modules. It standardizes the way trades are generated.

    Attributes:
        strategy (Strategy): The trading strategy that this trader will be using.
    """

    strategy: Strategy

    def trade(self, symbol: Symbol, day: datetime) -> dict:
        return self.strategy.strat(symbol, day).as_dict()

