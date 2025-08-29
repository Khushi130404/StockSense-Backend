import pandas as pd
import yfinance as yf
from datetime import datetime
import time # Import the time module

# --- This can be in your settings file ---
YF_PERIOD = "7d" # Shorter period for more recent data
YF_INTERVAL = "5m" # Use a smaller interval for near real-time
CACHE_DURATION_SECONDS = 15 * 60 # 15 minutes
# ----------------------------------------

_cache = {} # The cache will now store a tuple: (data, timestamp)

def get_ohlc(symbol: str) -> pd.DataFrame:
    """
    Fetches OHLC data with a time-aware cache to ensure data freshness.
    """
    key = (symbol, YF_PERIOD, YF_INTERVAL)
    
    # Check if the key exists and if the data is fresh
    if key in _cache:
        df, timestamp = _cache[key]
        if (time.time() - timestamp) < CACHE_DURATION_SECONDS:
            print(f"Reading '{symbol}' from fresh cache.")
            return df.copy()

    # If cache is old or doesn't exist, fetch new data
    print(f"Fetching fresh data for '{symbol}' from yfinance...")
    df = yf.download(
        symbol, 
        period=YF_PERIOD, 
        interval=YF_INTERVAL, 
        auto_adjust=True, 
        progress=False
    )
    
    if df.empty:
        return pd.DataFrame() # Return an empty DataFrame if download fails

    df = df.rename(columns=str.lower)
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    
    # Store the new data and the current timestamp in the cache
    _cache[key] = (df, time.time())
    
    return df.copy()

# Your recent_news function is good, no changes needed there.
def recent_news(symbol: str):
    try:
        tk = yf.Ticker(symbol)
        return tk.news or []
    except Exception:
        return []
    
    # testing the code
    # --- ADD THIS TEST BLOCK AT THE END OF YOUR FILE ---

# This code will only run when you execute `python -m app.data`
if __name__ == "__main__":
    # 1. Choose a stock to test with
    test_symbol = "AAPL" # Using a local Indian stock for a good test
    print(f"--- Testing data fetch for {test_symbol} ---")
    
    # 2. Call your function
    stock_df = get_ohlc(test_symbol)
    
    # 3. Check the result
    if stock_df is not None and not stock_df.empty:
        print("✅ Data fetched successfully!")
        
        # Print the shape of the DataFrame (rows, columns)
        print(f"Shape of data: {stock_df.shape}")
        
        # Print the last 5 rows to see the most recent data
        print("--- Most recent data: ---")
        print(stock_df.tail())
    else:
        print("❌ Failed to fetch data or the DataFrame is empty.")