import yfinance as yf

def fetch_stock(ticker, start="2019-01-01", end="2023-12-31"):
    data = yf.download(ticker, start=start, end=end, multi_level_index=False)
    return data["Close"]

def fetch_multiple(tickers, start="2019-01-01", end="2023-12-31"):
    data = yf.download(tickers, start=start, end=end, multi_level_index=False)
    return data["Close"]