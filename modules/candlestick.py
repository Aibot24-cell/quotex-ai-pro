import pandas as pd
import numpy as np

def detect_candlestick_patterns(df):
    if df is None or len(df) < 3:
        return []
    patterns = []
    c_curr = df.iloc[-1]
    c_prev = df.iloc[-2]
    body_curr = abs(c_curr['Close'] - c_curr['Open'])
    range_curr = c_curr['High'] - c_curr['Low']
    if range_curr == 0:
        range_curr = 0.00001
    is_bullish_prev = c_prev['Close'] > c_prev['Open']
    is_bearish_prev = c_prev['Close'] < c_prev['Open']
    is_bullish_curr = c_curr['Close'] > c_curr['Open']
    is_bearish_curr = c_curr['Close'] < c_curr['Open']
    upper_wick_curr = c_curr['High'] - max(c_curr['Open'], c_curr['Close'])
    lower_wick_curr = min(c_curr['Open'], c_curr['Close']) - c_curr['Low']

    if body_curr <= (range_curr * 0.10):
        patterns.append({"name": "Doji", "type": "Neutral / Indecision", "implication": "Market indecision."})
    if (lower_wick_curr >= 2 * body_curr) and (upper_wick_curr <= 0.15 * range_curr):
        patterns.append({"name": "Hammer", "type": "Bullish Reversal", "implication": "Rejection of lower prices."})
    if (upper_wick_curr >= 2 * body_curr) and (lower_wick_curr <= 0.15 * range_curr):
        patterns.append({"name": "Shooting Star", "type": "Bearish Reversal", "implication": "Rejection of higher prices."})
    if is_bearish_prev and is_bullish_curr and (c_curr['Open'] <= c_prev['Close']) and (c_curr['Close'] >= c_prev['Open']):
        patterns.append({"name": "Bullish Engulfing", "type": "Bullish Reversal", "implication": "Buyers overtook sellers."})
    if is_bullish_prev and is_bearish_curr and (c_curr['Open'] >= c_prev['Close']) and (c_curr['Close'] <= c_prev['Open']):
        patterns.append({"name": "Bearish Engulfing", "type": "Bearish Reversal", "implication": "Sellers overwhelmed buyers."})
    return patterns