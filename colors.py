from pygame import Color
import random

BLACK = (0x00, 0x00, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
RED   = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE  = (0x00, 0x00, 0xFF)

# Reds
coral_red = Color(254, 67, 60)
razzmatazz = Color(243, 29, 100)

# Pink
pink = Color(255,192,203)

# Greens
dark_green = Color(0x00, 0x80, 00)

# Blues
byzantine = Color(162, 36, 173)
grape = Color(106, 56, 179)
violet_blue = Color(60, 80, 177)
vivid_cerulean = Color(0, 149, 239)
# blue_violet = Color(138,43,226)
blue_violet = (138, 43, 226, 255)

# Purples
deep_purple = Color(88, 24, 69)

# Whites
alabaster = Color(245, 243, 230)
white_coffee = (228, 225, 209)
beer = Color(246, 151, 23)
empty_beer = (246, 151, 23, 25)

# Grays
outer_space = Color(69, 69, 69)
silver = Color(192,192,192)


def color_clamp(c):
    nc = []
    for i in range(len(c)):
        if c[i] < 0:
            nc.append(0)
        elif c[i] > 255:
            nc.append(255)
        else:
            nc.append(c[i])

    return tuple(nc)


def color_span(c1, c2, cur, total):
    # cr = int(c1[0] + ((c1[0] - c2[0]) * c2[0] * cur / total))
    cr = int(((c2[0] - c1[0]) * cur / total) + c1[0])
    cg = int(((c2[1] - c1[1]) * cur / total) + c1[1])
    cb = int(((c2[2] - c1[2]) * cur / total) + c1[2])
    ca = 255
    if len(c1) > 3 and len(c2) > 3:
        ca = int(((c2[3] - c1[3]) * cur / total) + c1[3])

    color = color_clamp((cr, cg, cb, ca))

    return color


def blend(c1, c2):
    cr = int((c1[0] + c2[0]) / 2)
    cg = int((c1[1] + c2[1]) / 2)
    cb = int((c1[2] + c2[2]) / 2)

    return color_clamp((cr, cg, cb))


def get_random_color(r_lim=(0, 255), g_lim=(0, 255), b_lim=(0, 255)):
    r = random.randint(r_lim[0], r_lim[1])
    g = random.randint(g_lim[0], g_lim[1])
    b = random.randint(b_lim[0], b_lim[1])
    return Color(color_clamp((r, g, b)))

