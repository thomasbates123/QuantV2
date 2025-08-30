import yfinance as yf

# Create a Ticker object
ticker = yf.Ticker("AAPL")  # Replace "AAPL" with the desired stock symbol

# Get historical data
historical_data = ticker.history(period="1mo")  # Options: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"

# Display the data
print(historical_data)