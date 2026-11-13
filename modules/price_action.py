import numpy as np
import pandas as pd

def analyze_price_action(df):
    if df is None or len(df) < 15:
        return {"trend": "Unknown", "support": 0.0, "resistance": 0.0, "condition": "Insufficient Data"}
    recent = df.tail(15)
    resistance = float(np.max(recent['High'].values))
    support = float(np.min(recent['Low'].values))
    current_close = float(df['Close'].iloc[-1])
    first_half = recent['Close'].iloc[:7].mean()
    second_half = recent['Close'].iloc[7:].mean()
    if second_half > first_half * 1.0003:
        trend = "Strong Uptrend"
    elif second_half < first_half * 0.9997:
        trend = "Strong Downtrend"
    else:
        trend = "Ranging / Sideways"
    return {"trend": trend, "support": support, "resistance": resistance, "current_price": current_close, "condition": "Mid-Range Momentum"}