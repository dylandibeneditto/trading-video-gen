from PIL import Image, ImageDraw
from fmov import Video
import pandas as pd

from styles import styles, pm

from video.utils.animate import ease_in_out, linear
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
    normalize = lambda price: video.height - (screen_middle - (final_close - price) / (max_price - min_price) * (video.height / 2 - 100))

    last_close_y = None
    for i, (index, row) in enumerate(df.iterrows()):
        frames_per_phase = total / 20
        current_candle = int(frame // frames_per_phase)

        if i > current_candle:
            break
        close_y = normalize(row['Close'].item())
        open_y = last_close_y if last_close_y is not None else normalize(row['Open'].item())
        high_y = normalize(row['High'].item())
        low_y = normalize(row['Low'].item())

        sx = i*candle_size + i*styles.candle_gap
        ex = sx + candle_size

        cx = (sx + ex) / 2

        # animation phases
        # candles come in linear from left to right over 5 seconds
        
        # candle animation
        # rectangle starts with no height at open
        # rectangle goes down to low
        # line comes in at low and animates to high with rectangle
        # rectangle goes down to close
        
        # make sure colors update correctly from rectangle

        line_sx = cx - 2
        line_sy = min(high_y, low_y)
        line_ex = cx + 2
        line_ey = max(high_y, low_y)
        rect_sx = sx
        rect_sy = min(open_y, close_y)
        rect_ex = ex
        rect_ey = max(open_y, close_y)

        up = close_y < open_y

        start_frame = i * frames_per_phase
        end_frame = (i + 1) * frames_per_phase

        if start_frame <= frame < end_frame:
            body_color = styles.colors.up if up else styles.colors.down
            frame_in_phase = frame - start_frame
            subphases = 3
            current_subphase = int(subphases * (frame_in_phase / frames_per_phase))
            frame_in_subphase = frame_in_phase % (frames_per_phase / subphases)
            completion_of_subphase = (subphases * (frame_in_phase / frames_per_phase)) % 1
            if current_subphase == 0:
                # rectangle goes down to low
                if up:
                    # goes to low
                    sy = open_y
                    ey = linear(open_y, low_y, completion_of_subphase)
                    draw.rectangle((p(rect_sx), p(min(sy, ey)), p(rect_ex), p(max(sy, ey))), fill=styles.colors.down)
                else:
                    # goes to high
                    sy = linear(open_y, high_y, completion_of_subphase)
                    ey = open_y
                    draw.rectangle((p(rect_sx), p(min(sy, ey)), p(rect_ex), p(max(sy, ey))), fill=styles.colors.up)
            elif current_subphase == 1:
                if up:
                    # goes to high
                    sy = linear(low_y, high_y, completion_of_subphase)
                    ey = open_y
                    color = styles.colors.up if ey > sy else styles.colors.down
                    draw.rectangle((p(rect_sx), p(min(sy, ey)), p(rect_ex), p(max(sy, ey))), fill=color)
                    draw.rectangle((p(line_sx), p(min(sy, low_y)), p(line_ex), p(max(sy, low_y))), fill=color)
                else:
                    # goes to low
                    sy = linear(high_y, low_y, completion_of_subphase)
                    ey = open_y
                    color = styles.colors.up if ey > sy else styles.colors.down
                    draw.rectangle((p(rect_sx), p(min(sy, ey)), p(rect_ex), p(max(sy, ey))), fill=color)
                    draw.rectangle((p(line_sx), p(min(sy, high_y)), p(line_ex), p(max(sy, high_y))), fill=color)
            else:
                if up:
                    sy = linear(high_y, close_y, completion_of_subphase)
                    ey = open_y
                else:
                    sy = linear(low_y, close_y, completion_of_subphase)
                    ey = open_y
                draw.rectangle((p(rect_sx), p(min(sy, ey)), p(rect_ex), p(max(sy, ey))), fill=body_color)
                draw.rectangle((p(line_sx), p(line_sy), p(line_ex), p(line_ey)), fill=body_color)
        else:
            body_color = styles.colors.up if up else styles.colors.down
            draw.rectangle((p(line_sx), p(line_sy), p(line_ex), p(line_ey)), fill=body_color)
            draw.rectangle((p(rect_sx), p(rect_sy), p(rect_ex), p(rect_ey)), fill=body_color)

            last_close_y = close_y

    return image