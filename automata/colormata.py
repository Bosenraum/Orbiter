import pygame
import sys
import random

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
from engine.pixel import *

from widgets.interfaces.IDrawable import IDrawable
from cell import *


class ColormataEngine(Engine):
    APP_NAME = "Colormata"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.cells = []

        pf = 10
        self.cells = generate_pixels(Cell, width, height, pf, init_state=0)
        self.row_length = int(width)
        self.col_length = int(height)
        self.num_cells = self.row_length * self.col_length
        self.num_starting_cells = int(0.2 * self.num_cells)

        self.init_cells()

        self.pause = True
        self.mouse_pos = (0, 0)

        super().__init__(width, height, pf)

    def process_key_inputs(self, ev: pygame.event.Event):
        if ev.key == pygame.K_SPACE:
            print(f"Pressed space.")
            self.pause = False

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

        if ev.key == pygame.K_ESCAPE:
            self.pause = not self.pause
            self.reset_cells()

    def process_mouse_inputs(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Mouse down events

            p = self.get_pixel(self.mouse_pos)
            p.set_color(colors.get_random_color())
            p.set()

        if ev.type == pygame.MOUSEBUTTONUP:
            # Mouse up events
            pass

        if ev.type == pygame.MOUSEWHEEL:
            # Mousewheel events
            pass

        if ev.type == pygame.MOUSEMOTION:
            # Mouse motion events
            pass

    def get_pixel(self, pos):
        x = int(pos[0] / self.pf)
        y = int(pos[1] / self.pf)
        return self.cells[x][y]

    def on_start(self):
        pass

    def init_cells(self):
        for _ in range(self.num_starting_cells):
            cell = None
            x, y = 0, 0
            while not cell or cell.state == 1:
                x = random.randint(0, self.row_length - 1)
                y = random.randint(0, self.col_length - 1)
                cell = self.cells[x][y]
            cell.set()
            cell.next_color = colors.get_random_color()
            self.cells[x][y] = cell

    def OLD_update_pixels(self):
        for x, col in enumerate(self.cells):
            for y, pixel in enumerate(col):
                if pixel.state:
                    variation = 0.1
                    r_lim = (int(pixel.on_color[0] * (1 - variation)), int(pixel.on_color[0] * (1 + variation)))
                    g_lim = (int(pixel.on_color[1] * (1 - variation)), int(pixel.on_color[1] * (1 + variation)))
                    b_lim = (int(pixel.on_color[2] * (1 - variation)), int(pixel.on_color[2] * (1 + variation)))

                    neighbors = self.get_neighbors(x, y)

                    for n in neighbors:
                        neighbor_color = colors.get_random_color(r_lim, g_lim, b_lim)
                        if not n.state:
                            n.set()
                            n.set_color(neighbor_color)
                        else:
                            n.add_color(neighbor_color)
                    pixel.kill()

    def OLD2_update_pixels(self):
        next_pixels = []
        for pixel in self.cur_pixels:
            neighbors = self.get_neighbors(self.cells, pixel.x, pixel.y)
            for n in neighbors:
                if n not in next_pixels and n.alive:
                    next_pixels.append(n)
            pixel.spread(neighbors)
            pixel.kill()

        self.cur_pixels = next_pixels
        if not self.cur_pixels:
            self.pause = True
            self.reset_pixels()

    def update_cells(self):
        for row in self.cells:
            for cell in row:
                n = self.get_neighbors(self.cells, cell.x, cell.y)
                cell.update(n)

    def reset_cells(self):
        for row in self.cells:
            for c in row:
                c.reset()

    def get_neighbors(self, cells, x, y):
        # get neighboring cells
        neighbor_count = 0
        neighbor_mask = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

        for i in range(len(neighbor_mask)):
            for j in range(len(neighbor_mask[i])):
                nx = x + i - 2
                ny = y + j - 2
                # if x == nx and y == ny:
                #     continue

                if 0 <= nx <= self.row_length - 1 and 0 <= ny <= self.col_length - 1:
                    try:
                        if neighbor_mask[i][j] and cells[nx][ny].state == 1:
                            neighbor_count += 1
                    except IndexError as ie:
                        print(f"Index error at i={i}, j={j}.")
                        print(f"x={x}, y={y}")
                        print(f"nx={nx}, ny={ny}")

        return neighbor_count

    def on_update(self, et):
        self.clock.tick(24)

        self.mouse_pos = pygame.mouse.get_pos()
        p = self.get_pixel(self.mouse_pos)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_key_inputs(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

            if event.type == pygame.JOYBUTTONDOWN:
                pass

            if event.type == pygame.JOYHATMOTION:
                pass

        if pygame.mouse.get_pressed()[0]:
            if p.state == 0:
                p.set()
                p.set_color(colors.get_random_color())

        if pygame.mouse.get_pressed()[2]:
            p.clear()

        self.screen.fill(colors.BLACK)

        self.update_cells()

        for row in self.cells:
            for cell in row:
                cell.next()
                cell.draw(self.screen)

        pygame.draw.circle(self.screen, colors.GREEN, self.mouse_pos, 5, width=1)

        pygame.display.update()


if __name__ == "__main__":
    ColormataEngine(100, 100)
