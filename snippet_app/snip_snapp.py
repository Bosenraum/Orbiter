import pygame
from pygame.event import Event
from pygame.rect import Rect
import pygame.mouse as mouse

import sys
import math

from engine.engine import Engine
from engine.vector import Vec2
import engine.colors as colors
import engine.snippets as snips
import engine.utils as utils

from widgets.shapes import shape_widget_factory as swf

# Demos for ideas from blog.bruce-hill.com/6-useful-snippets

GOLDEN_RATIO = (math.sqrt(5) + 1) / 2


def mix(low, high, amount):
    return (1 - amount) * low + amount * high


def get_gr_sample(i):
    return (i * GOLDEN_RATIO) % 1


class SnipEngine(Engine):
    APP_NAME = "Snippets"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.bg_color = None
        self.box = None
        self.m1 = None
        self.m2 = None
        self.m3 = None

        self.widget_factory = None
        self.mouse_pos = None

        pf = 1
        super().__init__(width, height, pf)

    def on_start(self):
        self.widget_factory = swf.ShapeFactory()
        self.mouse_pos = Vec2(mouse.get_pos())

        self.bg_color = colors.get_gray(25)
        color = colors.Blue.electric_blue
        start_pos = Vec2((self.width / 2) - 50, (self.height / 2) - 50)

        self.box = self.widget_factory.create("rectangle")
        self.box.pos = start_pos
        self.box.width = 20
        self.box.height = 20
        self.box.color = color

    def process_keydown_inputs(self, ev: Event):

        if ev.key == pygame.K_SPACE:
            print(f"Space at {self.mouse_pos}")

    def run_sim(self):
        if self.m1:
            speed = 0.1
            self.box.pos = mix(self.box.pos, self.mouse_pos, speed)

        if self.m3:
            new_pos = snips.new_pos(self.box.pos, self.mouse_pos, 1 / self.FPS,
                                    0.01 * (self.mouse_pos - self.box.pos))
            new_pos = Vec2(utils.clamp(0, self.width, new_pos.x),
                           utils.clamp(0, self.height, new_pos.y))
            self.box.pos = new_pos

    def draw_sim(self):
        self.box.draw(self.screen)

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
    print(f"Golden Ratio = {GOLDEN_RATIO}")

    # for x in range(20):
    #     print(f"{x=}, GR={get_gr_sample(x)}")

    SnipEngine(800, 800)