import math
import random

import pygame
import sys

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
import engine.snippets as snips

from hexgrid import *


class HexEngine(Engine):
    APP_NAME = "HexEngine"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.hexgrid = None


        pf = 1
        super().__init__(width, height, pf)

    def process_keydown_inputs(self, ev: pygame.event.Event):
        if self.debug:
            print(f"[KEY {ev.key}]")

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

        if ev.key == pygame.K_SPACE:
            self.reset()

        # Reset the current maze setup to re-run the algorithm
        if ev.key == pygame.K_r:
            self.reset()

    def process_mouse_inputs(self, ev: pygame.event.Event):
        m1, m2, m3 = pygame.mouse.get_pressed(3)
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # Mouse down events
            if m3:
                pass

            if m1:
                pass

        if ev.type == pygame.MOUSEBUTTONUP:
            pass

        if ev.type == pygame.MOUSEWHEEL:
            # Mousewheel events
            pass

        if ev.type == pygame.MOUSEMOTION:
            # Mouse motion events
            pass

    def process_joystick_inputs(self, ev: pygame.event.Event):
        if ev.type == pygame.JOYBUTTONDOWN:
            if ev.button == 6:
                sys.exit()

        if ev.type == pygame.JOYHATMOTION:
            pass

    def reset(self):
        self.hexgrid = HexGrid(20, 20)

    def on_start(self):
        self.reset()

    def draw_sim(self):
        # Draw start/end
        self.hexgrid.draw(self.screen)

    def run_sim(self):
        # run the algorithm every frame
        # open_set has the starting Spot
        pass

    def on_update(self, et):
        m1, m2, m3 = pygame.mouse.get_pressed(3)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_keydown_inputs(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

            self.process_joystick_inputs(event)

        self.screen.fill(colors.outer_space)

        self.run_sim()

        self.draw_sim()
        pygame.display.update()


if __name__ == "__main__":
    HexEngine(1200, 1200)
