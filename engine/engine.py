import sys

import pygame.freetype

# from engine.pixel import generate_pixels
from engine.timer import Timer, TickTimer
import engine.colors as colors
from engine.physics.physics_object import PhysicsObjectPool, PhysicsObject2D
from engine.vector import Vec2, UNIT_VECTOR_2D, NULL_VECTOR_2D


class Engine:

    debug_font = None
    CLOCK_TICK = 120
    FPS = 60

    APP_NAME = "Engine"
    MOUSE_EVENTS = [pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]
    KEYBOARD_EVENTS = [pygame.KEYDOWN, pygame.KEYUP]
    CONTROLLER_EVENTS = [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION, pygame.JOYAXISMOTION,
                         pygame.JOYBALLMOTION]

    # The screen width/height and the pixel scale factor (actual cells per pixel)
    def __init__(self, width, height, pf):
        pygame.init()
        pygame.display.set_caption(self.APP_NAME)

        # Set up controllers
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        # Load fonts
        # pygame.font.init()
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

        self.physics_object_pool = PhysicsObjectPool()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        # self.cells = generate_pixels(width, height, pf)

        self.start()

    def spawn(self, pos: Vec2, vel: Vec2 = NULL_VECTOR_2D, accel: Vec2 = NULL_VECTOR_2D):
        po = PhysicsObject2D(pos, vel, accel)
        if self.physics_object_pool.add(po):
            return po
        return None

    def draw_debug(self, text, color, posx, posy):
        img, img_rect = self.debug_font.render(text, True, color)
        self.screen.blit(img, (posx, posy))

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

