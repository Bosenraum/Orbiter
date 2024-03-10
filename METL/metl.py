
# The Mission Essential Task List

import math
import random

import pygame
import sys

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
import engine.snippets as snips

from tiers import *
from taskrep import CircleTaskRep
from tierrep import TierRep


class METLEngine(Engine):
    APP_NAME = "METL"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.tier_renderer = None
        self.task_renderer = None

        self.tiers = None

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
        tier_height = int(self.height / 3)

        tier_one_rep = TierRep(0, 0, colors.RED, self.width, tier_height)
        tier_two_rep = TierRep(0, tier_height, colors.BLUE, self.width, tier_height)
        tier_three_rep = TierRep(0, 2 * tier_height, colors.GREEN, self.width, tier_height)

        self.tiers = []
        self.tiers.append(Tier(None, tier_one_rep))
        self.tiers.append(Tier(self.tiers[-1], tier_two_rep))
        self.tiers.append(Tier(self.tiers[-1], tier_three_rep))

        for tier in self.tiers:
            self.generate_tasks(10, tier)

        self.tier_renderer = TierRenderer(self.screen)
        self.task_renderer = TaskRenderer(self.screen)

    def generate_tasks(self, num_tasks, tier: Tier):
        TASK_RADIUS = 10

        tier_rect = tier.tier_rep.get_rect()
        tier_w = tier_rect[2]
        tier_h = tier_rect[3]
        start_x = int(tier.tier_rep.x + TASK_RADIUS)
        start_y = int(tier.tier_rep.y + (tier_h / 2))

        for n in range(num_tasks):
            taskrep = CircleTaskRep(start_x + (2 * n * TASK_RADIUS), start_y, colors.WHITE, TASK_RADIUS)
            task = Task(f"Task{n:02d}", tier, taskrep)
            tier.add_task(task)

    def on_start(self):
        self.reset()

    def draw_sim(self):
        # Draw start/end
        for tier in self.tiers:
            # self.tier_renderer.draw_tier(tier)
            # self.task_renderer.draw_tasks(tier.get_tasks())
            tier.tier_rep.draw(self.screen)
            for task in tier.get_tasks():
                task.task_rep.draw(self.screen)

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
    METLEngine(1200, 1200)
