__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

import logging
from abc import ABC, abstractmethod
from datetime import datetime

from art_trader.abstract.common import BaseTrader, Symbol
from art_trader.abstract.common import Symbol

log = logging.getLogger(__name__)


class Order(ABC):
    """
    Order is an abstract base class that represents a generic financial order.
    This class is meant to be extended to include relevant attributes and custom
    behavior for different types of orders.
    """

    def __repr__(self) -> str:
        return str(self.__dict__)


class Trader(BaseTrader):

    def __repr__(self) -> str:
        return str(self.__dict__)

    ##############################
    # Trade generation functions #

    def trade(self, symbol: Symbol, day: datetime) -> dict:
        return super().trade(symbol, day)

    @abstractmethod
    def close(self, order: Order) -> dict:
        """
        Returns an order to close a trade
        """
        pass

    @abstractmethod
    def cancel(self, order: Order) -> dict:
        """
        Returns an order to cancel a trade
        """
        pass

    ##############################
    # Trade monitoring functions #

    @abstractmethod
    def get_open_orders(self, symbol: Symbol) -> list[Order]:
        pass

    @abstractmethod
    def get_pending_orders(self, symbol: Symbol) -> list[Order]:
        pass

    @abstractmethod
    def get_closed_orders(self, symbol: Symbol, start: datetime, end: datetime) -> list[Order]:
        pass

    #############################
    # Trade execution functions #

    @abstractmethod
    def send(self, order: dict) -> bool:
        """
        Sends a given order to the broker, returns False if the order fails
        """
        pass
