from statsmodels.tsa.stattools import coint
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.fetcher import fetch_multiple

def find_pairs(tickers, start="2019-01-01", end="2023-12-31"):
    data = fetch_multiple(tickers, start, end)
    pairs = []
    tickers_list = data.columns.tolist()
    for i in range(len(tickers_list)):
        for j in range(i+1, len(tickers_list)):
            s1 = data[tickers_list[i]].dropna()
            s2 = data[tickers_list[j]].dropna()
            # align both series
            s1, s2 = s1.align(s2, join='inner')
            score, pvalue, _ = coint(s1, s2)
            if pvalue < 0.15:
                pairs.append((tickers_list[i], tickers_list[j], round(pvalue, 4)))
    return pd.DataFrame(pairs, columns=["Stock1", "Stock2", "P-value"])