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
    """Return a list of (index, signal_type) where 5+ candles move in one direction with strength and confirmation."""
    signals = []
    df['volume_avg'] = df['Volume'].rolling(20).mean()

    for i in range(20, len(df)):
        segment = df.iloc[i-5:i]
        close_series = segment['Close'].values
        open_series = segment['Open'].values

        all_green = (close_series > open_series).all()
        all_red = (close_series < open_series).all()

        start_price = segment['Open'].iloc[0].item()
        end_price = segment['Close'].iloc[-1].item()
        move_pct = abs(end_price - start_price) / start_price

        rsi = df['rsi'].iloc[i].item()
        volume_current = df['Volume'].iloc[i].item()
        volume_avg = df['volume_avg'].iloc[i].item()

        if all_green and move_pct > 0.01 and rsi < 70 and volume_current > volume_avg:
            signals.append((i, 'buy'))
        elif all_red and move_pct > 0.01 and rsi > 30 and volume_current > volume_avg:
            signals.append((i, 'short'))

    return signals