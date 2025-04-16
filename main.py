from fmov import Video
from rich.progress import Progress

from styles import styles
from video.intro import render_intro

def create_video():

    with Video((styles.render.width, styles.render.height), framerate=styles.render.fps, path="./out/output.mp4", prompt_deletion=False) as video:
        with Progress() as progress:
            task = progress.add_task("Creating video...", total=video.seconds_to_frame(5))
            for i in range(video.seconds_to_frame(5)):
                render_intro(video, i, video.seconds_to_frame(5))
                progress.update(task, advance=1)

if __name__ == "__main__":
    create_video()
    print("Video creation completed.")
