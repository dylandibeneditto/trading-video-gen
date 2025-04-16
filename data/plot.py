import matplotlib.pyplot as plt

def plot_trade_setup(df, idx, signal_type):
    window = df.iloc[idx-20:idx+5]
    plt.figure(figsize=(12, 6))
    plt.plot(window.index, window['Close'], label='Close', color='black')
    plt.plot(window.index, window['Open'], label='Open', color='gray')
    plt.plot(window.index, window['High'], label='High', color='green')
    plt.plot(window.index, window['Low'], label='Low', color='red')
    plt.plot(window.index, window['sma_20'], label='SMA 20', linestyle='--', color='blue')
    plt.plot(window.index, window['sma_50'], label='SMA 50', linestyle='--', color='red')
    plt.axvline(x=df.index[idx], color='green' if signal_type == 'buy' else 'red', linestyle='--', linewidth=2)
    plt.title(f"{signal_type.upper()} signal on {df.index[idx].date()}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()