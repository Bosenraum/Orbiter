import sys

import pygame.freetype

# from engine.pixel import generate_pixels
from engine.timer import Timer, TickTimer
import colors


class Engine:

    debug_font = None
    CLOCK_TICK = 120
    FPS = 60

    APP_NAME = "Engine"

    # The screen width/height and the pixel scale factor (actual pixels per pixel)
    def __init__(self, width, height, pf):
        pygame.init()
        pygame.display.set_caption(self.APP_NAME)

        # Load fonts
        pygame.font.init()
        pygame.freetype.init()
        Engine.debug_font = pygame.freetype.SysFont(["consolas", "courier"], 12, bold=True)

        self.width = width * pf
        self.height = height * pf
        self.pf = pf

        self.clock = pygame.time.Clock()
        self.tick = 1 / Engine.CLOCK_TICK
        self.et = 0

        self.numEngTimers = 4
        self.numTickTimers = 4
        self.engTimers = [Timer(0.0) for _ in range(self.numEngTimers)]
        self.tickTimers = [TickTimer(0) for _ in range(self.numTickTimers)]

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        # self.pixels = generate_pixels(width, height, pf)

        self.start()

    def process_key_inputs(self, ev: pygame.event.Event):
        pass
        # if ev.key == pygame.K_SPACE:
        #     print(f"Pressed space.")
        #
        # # Debug toggle
        # if ev.key == pygame.K_F1:
        #     self.debug = not self.debug

    def process_mouse_inputs(self, ev: pygame.event.Event):
        pass
        # if ev.type == pygame.MOUSEBUTTONDOWN:
        #     # Mouse down events
        #     pass
        # if ev.type == pygame.MOUSEBUTTONUP:
        #     # Mouse up events
        #     pass
        #
        # if ev.type == pygame.MOUSEWHEEL:
        #     # Mousewheel events
        #     pass
        #
        # if ev.type == pygame.MOUSEMOTION:
        #     # Mouse motion events
        #     pass

    def start(self):

        self.on_start()

        self.et = 0
        # Main game loop
        while True:
            self.clock.tick(self.CLOCK_TICK)
            self.et += self.tick

            # Tick engine timers
            for engTimer, tickTimer in zip(self.engTimers, self.tickTimers):
                engTimer.tick(self.tick)
                tickTimer.tick()

            self.on_update(self.et)

    def on_start(self):
        pass

    def on_update(self, elapsed_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(colors.BLACK)
        # Draw stuff

        pygame.display.update()

