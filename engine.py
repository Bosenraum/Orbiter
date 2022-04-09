import sys
import random
import math

import pygame
import pygame.freetype

from colors import *
from pixel import *
from utils import *
from tracer import *
from vector import *


class Engine:

    debug_font = None
    CLOCK_TICK = 120
    FPS = 60

    APP_NAME = "Engine"

    # The screen width/height and the pixel scale factor (actual pixels per pixel)
    def __init__(self, width, height, pf):
        pygame.init()
        pygame.display.set_caption(Engine.APP_NAME)

        # Load fonts
        pygame.freetype.init()
        Engine.debug_font = pygame.freetype.SysFont(["consolas", "courier"], 12, bold=True)

        self.width = width * pf
        self.height = height * pf
        self.pf = pf

        self.clock = pygame.time.Clock()
        self.tick = 1 / Engine.CLOCK_TICK
        self.et = 0

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.pixels = self.generate_pixels(width, height, pf)

        self.start()

    @staticmethod
    def generate_pixels(width, height, pf):
        pixels = []
        for w in range(width):
            pixels.append([])
            for h in range(height):
                pixels.append([Pixel(w, h, colors.BLACK, pf)])
        return pixels

    def start(self):

        self.on_start()

        self.et = 0
        # Main game loop
        while True:
            self.clock.tick(self.CLOCK_TICK)
            self.et += self.tick

            self.on_update(self.et)

    def on_start(self):
        pass

    def on_update(self, elapsed_time):
        pass

