import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


tickers = ["SPY","AAPL", "MSFT"]

import yfinance as yf
import pandas as pd
import sqlite3

tickers = [
    # Broad Market ETFs
    "SPY", "QQQ", "IWM", "DIA", "EFA", "EEM", "TLT", "GLD",

    # Large-Cap US Stocks
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "XOM",

    # Sector ETFs
    "XLK", "XLF", "XLE", "XLV", "XLY", "XLP",

    # Crypto (optional, 24/7 trading)
    "BTC-USD", "ETH-USD", "SOL-USD"
]

conn = sqlite3.connect("mean_reversion_data.db")

for ticker in tickers:
    data = yf.download(ticker, start="2015-01-01", end="2024-01-01")
    data["returns"] = data["Close"].pct_change()
    data["zscore"] = (data["Close"] - data["Close"].rolling(5).mean()) / data["Close"].rolling(5).std()
    data["signal"] = 0
    data.loc[data["zscore"] < -2, "signal"] = 1
    data.loc[data["zscore"] > 2, "signal"] = -1
    data["strategy"] = data["signal"].shift(1) * data["returns"]
    data.to_sql(f"mean_reversion_{ticker}", conn, if_exists="replace", index=True)
    print(f"Data saved to table 'mean_reversion_{ticker}'.")

conn.close()

# Cumulative performance
(1 + data[["returns", "strategy"]]).cumprod().plot(figsize=(12,6))
plt.title("SPY Buy & Hold vs. Mean Reversion Strategy")
plt.savefig("strategy_plot.png")
plt.show()
