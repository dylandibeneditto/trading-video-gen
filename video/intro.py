from PIL import Image, ImageDraw
from fmov import Video
import pandas as pd

from styles import styles, pm

from video.utils.animate import ease_in_out
from video.utils.position import p

def render_intro(video: Video, frame: int, total: int, df: pd.DataFrame) -> None:
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

    candle_size = (styles.render.width-styles.trailing_safe_area[0]) / 25 - styles.candle_gap

    # Normalize the data so that the final closing price is directly in the middle of the screen
    final_close = df.iloc[-1]['Close'].item()
    screen_middle = video.height / 2
    min_price = df[['Open', 'Close', 'High', 'Low']].min().min()
    max_price = df[['Open', 'Close', 'High', 'Low']].max().max()
    normalize = lambda price: screen_middle - (final_close - price) / (max_price - min_price) * (video.height / 2 - 100)

    for i, (index, row) in enumerate(df.iterrows()):
        open_y = p(normalize(row['Open'].item()))
        close_y = p(normalize(row['Close'].item()))
        high_y = p(normalize(row['High'].item()))
        low_y = p(normalize(row['Low'].item()))

        sx = i*candle_size + i*styles.candle_gap
        ex = sx + candle_size

        cx = (sx + ex) / 2

        body_color = styles.colors.up if row['Close'].item() < row['Open'].item() else styles.colors.down
        draw.rectangle((p(cx-2), min(high_y, low_y), p(cx+2), max(high_y, low_y)), fill=body_color)
        draw.rectangle((p(sx), min(open_y, close_y), p(ex), max(open_y, close_y)), fill=body_color)

    video.pipe(image)