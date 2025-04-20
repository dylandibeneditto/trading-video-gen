from types import SimpleNamespace
from PIL import ImageFont

# production, debug anim, debug image, debug
setting = "production"
pm = 1

font_paths = {
    "regular": "./video/assets/fonts/SF-Pro-Display-Regular.otf",
    "bold": "./video/assets/fonts/SF-Pro-Display-Bold.otf",
    "medium": "./video/assets/fonts/SF-Pro-Display-Medium.otf",
    "semibold": "./video/assets/fonts/SF-Pro-Display-Semibold.otf",
    "semibold-italic": "./video/assets/fonts/SF-Pro-Display-SemiboldItalic.otf",
    "italic": "./video/assets/fonts/SF-Pro-Display-RegularItalic.otf",
}

if setting == "debug anim":
    pm = 0.5
elif setting == "debug image":
    pm = 1.5
    styles.render.fps = 10
if setting == "debug":
    pm = 0.5
    styles.render.fps = 10

styles = SimpleNamespace(
    render=SimpleNamespace(
        width=1080*pm,
        height=1920*pm,
        pm=pm,
        fps=60,
    ),
    fonts=SimpleNamespace(
        title=ImageFont.truetype(font_paths["bold"], 56*pm),
        text=ImageFont.truetype(font_paths["regular"], 24*pm),
    ),
    colors=SimpleNamespace(
        background="#0A0A0A",
        text="#F5F5F5",
        up="#30D158",
        down="#FF453A",
        grid="#1A1A1A"
    ),
    top_safe_area=50,
    trailing_safe_area=(100,100),
    candle_gap=8,
)

