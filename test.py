import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



tickers = [
    # Broad Market ETFs
    "SPY"
]

for ticker in tickers:
    data = yf.download(ticker, start="2015-01-01", end="2024-01-01")
    data["returns"] = data["Close"].pct_change()
    data["zscore"] = (data["Close"] - data["Close"].rolling(5).mean()) / data["Close"].rolling(5).std()
    data["signal"] = 0
    data.loc[data["zscore"] < -1.5, "signal"] = 1
    data.loc[data["zscore"] > 1.5, "signal"] = -1
    data["strategy"] = data["signal"].shift(1) * data["returns"]
    
    

# Cumulative performance
(1 + data[["returns", "strategy"]]).cumprod().plot(figsize=(12,6))
plt.title("SPY Buy & Hold vs. Mean Reversion Strategy")
plt.savefig("strategy_plot.png")
plt.show()


