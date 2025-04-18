from fmov import Video
from rich.progress import Progress

from styles import styles
from video.intro import render_intro

from data.positions import load_data, add_indicators, find_teaching_signals

def create_video(name, df):
    with Video((styles.render.width, styles.render.height), framerate=styles.render.fps, path=f"./out/{name}.mp4", prompt_deletion=False) as video:
        with Progress() as progress:
            task = progress.add_task("Creating video...", total=video.seconds_to_frame(5))
            for i in range(video.seconds_to_frame(5)):
                render_intro(video, i, video.seconds_to_frame(5), df.iloc[:20])
                progress.update(task, advance=1)

if __name__ == "__main__":
    ticker = "^NDX"
    df = load_data(ticker, "2025-02-28", "2025-04-17", interval="5m")
    df = add_indicators(df)

    signals = find_teaching_signals(df)
    print(f"Found {len(signals)} teaching-quality signals.")

    for i, (idx, signal_type) in enumerate(signals):
        create_video(f"output_{i}", df.iloc[idx-20:idx+5])
