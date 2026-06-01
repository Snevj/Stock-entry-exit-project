import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def backtest(signals, s1, s2, hedge_ratio, capital=10000):
    s1, s2 = s1.align(s2, join='inner')
    signals = signals.reindex(s1.index).fillna(0)

    position = signals["signal"]
    daily_spread = s1 - hedge_ratio * s2
    daily_pnl = position.shift(1) * daily_spread.diff()
    daily_pnl = daily_pnl.fillna(0)
    
    # Transaction costs
    transaction_cost = 0.001  # 0.1% per trade
    trades = position.diff().abs().fillna(0)
    cost = trades * transaction_cost * capital
    daily_pnl = daily_pnl - cost
    cumulative_pnl = daily_pnl.cumsum()
    equity_curve = capital + cumulative_pnl

    total_return = (equity_curve.iloc[-1] - capital) / capital * 100
    sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252) if daily_pnl.std() != 0 else 0

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

    ax1.plot(signals.index, signals["zscore"], label="Z-Score")
    ax1.axhline(1.5, color='red', linestyle='--', label='Sell (1.5)')
    ax1.axhline(-1.5, color='green', linestyle='--', label='Buy (-1.5)')
    ax1.axhline(0, color='gray', linestyle='-', alpha=0.3)
    ax1.set_title("Spread Z-Score")
    ax1.legend()

    ax2.plot(signals.index, signals["signal"], label="Signal", color='orange')
    ax2.set_title("Trading Signals (1=Buy, -1=Sell, 0=Hold)")
    ax2.legend()

    ax3.plot(equity_curve.index, equity_curve, label="Equity Curve", color='purple')
    ax3.axhline(capital, color='gray', linestyle='--', label='Starting Capital $10,000')
    ax3.set_title("Portfolio Value Over Time")
    ax3.legend()

    plt.tight_layout()
    plt.show()

    return total_return, sharpe