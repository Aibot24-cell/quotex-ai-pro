import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    """
    Calculates comprehensive technical indicators using pure Pandas/NumPy:
    - RSI (Relative Strength Index)
    - EMA (Exponential Moving Average 12 & 26)
    - MACD & Signal Line
    - Bollinger Bands
    - Stochastic Oscillator (%K, %D)
    - ATR (Average True Range)
    - CCI (Commodity Channel Index)
    - ADX (Average Directional Index)
    """
    try:
        df = df.copy()
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.dropna(subset=['Close'], inplace=True)
        close = df['Close']
        high = df['High']
        low = df['Low']
        
        # 1. EMA (Exponential Moving Average)
        df['EMA12'] = close.ewm(span=12, adjust=False).mean()
        df['EMA26'] = close.ewm(span=26, adjust=False).mean()
        
        # 2. MACD
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # 3. RSI (14 periods)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        df['RSI'] = 100 - (100 / (1 + rs))
        df['RSI'].fillna(50, inplace=True)
        
        # 4. Bollinger Bands (20 periods, 2 std)
        rolling_mean = close.rolling(window=20).mean()
        rolling_std = close.rolling(window=20).std()
        df['BB_Middle'] = rolling_mean
        df['BB_Upper'] = rolling_mean + (rolling_std * 2)
        df['BB_Lower'] = rolling_mean - (rolling_std * 2)
        df['BB_Middle'].fillna(close, inplace=True)
        df['BB_Upper'].fillna(close * 1.02, inplace=True)
        df['BB_Lower'].fillna(close * 0.98, inplace=True)
        
        # 5. Stochastic Oscillator (%K, %D - 14, 3)
        low14 = low.rolling(window=14).min()
        high14 = high.rolling(window=14).max()
        df['Stoch_K'] = 100 * ((close - low14) / (high14 - low14 + 1e-10))
        df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()
        df['Stoch_K'].fillna(50, inplace=True)
        df['Stoch_D'].fillna(50, inplace=True)
        
        # 6. ATR (Average True Range - 14 periods)
        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=14).mean()
        df['ATR'].fillna(tr.mean(), inplace=True)
        
        # 7. CCI (Commodity Channel Index - 20 periods)
        tp = (high + low + close) / 3
        sma_tp = tp.rolling(window=20).mean()
        mad = (tp - sma_tp).abs().rolling(window=20).mean()
        df['CCI'] = (tp - sma_tp) / (0.015 * mad + 1e-10)
        df['CCI'].fillna(0, inplace=True)
        
        # 8. ADX (Average Directional Index - 14 periods)
        up_move = high - high.shift(1)
        down_move = low.shift(1) - low
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
        
        tr_smooth = df['ATR'] * 14
        plus_di = 100 * pd.Series(plus_dm).rolling(window=14).sum() / (tr_smooth + 1e-10)
        minus_di = 100 * pd.Series(minus_dm).rolling(window=14).sum() / (tr_smooth + 1e-10)
        dx = 100 * (plus_di - minus_di).abs() / ((plus_di + minus_di) + 1e-10)
        df['ADX'] = dx.rolling(window=14).mean()
        df['ADX'].fillna(25, inplace=True)
        
        return df
    except Exception as e:
        return df

def generate_sample_market_data(num_rows=60):
    """Generates synthetic market candlestick data for testing/fallback."""
    np.random.seed(42)
    base_price = 1.0850
    prices = [base_price]
    for _ in range(num_rows - 1):
        change = np.random.normal(0, 0.0005)
        prices.append(prices[-1] + change)
    
    df = pd.DataFrame({
        'Open': prices,
        'High': [p + abs(np.random.normal(0, 0.0003)) for p in prices],
        'Low': [p - abs(np.random.normal(0, 0.0003)) for p in prices],
        'Close': [p + np.random.normal(0, 0.0002) for p in prices],
        'Volume': np.random.randint(1000, 5000, size=num_rows)
    })
    return df