from fmov import Video
from rich.progress import Progress, track

from styles import styles, pm
from video.intro import render_intro

from data.positions import load_data, add_indicators, find_teaching_signals

prog = None

def create_video(name, df):
    with Video((styles.render.width, styles.render.height), framerate=styles.render.fps, path=f"./out/{name}.mp4", prompt_deletion=False) as video:
        task = prog.add_task("Creating video...", total=video.seconds_to_frame(5))

        final_intro = None
        
        # intro, 5 seconds
        for i in range(video.seconds_to_frame(5)):
            image = render_intro(video, i, video.seconds_to_frame(5), df.iloc[:40])
            video.pipe(image)
            if i == video.seconds_to_frame(5) - 1:
                final_intro = image
            prog.update(task, advance=1)

        prog.remove_task(task)

if __name__ == "__main__":
    ticker = "AAPL"
    df = load_data(ticker, "2000-01-01", "2025-04-17", interval="1d")
    df = add_indicators(df)

    signals = find_teaching_signals(df)
    print(f"Found {len(signals)} teaching-quality signals.")

    with Progress() as progress:
        prog = progress
        task = progress.add_task("Creating videos...", total=len(signals))

        for i, (idx, signal_type) in enumerate(signals):
            progress.update(task, advance=1)
            create_video(f"output_{i}", df.iloc[idx-40:idx+5])
