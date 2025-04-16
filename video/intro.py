from PIL import Image, ImageDraw
from fmov import Video

from styles import styles, pm

from video.utils.animate import ease_in_out
from video.utils.position import p

def render_intro(video: Video, frame: int, total: int) -> None:
    """
    Renders the intro section for the video.
    
    Includes the title and the the inital animation of the candlesticks
    """
    image = Image.new("RGB", (video.width, video.height), styles.colors.background)
    draw = ImageDraw.Draw(image)
    grid_lines = (5,20)
    for x in range(1,grid_lines[0]):
        pos = (video.width-styles.trailing_safe_area[0])/grid_lines[0]*x
        draw.rectangle((p(pos), 0, p(pos+1), p(ease_in_out(0, video.height, frame / total))), fill=styles.colors.grid)
    for y in range(1,grid_lines[1]):
        pos = (video.height-styles.top_safe_area-styles.trailing_safe_area[1])/grid_lines[1]*y+styles.top_safe_area
        draw.rectangle((0, p(pos), p(ease_in_out(0, video.width, frame / total)), p(pos+1)), fill=styles.colors.grid)

    video.pipe(image)