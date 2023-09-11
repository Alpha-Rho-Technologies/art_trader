# ART_Trader: Test and Trade with Your Own Strategy

__Note__: This repository is currently under development and is not ready for use. The code is being adapted from a closed-source library previously used by Alpha Rho Technologies and is now being refactored as an open-source library.

## Introduction
ART_Trader is an open-source library designed to allow developers to test and trade using their own trading strategies. This library makes it seamless to use the same strategy logic for both backtesting and live trading, ensuring consistent results.

## Features
- Backtesting: Test your trading strategy on historical data.
- Live Trading: Deploy your strategy for live trading.
- Uniform Logic: Use the same code for both testing and live deployment.
- Multiple Data Sources: Support for various data sources for trading data, currently limited to MetaTrader 5.
- Extensibility: Built to be easily extendable to include custom metrics, data sources, and trading logic.


To get a taste of how ART_Trader works, you can check out the example backtest [`sample_backtest.ipynb`](examples/sample_backtest.ipynb) and the example strategy [`previous_day_trend_strategy.py`](examples/strategies/previous_day_trend_strategy.py).
