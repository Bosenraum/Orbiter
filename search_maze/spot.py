from pygame import rect, draw, freetype
from engine.vector import Vec2
import engine.colors as colors
import math

from widgets.interfaces.IDrawable import IDrawable

if not freetype.get_init():
    freetype.init()


class Spot(IDrawable):

    def __init__(self, pos: Vec2, width, height, color, offset: Vec2, walkable=True, border_width=0):
        self.pos = pos
        self.maze_pos = Vec2(self.pos.x * width, self.pos.y * height)
        self.width = width
        self.height = height
        self.color = color
        self.offset = offset
        self.border_width = border_width

        self.walkable = walkable

        self.parent = None

        self.neighbors = []
        self.soft_reset()

    def __eq__(self, other):
        # Can change check for equality if needed
        if other is None:
            return False

        return self.pos == other.pos

    def __hash__(self):
        return hash((self.pos, self.height, self.width))

    def draw(self, screen):
        p = self.abs_pos
        color = self.color if self.walkable else colors.get_gray(35)
        draw.rect(screen, color, rect.Rect(p.x, p.y, self.width - 2, self.height - 2), self.border_width)

    def get_center(self):
        abs_pos = Vec2(self.pos.x * self.width + self.offset.x,
                       self.pos.y * self.height + self.offset.y)
        return Vec2(abs_pos.x + (self.width * 0.5), abs_pos.y + (self.height * 0.5))

    def soft_reset(self):
        self.f = math.inf
        self.g = math.inf
        self.h = 0

    def add_neighbors(self, maze):
        if not self.walkable:
            return

        r = self.pos.x
        c = self.pos.y
        mask = [
            (r + 1, c + 1),
            (r - 1, c + 1),
            (r + 1, c - 1),
            (r - 1, c - 1),
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1)
         ]

        for loc in mask:
            spot = maze.get_spot(loc[0], loc[1])
            if spot:
                self.neighbors.append(spot)

    @property
    def abs_pos(self):
        return Vec2(self.pos.x * self.width + self.offset.x, self.pos.y * self.height + self.offset.y)

    # def add_neighbors(self, search_maze):
    #     mask = [
    #         [0, 1, 0],
    #         [1, 0, 1],
    #         [0, 1, 0]
    #     ]
    #
    #     me = (1, 1)
    #     for row, m in enumerate(mask):
    #         for col, v in enumerate(m):
    #             if v:
    #                 dr = me[0] - row
    #                 dc = me[1] - col
    #                 neighbor = search_maze.get_spot(self.row + dr, self.col + dc)
    #                 if neighbor:
    #                     self.neighbors.append(neighbor)


class SpotMarker(IDrawable):

    def __init__(self, spot, color, radius_multiplier=0.9, border_width=0):
        self.spot = spot
        self.color = color
        self.border_width = border_width
        self.radius_multiplier = radius_multiplier

        self.spot_font = None
        # self.font_size = int(self.spot.height * 0.5)
        self.font_size = 14

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size
        self.spot_font = freetype.SysFont("lucidabright", font_size)

    def draw(self, screen, override_color=None, debug=False):
        radius = self.radius_multiplier * min(self.spot.width, self.spot.height) // 2
        color = override_color if override_color else self.color
        draw.circle(screen, color, self.spot.get_center().get(), radius, self.border_width)
        draw.circle(screen, colors.Grey.outline_black, self.spot.get_center().get(), self.spot.width * self.radius_multiplier // 2, 2)

        if debug:
            # Playing with some spot font things
            if self.spot.f is math.inf:
                spot_text = f"I"
            else:
                spot_text = f"{round(self.spot.f)}"

            text_pos = Vec2(self.spot.abs_pos.x + 0.2 * self.spot.width, self.spot.abs_pos.y + 0.2 * self.spot.height)
            self.spot_font.render_to(screen, text_pos.get(), spot_text)
