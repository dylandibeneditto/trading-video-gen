from fmov import Video
from rich.progress import Progress

from styles import styles
from video.intro import render_intro

from data.signal_finder import load_data, add_indicators, find_rsi_extremes, find_ma_crossovers
from data.plot import plot_trade_setup

def create_video(name, df):
    with Video((styles.render.width, styles.render.height), framerate=styles.render.fps, path=f"./out/{name}.mp4", prompt_deletion=False) as video:
        with Progress() as progress:
            task = progress.add_task("Creating video...", total=video.seconds_to_frame(5))
            for i in range(video.seconds_to_frame(5)):
                render_intro(video, i, video.seconds_to_frame(5), df.iloc[:20])
                progress.update(task, advance=1)

if __name__ == "__main__":
    ticker = "^NDX"
    df = load_data(ticker, "2024-01-01", "2025-01-01", interval='1d')
    df = add_indicators(df)

    rsi_signals = find_rsi_extremes(df)
    ma_signals = find_ma_crossovers(df)

    print(f"Found {len(rsi_signals)} RSI-based signals.")
    print(f"Found {len(ma_signals)} MA crossover signals.")

    valid_signals = []

    for idx, signal_type in rsi_signals + ma_signals:
        if idx < 20 or idx + 5 >= len(df):
            continue  # not enough data for before/after window

        after_window = df.iloc[idx+1:idx+6]  # 5 candles after signal

        if signal_type == 'buy':
            if all(after_window['Close'] > after_window['Open']):
                valid_signals.append((idx, signal_type))
        elif signal_type == 'short':
            if all(after_window['Close'] < after_window['Open']):
                valid_signals.append((idx, signal_type))

    for i, (idx, signal_type) in enumerate(valid_signals):
        create_video(f"output_{i}", df.iloc[idx-20:idx+5])
