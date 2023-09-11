__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

import logging
from datetime import datetime

from abstract.common import Account
from abstract.trading import Order, Trader

from .common import MT5Symbol, MT5Utils, mt5

log = logging.getLogger(__name__)


class MT5Account(Account):
    """
    MT5Account is a concrete class extending the Account abstract base class.
    It provides a specific implementation for MetaTrader 5 accounts.

    Attributes:
        balance (float): Returns the equity of the MetaTrader 5 account.
        currency (str): Returns the currency of the MetaTrader 5 account (eg: "USD").
    """

    @property
    def balance(self) -> float:
        """Returns the equity of the MetaTrader 5 account."""
        return mt5.account_info().equity

    @property
    def currency(self) -> str:
        """Returns the currency of the MetaTrader 5 account."""
        return mt5.account_info().currency


class MT5Order(Order):
    """
    MT5Order is a concrete class extending the Order abstract base class.
    It provides a specific implementation for MetaTrader 5 orders.

    Attributes:
        symbol (str): The trading symbol for the order.
        ticket (int): The unique identifier for the order.
        type (str): The type of the order (e.g., "BUY", "SELL").
        volume (float): The volume of the order.
        price (float): The price at which the order is executed.
    """

    def __init__(self, o) -> None:
        """
        Initializes an MT5Order instance with order details.

        Args:
            o: An object containing the order details.
        """
        self.ticket = o.ticket
        self.symbol = o.symbol
        self.type = o.type
        self.price = o.price_open
        try:
            self.volume = o.volume
        except AttributeError as ae:
            self.volume = o.volume_current


class MT5Trader(Trader):
    """
    Subclass of Trader designed for interfacing with the MT5 trading platform.
    """

    symbol_class = MT5Symbol
    brokerUtil = MT5Utils

    #############################
    # Trade execution functions #

    def send(self, order: dict) -> bool:
        """
        Sends an order to the MT5 trading platform.

        Args:
            order (dict): The order parameters in dictionary form.

        Returns:
            bool: True if the order was successfully sent, False otherwise.
        """
        result = mt5.order_send(order)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            log.info(
                f"order_send successful for {result.request.symbol}")
            log.debug(result._asdict())
            return True
        else:
            log.error(
                f"order_send failed for {result.request.symbol}: {result.comment}")
            log.debug(result._asdict())
            return False

    ##############################
    # Trade generation functions #

    def trade(self, symbol: MT5Symbol, day: None = None) -> dict:
        """
        Generates a trade for the given symbol.

        Args:
            symbol (MT5Symbol): The trading symbol.
            day (None, optional): Should always be None for live trading.

        Returns:
            dict: The trade order in dictionary form.
        """
        if day is not None:
            raise ValueError(
                "Parameter 'day' should not be initialised for live trading.")

        trade = super().trade(symbol, day=None)

        if trade["is_long"]:
            if trade["entry_price"] > mt5.symbol_info_tick(symbol.info.ticker).ask:
                order_type = mt5.ORDER_TYPE_BUY_STOP
            else:
                order_type = mt5.ORDER_TYPE_BUY_LIMIT
        else:
            if trade["entry_price"] > mt5.symbol_info_tick(symbol.info.ticker).bid:
                order_type = mt5.ORDER_TYPE_SELL_LIMIT
            else:
                order_type = mt5.ORDER_TYPE_SELL_STOP

        return {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": trade["ticker"],
            "volume": trade["volume"],
            "type": order_type,
            "price": trade["entry_price"],
            "sl": trade["SL"],
            "tp": trade["TP"],
            "deviation": 20,
            "magic": 234000,
            "comment": "ART script OPEN",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }

    def close(self, order: MT5Order) -> dict:
        """
        Generates a closing order for an existing open position.

        Args:
            order (MT5Order): The existing open position.

        Returns:
            dict: The closing order in dictionary form.
        """
        order_type = mt5.ORDER_TYPE_BUY if order.type == 1 else mt5.ORDER_TYPE_SELL

        price = mt5.symbol_info_tick(
            order.symbol).ask if order.type == 1 else mt5.symbol_info_tick(order.symbol).bid

        return {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": order.ticket,
            "symbol": order.symbol,
            "volume": order.volume,
            "type": order_type,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "ART script CLOSE",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

    def cancel(self, order: MT5Order) -> dict:
        """
        Cancels an existing order.

        Args:
            order (MT5Order): The existing open position.

        Returns:
            dict: The cancellation order in dictionary form.
        """
        return {
            "order": order.ticket,
            "action": mt5.TRADE_ACTION_REMOVE,
            "symbol": order.symbol
        }

    ##############################
    # Trade monitoring functions #

    def get_open_orders(self, symbol: MT5Symbol) -> list[Order]:
        """
        Retrieves a list of open orders for a given symbol.

        Args:
            symbol (MT5Symbol): The trading symbol.

        Returns:
            list[Order]: A list of open orders.
        """
        open_orders = mt5.positions_get(symbol=symbol.info.ticker)
        if open_orders:
            return [MT5Order(x) for x in open_orders]
        else:
            return []

    def get_pending_orders(self, symbol: MT5Symbol) -> list[Order]:
        """
        Retrieves a list of pending orders for a given symbol.

        Args:
            symbol (MT5Symbol): The trading symbol.

        Returns:
            list[Order]: A list of pending orders.
        """
        pending_orders = mt5.orders_get(symbol=symbol.info.ticker)
        if pending_orders:
            return [MT5Order(x) for x in pending_orders]
        else:
            return []

    def get_closed_orders(self, symbol: MT5Symbol, start: datetime, end: datetime) -> list[Order]:
        """
        Retrieves a list of closed orders for a given symbol within a specific time range.

        Args:
            symbol (MT5Symbol): The trading symbol.
            start (datetime): The start date and time for the query.
            end (datetime): The end date and time for the query.

        Returns:
            list[Order]: A list of closed orders.
        """
        closed_orders = mt5.history_orders_get(
            start, end, group=symbol.info.ticker)
        if closed_orders:
            return [MT5Order(x) for x in closed_orders]
        else:
            return []
