import math

def ease_in_out(start: int, end: int, t: float) -> int:
    if t < 0:
        t = 0
    elif t > 1:
        t = 1

    change = end - start
    if t < 0.5:
        eased_value = change * (4 * t ** 3) + start
    else:
        eased_value = change * (1 - (-2 * t + 2) ** 3 / 2) + start

    return round(eased_value)

def linear(start: int, end: int, t: float) -> int:
    if t < 0:
        t = 0
    elif t > 1:
        t = 1

    change = end - start
    eased_value = change * t + start

    return round(eased_value)