import math
import random

import pygame
import sys

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
import engine.snippets as snips

from maze import Maze
from spot import Spot, SpotMarker


class AStarEngine(Engine):
    APP_NAME = "A*"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.stepping_enabled = True
        self.step = False
        self.step_number = None
        self.win = None
        self.fail = None

        self.maze = None
        self.player_pos = None
        self.player_radius = None
        self.player_color = None

        # Things that should still be evaluated
        self.open_set = None
        self.open_set_markers = None

        # Things that no longer need to be evaluated
        self.closed_set = None
        self.closed_set_markers = None

        # Important spots to track
        self.starting_spot = None
        self.starting_spot_marker = None
        self.ending_spot = None
        self.ending_spot_marker = None
        self.current_spot = None
        self.current_spot_marker = None

        self.click_spot = None
        self.click_spot_maker = None

        self.paint = None
        self.paint_type = None

        self.last_hat_value = None
        self.hat_input = [0, 0]

        pf = 1
        super().__init__(width, height, pf)

    def process_keydown_inputs(self, ev: pygame.event.Event):
        if ev.key == pygame.K_SPACE:
            print(f"Pressed space.")

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

        if ev.key == pygame.K_SPACE:
            self.on_start()

        # Step the simulation
        if ev.key == pygame.K_f:
            self.step = True

        # Toggle stepping the simulation
        if ev.key == pygame.K_s:
            self.stepping_enabled = not self.stepping_enabled

        # Clear 'click_spot'
        if ev.key == pygame.K_c:
            self.click_spot = None

        # Reset the current maze setup to re-run the algorithm
        if ev.key == pygame.K_r:
            self.reset_current()

    def get_mouse_spot(self):
        mouse_pos = Vec2(pygame.mouse.get_pos())
        rel_mouse_pos = mouse_pos - self.maze.pos
        maze_spot = self.maze.get_spot(int(rel_mouse_pos.x / self.maze.spot_width),
                                       int(rel_mouse_pos.y / self.maze.spot_height))
        return maze_spot

    def process_mouse_inputs(self, ev: pygame.event.Event):
        m1, m2, m3 = pygame.mouse.get_pressed(3)
        maze_spot = self.get_mouse_spot()
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # Mouse down events
            if m3:
                self.click_spot = maze_spot
                print(f"{self.click_spot.f=}")

            if m1:
                # Toggle obstacle
                self.paint = True
                self.paint_type = not maze_spot.walkable

        if ev.type == pygame.MOUSEBUTTONUP:
            # Mouse up events
            if m1:
                self.paint = False

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
            print(ev)
            x, y = ev.value
            if ev.value != (0, 0):
                self.hat_input[0] = x if x else self.hat_input[0]
                self.hat_input[1] = y if y else self.hat_input[1]
            else:
                self.player_pos.x += self.hat_input[0]
                self.player_pos.y += self.hat_input[1] * -1
                if self.player_pos.x < 0:
                    self.player_pos.x = 0
                elif self.player_pos.x >= self.maze.num_cols:
                    self.player_pos.x = self.maze.num_cols - 1

                if self.player_pos.y < 0:
                    self.player_pos.y = 0
                elif self.player_pos.y >= self.maze.num_rows:
                    self.player_pos.y = self.maze.num_rows - 1
                self.hat_input = [0, 0]

    def reset_current(self):
        self.step_number = 0
        self.win = False
        self.fail = False

        self.starting_spot.g = 0

        # Things that should still be evaluated
        self.open_set = set()
        self.open_set_markers = []

        # Things that no longer need to be evaluated
        self.closed_set = set()
        self.closed_set_markers = []
        self.open_set.add(self.starting_spot)

        self.paint = False
        self.paint_type = False  # Set walkable to 'False'

        self.maze.calc_neighbors()

    def on_start(self):
        cols = 20
        rows = 20
        start_marker_color = colors.Blue.start_blue
        end_marker_color = colors.Red.end_red
        margin = 0.1
        spot_width = self.width * (1 - margin) // cols
        spot_height = self.height * (1 - margin) // rows
        spot_size = Vec2(spot_width, spot_height)
        w = spot_size.x * cols
        h = spot_size.y * rows
        self.maze = Maze(Vec2(int(self.width * margin / 2), int(self.height * margin / 2)), w, h, rows, cols)

        self.starting_spot = self.maze.get_rand_spot()

        self.starting_spot_marker = SpotMarker(self.starting_spot, start_marker_color, radius_multiplier=0.8)
        self.ending_spot = self.starting_spot
        while self.ending_spot == self.starting_spot:
            # self.ending_spot = self.search_maze.get_rand_spot()
            self.ending_spot = self.maze.get_spot(self.maze.num_rows - 1, self.maze.num_cols - 1)
            self.ending_spot_marker = SpotMarker(self.ending_spot, end_marker_color, radius_multiplier=0.8)

        self.reset_current()

    def draw_sim(self):
        # Draw start/end
        if self.starting_spot_marker:
            self.starting_spot_marker.draw(self.screen)
        if self.ending_spot_marker:
            self.ending_spot_marker.draw(self.screen)

        # Draw open/closed set
        for spot_mark in self.open_set_markers:
            spot_mark.draw(self.screen)

        for spot_mark in self.closed_set_markers:
            if self.fail:
                spot_mark.draw(self.screen, override_color=colors.Red.failure_red)

        if self.click_spot:
            SpotMarker(self.click_spot, colors.Blue.violet_blue, radius_multiplier=0.25).draw(self.screen)

            # Draw some neighbors
            for n in self.click_spot.neighbors:
                SpotMarker(n, colors.Blue.vivid_cerulean, radius_multiplier=0.2).draw(self.screen)

        # Draw current
        if self.current_spot_marker:
            self.current_spot_marker.draw(self.screen)

        if self.win:
            spot = self.ending_spot
            n = 0
            while spot != self.starting_spot and n < self.step_number:
                color = snips.get_gr_sample(n)
                SpotMarker(spot, colors.Blue.electric_blue, radius_multiplier=0.6).draw(self.screen)
                if spot:
                    spot = spot.parent
                else:
                    break

    def run_sim(self):
        # run the algorithm every frame
        # open_set has the starting Spot
        if self.win or self.fail:
            return

        self.step_number += 1

        if len(self.open_set) > 0:
            winner_spot = None

            for spot in self.open_set:
                if winner_spot:
                    if spot.f < winner_spot.f:
                        winner_spot = spot
                else:
                    winner_spot = spot

                # Create SpotMarker for each spot in the open_set
                self.open_set_markers.append(SpotMarker(spot, colors.Green.open_set_green, radius_multiplier=0.3))

            self.current_spot = winner_spot
            self.current_spot_marker = SpotMarker(self.current_spot, colors.Yellow.player_yellow, radius_multiplier=0.2)

            if self.current_spot == self.ending_spot:
                # Found the end, WIN
                print(f"You win! ({self.step_number})")
                self.win = True

            self.open_set.remove(self.current_spot)
            self.closed_set.add(self.current_spot)

            # Get neighbors of current
            for neighbor in self.current_spot.neighbors:
                if not neighbor.walkable or neighbor in self.closed_set:
                    continue

                tentative_g = self.current_spot.g + (self.current_spot.pos.distance(neighbor.pos))

                if tentative_g < neighbor.g:
                    # This is the shortest path so far
                    neighbor.parent = self.current_spot
                    neighbor.g = tentative_g
                    neighbor.f = tentative_g + self.heuristic(neighbor, self.ending_spot)

                    if neighbor not in self.open_set:
                        self.open_set.add(neighbor)

        else:
            print(f"No solution!")
            self.fail = True
            # No solution

        if len(self.closed_set) > 0:
            for spot in self.closed_set:
                self.closed_set_markers.append(SpotMarker(spot, colors.Purple.closed_set_purple, radius_multiplier=0.5))

    def heuristic(self, spot_a, spot_b):
        h_dist = int(10 * spot_a.pos.distance(spot_b.pos))
        # print(f"Calculated H = {h_dist} for Spot({spot_a.pos.get()})")
        return h_dist

    def on_update(self, et):
        self.step = not self.stepping_enabled
        m1, m2, m3 = pygame.mouse.get_pressed(3)
        maze_spot = self.get_mouse_spot()

        if m1:
            if maze_spot.walkable != self.paint_type:
                maze_spot.walkable = self.paint_type

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

        self.screen.fill(colors.BLACK)
        self.maze.draw(self.screen)

        if self.step:
            if not self.win:
                print(f"Starting step {self.step_number + 1}")
            self.run_sim()

        self.draw_sim()
        pygame.display.update()


if __name__ == "__main__":
    AStarEngine(800, 800)
