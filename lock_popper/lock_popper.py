import sys
import math
import random

import pygame

import engine.colors as colors
from engine.engine import Engine
from engine.vector import Vec2
import engine.utils as utils
from engine.tracer import Tracer
from engine.controller import Controller

from widgets.interfaces.IDrawable import IDrawable


class Lock(IDrawable):
    STARTING_COLOR = colors.GREEN
    MID_COLOR = colors.PURPLE
    END_COLOR = colors.RED
    TUMBLER_COLOR = colors.beer

    STARTING_HITS = 50
    STARTING_VELOCITY = 1

    CLOCKWISE = True
    ANTICLOCKWISE = False

    STARTING_PALETTE = {
        "bg": colors.vivid_cerulean,
        "fg": colors.alabaster,
        "tumbler": TUMBLER_COLOR,
        "pin": colors.GREEN,
        "speed": STARTING_VELOCITY
    }

    MID_PALETTE = {
        "bg": colors.dark_green,
        "fg": colors.white_coffee,
        "tumbler": TUMBLER_COLOR,
        "pin": colors.alabaster,
        "speed": 1.5 * STARTING_VELOCITY
    }

    END_PALETTE = {
        "bg": colors.outer_space,
        "fg": colors.silver,
        "tumbler": TUMBLER_COLOR,
        "pin": colors.coral_red,
        "speed": 2.0 * STARTING_VELOCITY
    }

    def __init__(self, x, y, radius, running=False, debug=False):
        self.pos = Vec2(x, y)
        self.radius = radius
        self.palette = Lock.STARTING_PALETTE
        self.running = running
        self.win = False

        self.pin_radius = 20
        self.pin_pos = Vec2(self.pos.x + self.radius - (1.25 * self.pin_radius), self.pos.y)
        self.pin_distance = self.pos.distance(self.pin_pos)

        self.dir = Lock.CLOCKWISE
        self.angle = 0
        self.angle_rad = self.to_rads(self.angle)

        self.tumbler_radius = 20
        self.tumbler_pos = None
        self.tumbler_angle = 0
        self.tumbler_angle_rad = 0
        self.in_tumbler = False

        self.start_button = "SPACE"

        self.hits_remaining = Lock.STARTING_HITS

        self.font_size = int(radius)
        self.counter_font = pygame.freetype.SysFont(["jetbrainsmono"], self.font_size)
        self.menu_font = pygame.freetype.SysFont(["jetbrainsmono"], 20)

        self.debug = debug
        self.pin_tracer = Tracer(self.palette["fg"], 4, Lock.STARTING_HITS)

    def get_pin_point(self, angle):
        return self.get_lock_point(self.pin_distance, angle)

    def get_lock_point(self, dist, angle):
        x = dist * math.cos(angle) + self.pos.x
        y = dist * math.sin(angle) + self.pos.y
        return Vec2(x, y)

    def set_tumbler(self, angle):
        self.tumbler_angle = angle % 360
        self.tumbler_angle_rad = self.to_rads(angle)
        self.tumbler_pos = self.get_pin_point(self.tumbler_angle_rad)

    def random_tumbler(self):
        close_angle = 40
        far_angle = 160
        if self.dir:
            # Angle will be increasing
            self.set_tumbler(random.randrange(int(self.angle + close_angle), int(self.angle + far_angle), 5))
        else:
            # Angle will be decreasing
            self.set_tumbler(random.randrange(int(self.angle - far_angle), int(self.angle - close_angle), 5))

    @staticmethod
    def to_rads(angle):
        angle %= 360
        return angle * (math.pi / 180.0)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle % 360

    def next_palette(self):
        if self.palette == Lock.STARTING_PALETTE:
            self.palette = Lock.MID_PALETTE
        elif self.palette == Lock.MID_PALETTE:
            self.palette = Lock.END_PALETTE
        elif self.palette == Lock.END_PALETTE:
            self.palette = Lock.STARTING_PALETTE
        else:
            print(f"Unknown palette! {self.palette}")

    def update(self):
        if not self.running:
            return None

        # Update the pin based on elapsed time
        if self.dir:
            self.angle += self.palette["speed"]
        else:
            self.angle -= self.palette["speed"]

        self.angle_rad = self.to_rads(self.angle)

        self.pin_pos = self.get_pin_point(self.angle_rad)

        intersect_point = self.in_wedge(self.angle, self.pin_distance, self.tumbler_angle, 16)
        if self.in_tumbler and not intersect_point:
            # We missed the wedge. Lose!
            self.lose()
        if intersect_point:
            self.in_tumbler = True
        else:
            self.in_tumbler = False

        return self.running

    def check(self):
        if not self.running:
            self.running = True
            self.win = False
            self.random_tumbler()
        else:
            result = False
            # if self.pin_pos.distance(self.tumbler_pos) <= self.pin_radius + self.tumbler_radius:
            # intersect_point = self.in_wedge(self.angle, self.pin_distance, self.tumbler_angle, 16)
            if self.in_tumbler:
                # Change direction
                self.dir = not self.dir

                self.hits_remaining -= 1
                if self.hits_remaining == 0:
                    print(f"YOU WIN!")
                    self.running = False
                    self.win = True
                    self.hits_remaining = Lock.STARTING_HITS
                    self.palette = Lock.STARTING_PALETTE
                    return False

                # End section
                if self.hits_remaining <= 10:
                    self.palette = Lock.END_PALETTE

                # Mid section
                elif self.hits_remaining <= 30:
                    self.palette = Lock.MID_PALETTE

                # Start section
                else:
                    self.palette = Lock.STARTING_PALETTE

                # print(f"Pin angle: {self.angle} deg | Intersect point: {intersect_point}")
                self.pin_tracer.append(self.pin_pos)

                # Place the next tumbler
                self.random_tumbler()
                self.in_tumbler = False
                result = True

            else:
                self.lose()

            self.running = result
        return self.running

    def lose(self):
        self.hits_remaining = Lock.STARTING_HITS
        self.palette = Lock.STARTING_PALETTE
        self.running = False

        # print(f"FAILURE!")
        # print(f"Pin angle: {self.angle} deg")
        # print(f"Tumbler angle: {self.tumbler_angle} deg")

    def draw_wedge(self, screen, color, d1, d2, angle, angle_span, width=0, rounded=False):
        p1 = self.get_lock_point(d1, self.to_rads(angle - (0.5 * angle_span)))
        p2 = self.get_lock_point(d1, self.to_rads(angle + (0.5 * angle_span)))
        p3 = self.get_lock_point(d2, self.to_rads(angle + (0.5 * angle_span)))
        p4 = self.get_lock_point(d2, self.to_rads(angle - (0.5 * angle_span)))

        points = [p1.get(), p2.get(), p3.get(), p4.get()]
        pygame.draw.polygon(screen, color, points, width)
        if rounded:
            r1 = p4.distance(p3) * 0.5
            c1 = self.get_lock_point(d2, self.to_rads(angle))

            r2 = p2.distance(p1) * 0.5
            c2 = self.get_lock_point(d1, self.to_rads(angle))
            pygame.draw.circle(screen, color, c1.get(), r1, width=width)
            pygame.draw.circle(screen, color, c2.get(), r2, width=width)

    def in_wedge(self, test_angle, distance, wedge_angle, angle_span):
        p1 = self.get_lock_point(distance, self.to_rads(wedge_angle - (0.5 * angle_span)))
        p2 = self.get_lock_point(distance, self.to_rads(wedge_angle + (0.5 * angle_span)))
        intersect_point = utils.line_line_intersect(self.get_lock_point(distance, self.to_rads(test_angle)), self.pos, p1, p2)
        return intersect_point

    def draw(self, screen):
        # Draw the back of the lock
        pygame.draw.circle(screen, self.palette["bg"], self.pos.get(), self.radius)
        pygame.draw.circle(screen, self.palette["fg"], self.pos.get(), self.radius - (self.pin_radius * 2 + 10))

        if self.running:
            # Draw counter
            count_str = f"{self.hits_remaining}"
            text, t_rect = self.counter_font.render(count_str, True, self.palette["bg"])
            vo = t_rect.h * 0.5
            ho = t_rect.w * 0.5
            self.counter_font.render_to(screen, (self.pos.x - ho, self.pos.y - vo), count_str, self.palette["bg"])

            # Draw tumbler
            pygame.draw.circle(screen, self.palette["tumbler"], self.tumbler_pos.get(), self.tumbler_radius)

        else:
            menu_str = f"PRESS [{self.start_button}] TO START"
            if self.win:
                menu_str = f"YOU WIN!"

            text, t_rect = self.menu_font.render(menu_str, True, self.palette["bg"])
            vo = t_rect.h * 0.5
            ho = t_rect.w * 0.5
            self.menu_font.render_to(screen, (self.pos.x - ho, self.pos.y - vo), menu_str, self.palette["bg"])

        # Draw the pin of the lock
        inner_dist = self.pin_distance - (self.pin_radius * 0.5)
        outer_dist = self.pin_distance + (self.pin_radius * 0.5)
        self.draw_wedge(screen, self.palette["pin"], inner_dist, outer_dist, self.angle, 5, rounded=True)

        if self.debug:
            pygame.draw.line(screen, self.palette["pin"], self.pos.get(), self.pin_pos.get(), width=2)
            pygame.draw.line(screen, self.palette["tumbler"], self.tumbler_pos.get(), self.pos.get(), width=2)
            self.draw_wedge(screen, colors.BLACK, inner_dist, outer_dist, self.tumbler_angle, 15, width=2)
            self.pin_tracer.trace(screen)


