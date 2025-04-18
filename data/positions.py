import yfinance as yf
import pandas as pd
import ta

def load_data(ticker, start, end, interval='5m'):
    df = yf.download(ticker, start=start, end=end, interval=interval)
    df.dropna(inplace=True)
    return df

def add_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'].squeeze(), window=14).rsi()
    df['sma_20'] = ta.trend.SMAIndicator(df['Close'].squeeze(), window=20).sma_indicator()
    df['sma_50'] = ta.trend.SMAIndicator(df['Close'].squeeze(), window=50).sma_indicator()
    return df

def find_teaching_signals(df):
    """Return a list of (index, signal_type) where 5+ candles move in one direction."""
    signals = []
    for i in range(5, len(df)):
        segment = df.iloc[i-5:i]
        close_series = segment['Close'].values
        open_series = segment['Open'].values

        all_green = (close_series > open_series).all()
        all_red = (close_series < open_series).all()

        if all_green:
            signals.append((i, 'buy'))
        elif all_red:
            signals.append((i, 'short'))

    return signals