import sys

import pygame.freetype

from engine.pixel import *
from tracer import *


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

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.pixels = []
        self.generate_pixels(width, height, pf)

        self.start()

    def generate_pixels(self, width, height, pf):
        for w in range(width):
            self.pixels.append([])
            for h in range(height):
                self.pixels[w].append(Pixel(w, h, colors.BLACK, pf))

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(BLACK)
        # Draw stuff

        pygame.display.update()

