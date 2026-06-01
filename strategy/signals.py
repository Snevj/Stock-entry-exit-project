import pandas as pd

def generate_signals(spread):
    signals = pd.DataFrame(index=spread.index)
    signals["spread"] = spread
    signals["zscore"] = (spread - spread.rolling(window=30).mean()) / spread.rolling(window=30).std()
    
    signals["signal"] = 0
    signals.loc[signals["zscore"] > 1.5, "signal"] = -1   # sell
    signals.loc[signals["zscore"] < -1.5, "signal"] = 1   # buy
    signals.loc[signals["zscore"].abs() < 0.5, "signal"] = 0  # exit
    
    signals = signals.dropna()
    return signals