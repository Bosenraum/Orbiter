import random
import math

import engine.colors as colors
from engine.vector import Vec2

from widgets.interfaces.IDrawable import IDrawable

from spot import Spot


class Maze(IDrawable):

    def __init__(self, pos: Vec2, width, height, num_rows, num_cols, **kwargs):
        self.pos = pos
        self.width = width
        self.height = height
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.background_color = kwargs.get("background_color", colors.Grey.background_grey)
        if num_rows <= 1:
            print(f"Cannot have < 1 row! Setting to 1.")
            self.num_rows = 1

        self.spot_width = self.width / self.num_rows

        if num_cols <= 1:
            print(f"Cannot have < 1 column! Setting to 1.")
            self.num_cols = 1

        self.spot_height = self.height / self.num_cols

        self.maze = self.init_maze(self.background_color)

    def calc_neighbors(self):
        for row in self.maze:
            for spot in row:
                spot.add_neighbors(self)

    def init_maze(self, color):
        maze = []
        for i in range(self.num_rows):
            maze.append([])
            for j in range(self.num_cols):
                pos = Vec2(i, j)
                maze[i].append(Spot(pos, self.spot_width, self.spot_height, color, offset=self.pos, border_width=0))

        return maze

    def get_spot(self, row, col):
        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            return self.maze[row][col]
        return None

    def get_rand_row(self):
        return math.floor(random.random() * self.num_rows)

    def get_rand_col(self):
        return math.floor(random.random() * self.num_cols)

    def get_rand_spot(self):
        return self.get_spot(self.get_rand_row(), self.get_rand_col())

    def soft_reset(self):
        for row in self.maze:
            for spot in row:
                spot.soft_reset()

    def draw(self, screen):
        for row in self.maze:
            for spot in row:
                spot.draw(screen)