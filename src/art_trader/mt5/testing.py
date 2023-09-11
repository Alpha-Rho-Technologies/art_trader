__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
__version__ = "0.0-SNAPSHOT"

from art_trader.mt5.common import MT5Symbol, MT5Utils

from art_trader.abstract.testing import Backtester


class MT5Backtester(Backtester):

    symbol_class = MT5Symbol
    brokerUtil = MT5Utils
