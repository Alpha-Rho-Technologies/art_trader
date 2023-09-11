from datetime import datetime

from art_trader.abstract.common import Symbol, Trade
from art_trader.abstract.trading import Trader
from art_trader.abstract.utils import CLOSE, OPEN, getPrevMarketDay
from art_trader.mt5.common import MT5Strategy


class PreviousDayTrendStrategy(MT5Strategy):
    """
    Implements a basic trading strategy based on the price movement of an asset on the previous day.
    """

    def strat(self, symbol: Symbol, day: datetime) -> Trader:
        """
        Implement the trading strategy logic to determine whether to go long or short on an asset.

        The decision is based on the price movement of the asset on the previous trading day.
        If the asset's price increased on the previous day, a long position is opened.
        If the asset's price decreased on the previous day, a short position is opened.

        Parameters:
        - symbol (Symbol): The financial symbol or instrument to trade.
        - day (datetime): The date for which the trading strategy is being applied.

        Returns:
        Trade: An object containing trade data.
        """
        prev_day = getPrevMarketDay(day)

        data = self.broker_utils.getDailyData(symbol, prev_day, prev_day)

        open_price = data[0, OPEN]
        close_price = data[0, CLOSE]

        is_long = close_price > open_price

        trade = Trade(
            ticker=symbol.info.ticker,
            is_long=is_long,
            entry_price=close_price,
            TP=close_price * 1.02 if is_long else close_price * 0.98,
            SL=close_price * 0.98 if is_long else close_price * 1.02,
            volume=1
        )

        return trade
