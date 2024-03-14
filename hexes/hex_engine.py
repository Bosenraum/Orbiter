import math
import random

import pygame
import sys

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
import engine.snippets as snips

from hexgrid import *
from hexgraph import *
from tile_representation import GlobalTileProperties

from widgets.dial import Dial

from states.game_input import GameInput
from states.state_machine import StateMachine
from states.menu_state import MenuState

"""
A brief aside on coding with AI tools.

I wrote a good chunk of this program using ChatCPT. This included thinking through the design process,
and translating those ideas into code. What I found was, there was plenty for me to do. I was more
focused on solving problems than on writing code. The AI generated large chunks of code, design 
documentation, product requirements, all at my direction. I improved them, refined them, then translated
them back into a larger project. Surely in time this will improve as well, and I'll be needed far less
on the mechanical side of the work, that is, writing the code by hand, making things compile by subtle
tweaks, adjusting the math when the language model doesn't understand math like humans do. But the 
problem is mine. I'm part of the solution by bringing the problem. 

Anyways, it reminded me of the industrial revolution removing the need for many workers doing strictly
physical tasks as part of a larger process. And later, the automation of car manufacturing with
assembly robots. There are still humans involved in that process, but it takes far fewer humans
to do the same amount of work. Those displaced humans can become the one running the robots, and
the solution scales because of the technical advancement. Suddenly GM can manufacture 10x more
cars or for 10% of what they previously cost, or both. The tool is a force multiplier.

AI is that same force multiplier for knowledge work. If Google was
moving from hand-crafted to an assembly line, ChatGPT is an assembly robot. It does the hard, 
tedious bits for you, while you focus on design. Design gets better as a result. 

I think it's called the 'tipping point', or maybe I just call it that. The point where we 
redirect that output at itself. As we are want to do. We use the tool to make itself better.
Heck, we did it with the assembly robots. Automated assembly of bots made designs get better,
made bots get better, which improved designs, then bots, and on and on... So with AI. We've 
eclipsed ourselves physically long ago, now we'll eclipse ourselves mentally. In the end,
the victory is man's. 

We're capable of building things.
Far bigger than ourselves.

"""


