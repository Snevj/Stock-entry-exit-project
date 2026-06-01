# strategy/spread.py
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def get_spread(s1, s2):
    # hedge ratio using linear regression
    hedge_ratio = np.polyfit(s2, s1, 1)[0]
    spread = s1 - hedge_ratio * s2
    return spread, hedge_ratio

def forecast_spread(spread):
    model = ARIMA(spread, order=(5,1,2)).fit()
    forecast = model.forecast(steps=1)
    return forecast[0]