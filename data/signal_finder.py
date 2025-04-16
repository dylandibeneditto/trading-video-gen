import yfinance as yf
import pandas as pd
import ta

def load_data(ticker, start, end, interval='5m'):
    df = yf.download(ticker, start=start, end=end, interval=interval)
    df.dropna(inplace=True)
    print(df)
    return df

def add_indicators(df):
    print(df['Close'].values)
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'].squeeze(), window=14).rsi()
    df['sma_20'] = ta.trend.SMAIndicator(df['Close'].squeeze(), window=20).sma_indicator()
    df['sma_50'] = ta.trend.SMAIndicator(df['Close'].squeeze(), window=50).sma_indicator()
    return df

def find_rsi_extremes(df):
    signals = []
    for i in range(50, len(df)):
        rsi = df['rsi'].iloc[i]
        if rsi < 30:
            signals.append((i, 'buy'))
        elif rsi > 70:
            signals.append((i, 'short'))
    return signals

def find_ma_crossovers(df):
    signals = []
    for i in range(1, len(df)):
        prev_diff = df['sma_20'].iloc[i-1] - df['sma_50'].iloc[i-1]
        curr_diff = df['sma_20'].iloc[i] - df['sma_50'].iloc[i]
        if prev_diff < 0 and curr_diff > 0:
            signals.append((i, 'buy'))
        elif prev_diff > 0 and curr_diff < 0:
            signals.append((i, 'short'))
    return signals