class HexEngine(Engine):
    APP_NAME = "HexEngine"
    CLOCK_TICK = 0

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.hexgrid = None
        self.hexgraph = None

        self.use_grid = True
        self.mouse_down = None
        self.mouse_pos = None
        self.click_pos = None

        self.init_offset = None
        self.invert_x = 1
        self.invert_y = 1

        self.dial_radius = None
        self.active_dial_pos = None

        self.clicked_tile = None
        self.last_clicked_tile = None

        self.game_input = None
        self.state_machine = None

        self.grid_surface = None
        self.ribbon_surface = None
        self.debug_surface = None

        self.do_once = True

        self.seed = 43

        pf = 1
        super().__init__(width, height, pf)

    def process_keydown_inputs(self, ev: pygame.event.Event):
        if self.debug:
            # print(f"[KEY {ev.key}]")
            pass

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

        if ev.key == pygame.K_F3:
            GlobalTileProperties.debug = not GlobalTileProperties.debug

        if ev.key == pygame.K_F4:
            self.do_once = True

        if ev.key == pygame.K_x:
            self.invert_x *= -1

        if ev.key == pygame.K_y:
            self.invert_y *= -1

        if ev.key == pygame.K_a:
            self.seed -= 1
            self.reset()

        if ev.key == pygame.K_d:
            self.seed += 1
            self.reset()

        if ev.key == pygame.K_w:
            self.seed += 10
            self.reset()

        if ev.key == pygame.K_s:
            self.seed -= 10
            self.reset()

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
                print(f"M3 Clicked!")
                # self.click_pos = self.mouse_pos
                # self.ocean_dial_active = self.ocean_dial.check_intersect(self.mouse_pos)
                # self.beach_dial_active = self.beach_dial.check_intersect(self.mouse_pos)

            if m2:
                self.mouse_down = True
                self.click_pos = self.mouse_pos
                self.init_offset = self.hexgrid.get_offset()

            if m1:

                if self.clicked_tile:
                    clicked_rep = TileRepresentation(self.clicked_tile.position, color=colors.BLACK)
                    self.clicked_tile.set_representation(clicked_rep)
                    self.clicked_tile.draw(self.grid_surface)

                    # for n in self.clicked_tile.get_neighbors():
                    for n in self.hexgrid.get_neighbors(self.clicked_tile, depth=1):
                        neighbor_rep = TileRepresentation(n.position, color=colors.WHITE)
                        n.set_representation(neighbor_rep)
                        n.draw(self.grid_surface)

        if ev.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = m1

        if ev.type == pygame.MOUSEWHEEL:
            # Mousewheel events
            self.hexgrid.zoom(ev.y)

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
        # self.grid_surface = pygame.surface.Surface((self.width, self.height - 200))
        self.grid_surface = self.screen.subsurface((0, 150, self.width, self.height - 200))
        self.ribbon_surface = self.screen.subsurface(0, 0, self.width, 150)
        # self.debug_surface = self.screen.subsurface((0, self.height - 100, self.width, 200))

        if self.use_grid:
            self.hexgrid = HexGrid(self.grid_surface.get_offset(), 50, 50, clip_plane=self.grid_surface.get_size(), seed=self.seed)
        else:
            self.hexgraph = HexGraph(40)

        self.mouse_down = False
        self.click_pos = (0, 0)
        self.init_offset = (0, 0)

        self.dial_radius = 50

        self.game_input = GameInput()
        self.state_machine = StateMachine(self.screen, self.game_input)
        self.state_machine.set_next_state(MenuState("Main Menu"))

    def on_start(self):
        self.reset()

    def draw_info(self):
        debug_width = 200
        debug_height = 100
        debug_rect = pygame.rect.Rect(0, 0, debug_width, debug_height)
        debug_surface = pygame.surface.Surface((debug_width, debug_height), pygame.SRCALPHA)

        bg_color = colors.get_gray(40)
        border_color = colors.get_gray(215)
        pygame.draw.rect(debug_surface, bg_color, debug_rect)
        pygame.draw.rect(debug_surface, border_color, debug_rect, width=4)

        gtp_properties = GlobalTileProperties.get_properties()

        x_pad = 10
        y_pad = 4

        info_font = pygame.freetype.SysFont(["consolas"], 14)
        font_color = colors.WHITE
        text_pos = [x_pad, x_pad]
        for key, value in gtp_properties.items():
            if isinstance(value, float):
                value = round(value, 4)
            img, img_rect = info_font.render(f"{key}: {value}", font_color, bg_color)
            debug_surface.blit(img, text_pos)
            text_pos[1] += img_rect.y + y_pad

        img, img_rect = info_font.render(f"FPS: {round(self.fps)}", font_color, bg_color)
        debug_surface.blit(img, text_pos)

        self.screen.blit(debug_surface, (10, self.height - debug_surface.get_height() - 10))

    def draw_debug(self):
        if self.debug:
            self.draw_info()

    def draw_sim(self):
        # Draw start/end
        if self.use_grid:
            self.hexgrid.draw(self.grid_surface)
        else:
            self.hexgraph.draw(self.screen)

        pygame.draw.rect(self.ribbon_surface, colors.Red.end_red, self.ribbon_surface.get_rect(), width=10)
        # self.screen.blit(self.grid_surface, (0, 200))

    def run_sim(self):

        if self.mouse_down:
            # offset the grid by the delta between where the mouse was clicked and where the mouse is now
            delta_x = self.mouse_pos[0] - self.click_pos[0] + self.init_offset[0]
            delta_y = self.mouse_pos[1] - self.click_pos[1] + self.init_offset[1]
            delta_pos = self.invert_x * delta_x, self.invert_y * delta_y
            self.hexgrid.move(delta_pos)

    def on_update(self, et):
        m1, m2, m3 = pygame.mouse.get_pressed(3)
        self.mouse_pos = pygame.mouse.get_pos()

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
        self.draw_debug()
        # self.state_machine.step()

        pygame.display.update()


if __name__ == "__main__":
    HexEngine(1200, 1200, debug=True)
