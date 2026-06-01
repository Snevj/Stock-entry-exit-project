import sys
import os

from data.fetcher import fetch_stock
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yfinance as yf
from strategy.cointegration import find_pairs
from strategy.spread import get_spread
from strategy.signals import generate_signals
from strategy.backtest import backtest

print("=" * 50)
print("PAIRS TRADING STRATEGY — MSFT vs GOOGL")
print("=" * 50)

# Step 1 — Find cointegrated pairs
print("\n[1] Checking cointegration among tech stocks...")
tickers = ["MSFT", "GOOGL", "AAPL", "META", "AMZN"]
pairs = find_pairs(tickers, start="2019-01-01", end="2023-12-31")
if len(pairs) == 0:
    print("No cointegrated pairs found.")
else:
    print("Cointegrated pairs found:")
    print(pairs.to_string(index=False))

# Step 2 — Download MSFT and GOOGL
print("\n[2] Downloading MSFT and GOOGL data...")
s1 = fetch_stock("MSFT", start="2019-01-01", end="2023-12-31")
s2 = fetch_stock("GOOGL", start="2019-01-01", end="2023-12-31")
print(f"MSFT: {len(s1)} days, GOOGL: {len(s2)} days")

# Step 3 — Calculate spread
print("\n[3] Calculating spread...")
spread, hedge_ratio = get_spread(s1, s2)
print(f"Hedge ratio: {round(hedge_ratio, 4)}")

# Step 4 — Generate signals
print("\n[4] Generating trading signals...")
signals = generate_signals(spread)
buys = (signals["signal"] == 1).sum()
sells = (signals["signal"] == -1).sum()
print(f"Buy signals: {buys}, Sell signals: {sells}")

# Step 5 — Backtest
print("\n[5] Running backtest...")
total_return, sharpe = backtest(signals, s1, s2, hedge_ratio)
print(f"\nTotal Return: {round(total_return, 2)}%")
print(f"Sharpe Ratio: {round(sharpe, 2)}")
print("\nDone! Check the plots.")