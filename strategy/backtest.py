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

def backtest_api(signals, s1, s2, hedge_ratio, capital=10000):
    s1, s2 = s1.align(s2, join='inner')
    signals = signals.reindex(s1.index).fillna(0)

    position = signals["signal"]
    daily_spread = s1 - hedge_ratio * s2
    daily_pnl = position.shift(1) * daily_spread.diff()
    daily_pnl = daily_pnl.fillna(0)

    transaction_cost = 0.001
    trades = position.diff().abs().fillna(0)
    cost = trades * transaction_cost * capital
    daily_pnl = daily_pnl - cost

    cumulative_pnl = daily_pnl.cumsum()
    equity_curve = capital + cumulative_pnl

    total_return = (equity_curve.iloc[-1] - capital) / capital * 100
    sharpe = (daily_pnl.mean() / daily_pnl.std()) * (252**0.5) if daily_pnl.std() != 0 else 0

    return {
        "total_return": round(float(total_return), 2),
        "sharpe_ratio": round(float(sharpe), 2),
        "hedge_ratio": round(float(hedge_ratio), 4),
        "buy_signals": int((signals["signal"] == 1).sum()),
        "sell_signals": int((signals["signal"] == -1).sum()),
        "dates": [str(d) for d in equity_curve.index],
        "equity_curve": [round(float(v), 2) for v in equity_curve.values],
        "zscore": [round(float(v), 4) for v in signals["zscore"].values],
        "signals": [int(v) for v in signals["signal"].values]
    }

def calculate_metrics(daily_pnl, equity_curve, capital=10000):
    import numpy as np

    # Total return
    total_return = (equity_curve.iloc[-1] - capital) / capital * 100

    # Sharpe ratio
    sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252)

    # Max drawdown — biggest peak to trough loss
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max * 100
    max_drawdown = drawdown.min()

    # Win rate — % of trades that were profitable
    winning_days = (daily_pnl > 0).sum()
    total_days = (daily_pnl != 0).sum()
    win_rate = (winning_days / total_days * 100) if total_days > 0 else 0

    # Average win vs average loss
    avg_win = daily_pnl[daily_pnl > 0].mean()
    avg_loss = daily_pnl[daily_pnl < 0].mean()

    # Profit factor
    gross_profit = daily_pnl[daily_pnl > 0].sum()
    gross_loss = abs(daily_pnl[daily_pnl < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0

    # Calmar ratio — return / max drawdown
    calmar = total_return / abs(max_drawdown) if max_drawdown != 0 else 0

    return {
        "total_return": round(float(total_return), 2),
        "sharpe_ratio": round(float(sharpe), 2),
        "max_drawdown": round(float(max_drawdown), 2),
        "win_rate": round(float(win_rate), 2),
        "avg_win": round(float(avg_win), 4),
        "avg_loss": round(float(avg_loss), 4),
        "profit_factor": round(float(profit_factor), 2),
        "calmar_ratio": round(float(calmar), 2)
    }

def backtest_api(signals, s1, s2, hedge_ratio, capital=10000):
    import numpy as np

    s1, s2 = s1.align(s2, join='inner')
    signals = signals.reindex(s1.index).fillna(0)

    position = signals["signal"]
    daily_spread = s1 - hedge_ratio * s2
    daily_pnl = position.shift(1) * daily_spread.diff()
    daily_pnl = daily_pnl.fillna(0)

    transaction_cost = 0.001
    trades = position.diff().abs().fillna(0)
    cost = trades * transaction_cost * capital
    daily_pnl = daily_pnl - cost

    cumulative_pnl = daily_pnl.cumsum()
    equity_curve = capital + cumulative_pnl

    # Core metrics
    total_return = (equity_curve.iloc[-1] - capital) / capital * 100
    sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252) if daily_pnl.std() != 0 else 0

    # Max drawdown
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max * 100
    max_drawdown = drawdown.min()

    # Win rate
    winning_days = (daily_pnl > 0).sum()
    total_active_days = (daily_pnl != 0).sum()
    win_rate = (winning_days / total_active_days * 100) if total_active_days > 0 else 0

    # Profit factor
    gross_profit = daily_pnl[daily_pnl > 0].sum()
    gross_loss = abs(daily_pnl[daily_pnl < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0

    # Buy and hold comparison
    buy_hold = (s1.iloc[-1] - s1.iloc[0]) / s1.iloc[0] * 100

    return {
        "total_return": round(float(total_return), 2),
        "sharpe_ratio": round(float(sharpe), 2),
        "max_drawdown": round(float(max_drawdown), 2),
        "win_rate": round(float(win_rate), 2),
        "profit_factor": round(float(profit_factor), 2),
        "buy_hold_return": round(float(buy_hold), 2),
        "hedge_ratio": round(float(hedge_ratio), 4),
        "buy_signals": int((signals["signal"] == 1).sum()),
        "sell_signals": int((signals["signal"] == -1).sum()),
        "dates": [str(d) for d in equity_curve.index],
        "equity_curve": [round(float(v), 2) for v in equity_curve.values],
        "zscore": [round(float(v), 4) for v in signals["zscore"].values],
        "signals": [int(v) for v in signals["signal"].values]
    }