class LockPopper(Engine):
    APP_NAME = "Lock Popper"
    INPUT_LOCKOUT_TIMER = 0

    def __init__(self, width, height):
        # Do custom init stuff
        self.lock = None
        self.controller = None
        self.input_mode = "KEYBOARD"
        self.joy_events = [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION, pygame.JOYAXISMOTION, pygame.JOYBALLMOTION]
        self.key_events = [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]

        # Call engine init to start main loop
        pf = 1
        super().__init__(width, height, pf)

    def on_start(self):
        self.lock = Lock(self.width * 0.5, self.height * 0.5, min(self.width, self.height) * 0.4, debug=False)
        joystick = None
        if self.joysticks:
            joystick = self.joysticks[0]
            joystick.init()

        self.controller = Controller(joystick)

    def on_update(self, et):
        # Game loop

        # Process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Keyboard events
            # Pause taking inputs when we've set the engine timer to something
            if self.engTimers[LockPopper.INPUT_LOCKOUT_TIMER].is_running():
                # print(f"Timer running! {self.engTimer0.get()} left.")
                continue

            if event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(pygame.joystick.get_count() - 1)
                joystick.init()
                self.controller.set_joystick(joystick)

            if event.type in self.joy_events:
                self.input_mode = "CONTROLLER"
                self.lock.start_button = "A"

            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
                if event.button == self.controller.button_map["A"]:
                    result = self.lock.check()
                    if not result:
                        self.engTimers[LockPopper.INPUT_LOCKOUT_TIMER].set(0.5)

                if event.button == self.controller.button_map["B"]:
                    self.lock.next_palette()

            if event.type in self.key_events:
                self.input_mode = "KEYBOARD"
                self.lock.start_button = "SPACE"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    result = self.lock.check()
                    if not result:
                        self.engTimers[LockPopper.INPUT_LOCKOUT_TIMER].set(0.5)

                if event.key == pygame.K_w:
                    self.lock.hits_remaining -= 1
                if event.key == pygame.K_s:
                    self.lock.hits_remaining -= 10
                if event.key == pygame.K_a:
                    self.lock.hits_remaining += 1
                if event.key == pygame.K_d:
                    self.lock.hits_remaining += 10
                if event.key == pygame.K_p:
                    self.lock.next_palette()
                if event.key == pygame.K_z:
                    self.lock.set_tumbler(0.0)

                if event.key == pygame.K_F1:
                    self.lock.debug = not self.lock.debug

        # Simulate
        # Update the lock
        if self.lock.running and not self.lock.update():
            self.engTimers[LockPopper.INPUT_LOCKOUT_TIMER].set(0.5)

        # Draw frame
        self.screen.fill(colors.BLACK)

        self.debug_font.render_to(self.screen, (self.lock.pos.x - 50, self.lock.pos.y + 230), f"HITS LEFT: {self.lock.hits_remaining}", colors.WHITE)
        angle_debug = f"PIN ANGLE: {round(self.lock.angle, 2)}, TUMBLER ANGLE: {round(self.lock.tumbler_angle, 2)}"
        self.debug_font.render_to(self.screen, (self.lock.pos.x - 50, self.lock.pos.y + 210), angle_debug, colors.WHITE)
        self.lock.draw(self.screen)

        pygame.display.update()


if __name__ == "__main__":
    lock_popper = LockPopper(500, 500)