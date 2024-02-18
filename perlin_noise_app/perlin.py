
import noise

import pygame
from pygame.event import Event
from pygame.rect import Rect
import pygame.mouse as mouse

import sys
import math
import random

from engine.engine import Engine
from engine.vector import Vec2
import engine.colors as colors
import engine.snippets as snips
import engine.utils as utils

from widgets.shapes import shape_widget_factory as swf


class PerlinEngine(Engine):
    APP_NAME = "Perlin Noise"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)
        pf = kwargs.get("pf", 1)

        self.bg_color = None
        self.m1 = None
        self.m2 = None
        self.m3 = None

        self.widget_factory = None
        self.mouse_pos = None

        self.noise_x = None
        self.noise_y = None

        self.pixels = None

        super().__init__(width, height, pf)

    def on_start(self):
        self.widget_factory = swf.ShapeFactory()
        self.mouse_pos = Vec2(mouse.get_pos())

        self.bg_color = colors.get_gray(25)

        # noise.pnoise2

        self.pixels = []
        min_n, max_n = math.inf, -math.inf
        for i in range(self.width):
            for j in range(self.height):
                n1 = noise.pnoise2(i / self.width, j / self.height, octaves=3, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024,
                                   base=random.randint(0, 20))
                n2 = noise.pnoise2(i / self.width, j / self.height, octaves=6, persistence=0.5, lacunarity=3.0, base=random.randint(0, 20))
                n3 = noise.pnoise2(i / self.width, j / self.height, octaves=12, persistence=0.25, lacunarity=4.0, base=random.randint(0, 20))
                n = n1 + n2 + n3
                # print(f"({i}, {j}) => {n}")

                color = colors.get_gray(100 + n * 128 / 1.5)
                r = pygame.rect.Rect(i, j, 1, 1)
                self.pixels.append((color, r))

                if n > max_n:
                    max_n = n
                if n < min_n:
                    min_n = n

        print(f"Min n: {min_n}, Max n: {max_n}")

    def process_keydown_inputs(self, ev: Event):
        pass

    def run_sim(self):
        pass

    def draw_sim(self):
        for p in self.pixels:
            pygame.draw.rect(self.screen, p[0], p[1])

    def on_update(self, elapsed_time):

        self.m1, self.m2, self.m3 = pygame.mouse.get_pressed(3)
        self.mouse_pos = Vec2(mouse.get_pos())

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_keydown_inputs(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

        self.screen.fill(self.bg_color)

        self.run_sim()
        self.draw_sim()

        pygame.display.update()


if __name__ == "__main__":

    PerlinEngine(200, 200, pf=2)
