import copy
import json

import easygui
import pygame
import sys
import random

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
from engine.tracer import Tracer

from input_context import *


class TextTracer(Tracer):

    def __init__(self, color, max_length, font):
        self.font = font
        super().__init__(color, max_length, end_color=colors.WHITE)

    # Data will be a 3-tuple of ('string', x, y)
    def trace(self, screen):
        for i, data in enumerate(self.data):
            text, x, y = data
            img, img_rect = self.font.render(text, True, self.calc_color(i))
            screen.blit(img, (x, y))


class AdventureTypeEngine(Engine):
    APP_NAME = "Adventure Type"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", True)

        self.input_context = TypingContext()
        self.cur_string = ""
        self.text_pos = Vec2(width//2, height//2)

        self.game_font = None
        self.text_tracer = None

        self.pause = True
        self.mouse_pos = (0, 0)

        self.active_words = ["Test", "word", "CAPS", "weather", "cats"]

        pf = 1
        super().__init__(width, height, pf)

    def process_keydown(self, ev: pygame.event.Event):
        if ev.key == pygame.K_F1:
            self.debug = not self.debug
            return

        if ev.key == pygame.K_ESCAPE:
            self.pause = not self.pause
            return

        if ev.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.input_context.capitalize = True
            return

        if ev.key == pygame.K_RETURN:
            print(f"Saving {self.cur_string} to the Text Tracer")
            self.text_tracer.append((self.cur_string, self.text_pos.x, self.text_pos.y))
            self.input_context.clear()
            self.cur_string = ""
            return

        if self.debug:
            print(f"Unicode: {ev.unicode}")
        self.cur_string = self.input_context.process(ev)

    # def process_keyup(self, ev: pygame.event.Event):
    #     if ev.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
    #         self.input_context.capitalize = Falseust

    def process_mouse_inputs(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Mouse down events
            self.text_pos = Vec2(self.mouse_pos)
            pass

        if ev.type == pygame.MOUSEBUTTONUP:
            # Mouse up events
            pass

        if ev.type == pygame.MOUSEWHEEL:
            # Mousewheel events
            pass

        if ev.type == pygame.MOUSEMOTION:
            # Mouse motion events
            pass

    def draw_string(self, s, pos, color=colors.WHITE, font=Engine.debug_font):
        # Only draw the string if the position is on the screen
        # TODO: need to check to see if any part of the text would be rendered
        if (0 <= pos.x <= self.screen.get_width()) and (0 <= pos.y <= self.screen.get_height()):
            # font.render_to(self.screen, pos, s, color)
            # if s:
            #     padding = Vec2(2, 2)
            #     text_size = Vec2(self.debug_font.size(s)) + padding
            #     text_background = pygame.rect.Rect(pos.x - (padding.x // 2), pos.y - (padding.y // 2), text_size.x, text_size.y)
            #     pygame.draw.rect(self.screen, colors.coral_red, text_background)
            self.draw_debug(s, color, pos.x, pos.y)

    def on_start(self):
        self.game_font = pygame.freetype.SysFont("lucidabright", 20)
        self.text_tracer = TextTracer(colors.vivid_cerulean, 100, self.game_font)

    def on_update(self, et):
        self.clock.tick(24)

        self.mouse_pos = pygame.mouse.get_pos()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_keydown(event)

            # if event.type == pygame.KEYUP:
            #     self.process_keyup(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

            if event.type == pygame.JOYBUTTONDOWN:
                pass

            if event.type == pygame.JOYHATMOTION:
                pass

        self.screen.fill(colors.BLACK)

        self.text_tracer.trace(self.screen)
        self.draw_string(self.cur_string, self.text_pos)

        pygame.display.update()


if __name__ == "__main__":
    AdventureTypeEngine(1000, 1000)
