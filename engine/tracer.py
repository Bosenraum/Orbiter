import pygame
import pygame.gfxdraw
from enum import Enum, auto
from engine.utils import clamp
import engine.colors as colors


class TracerType(Enum):

    POINT = auto()
    LINE = auto()
    PLINE = auto()


class Tracer:

    def __init__(self, color, width, max_length, tracer_type=TracerType.POINT, *args, **kwargs):

        self.end_color = kwargs.get("end_color", color)

        self.color = color
        self.width = width
        self.max_length = max_length
        self.tracer_type = tracer_type
        self.data = []

        for arg in args:
            self.append(arg)

    # Assume the data is appropriate for now
    def append(self, data, color=None):

        if not color:
            color = self.color

        if len(self.data) >= self.max_length:
            self.data.pop(0)
        self.data.append(data)

    def clear(self):
        self.data.clear()

    def old_calc_color(self, color, i):
        # if len(self.data) < self.max_length:
        percent = ((i / len(self.data)) ** 2) * 100
        bins = 10
        percent_rounded = clamp(0.0, ((percent // bins) + 1) * (1 / bins), 1.0)
        ff = percent_rounded
        dim = 1.0
        ff_dim = ff * dim
        return color[0] * ff_dim, color[1] * ff_dim, color[2] * ff_dim

    def calc_color(self, i):
        return colors.color_span(self.color, self.end_color, i, len(self.data))

    def trace(self, screen):
        if self.tracer_type == TracerType.POINT:
            for i, point in enumerate(self.data):
                # pygame.draw.circle(screen, self.calc_color(i), (point.x, point.y), self.width)
                pygame.gfxdraw.filled_circle(screen, int(point.x), int(point.y), int(self.width), self.calc_color(i))

        elif self.tracer_type == TracerType.PLINE:
            for i, point in enumerate(self.data):
                if i == 0:
                    continue
                # pygame.draw.line(screen, self.calc_color(i), point.get(), self.data[i-1].get(), self.width)
                pygame.gfxdraw.line(screen, int(point.x), int(point.y), int(self.data[i-1].x), int(self.data[i-1].y), self.calc_color(i))

        elif self.tracer_type == TracerType.LINE:
            for i, line in enumerate(self.data):
                color = self.calc_color(i)
                pygame.draw.line(screen, color, line[0], line[1], self.width)
        else:
            print(f"Unknown tracer type! TT={self.tracer_type}")