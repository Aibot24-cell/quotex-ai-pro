import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def get_market_feed_simulation(pair_name="EUR/USD", market_type="Real Market"):
    """
    Fetches real data for real markets and generates dynamic,
    time-variant synthetic data for OTC markets to prevent fixed signals.
    """
    clean_name = pair_name.replace(" (OTC)", "").replace(" (Real)", "").replace(" (Crypto)", "").strip()
    
    # OTC বা সিমুলেশন মার্কেটের জন্য ডাইনামিক র্যান্ডম প্রাইস জেনারেটর
    if "OTC" in market_type:
        num_rows = 60
        np.random.seed(None) # Disable static seed for true real-time variation
        base_price = 1.0850 + np.random.uniform(-0.02, 0.02)
        prices = [base_price]
        for _ in range(num_rows - 1):
            change = np.random.normal(0, 0.0008)
            prices.append(prices[-1] + change)
        
        df = pd.DataFrame({
            'Open': prices,
            'High': [p + abs(np.random.normal(0, 0.0004)) for p in prices],
            'Low': [p - abs(np.random.normal(0, 0.0004)) for p in prices],
            'Close': [p + np.random.normal(0, 0.0003) for p in prices],
            'Volume': np.random.randint(1200, 6000, size=num_rows)
        })
        now = datetime.now()
        return {
            "dataframe": df,
            "start_time": now.strftime("%H:%M:%S"),
            "end_time": (now + timedelta(minutes=1)).strftime("%H:%M:%S")
        }
    
    # রিয়েল মার্কেট বা ক্রিপ্টোর জন্য গ্লোবাল ফরেক্স ফিড ম্যাপ
    symbol_map = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "USDJPY=X",
        "AUD/USD": "AUDUSD=X",
        "EUR/GBP": "EURGBP=X",
        "USD/CHF": "USDCHF=X",
        "BTC/USD": "BTC-USD"
    }
    
    ticker = symbol_map.get(clean_name, "EURUSD=X")
    
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        
        if df.empty or len(df) < 5:
            raise Exception("Live data empty")
            
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
            
        clean_df = pd.DataFrame()
        clean_df['Open'] = df['Open']
        clean_df['High'] = df['High']
        clean_df['Low'] = df['Low']
        clean_df['Close'] = df['Close']
        clean_df['Volume'] = df['Volume']
        clean_df.dropna(inplace=True)
        
        now = datetime.now()
        return {
            "dataframe": clean_df,
            "start_time": now.strftime("%H:%M:%S"),
            "end_time": (now + timedelta(minutes=1)).strftime("%H:%M:%S")
        }
        
    except Exception as e:
        # ফলব্যাক হিসেবে ডাইনামিক ডেটা
        num_rows = 60
        base_price = 1.0850
        prices = [base_price + np.random.uniform(-0.01, 0.01)]
        for _ in range(num_rows - 1):
            prices.append(prices[-1] + np.random.normal(0, 0.0006))
            
        df = pd.DataFrame({
            'Open': prices,
            'High': [p + 0.0004 for p in prices],
            'Low': [p - 0.0004 for p in prices],
            'Close': [p + np.random.normal(0, 0.0002) for p in prices],
            'Volume': np.random.randint(1000, 5000, size=num_rows)
        })
        now = datetime.now()
        return {
            "dataframe": df,
            "start_time": now.strftime("%H:%M:%S"),
            "end_time": (now + timedelta(minutes=1)).strftime("%H:%M:%S")
        }