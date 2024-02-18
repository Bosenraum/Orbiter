import pygame
import sys

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2

from widgets.interfaces.IDrawable import IDrawable


class Spot(IDrawable):

    def __init__(self, pos: Vec2, width, height, color, border_width=0):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.rect.Rect(self.pos.x, self.pos.y, self.width, self.height), self.border_width)

    def get_center(self):
        return Vec2(self.pos.x + (self.width * 0.5), self.pos.y + (self.height * 0.5))


class Maze(IDrawable):

    def __init__(self, pos: Vec2, width, height, num_rows, num_cols):
        self.pos = pos
        self.width = width
        self.height = height
        self.num_rows = num_rows
        self.num_cols = num_cols
        if num_rows <= 1:
            print(f"Cannot have < 1 row! Setting to 1.")
            self.num_rows = 1

        self.spot_width = self.width / self.num_rows

        if num_cols <= 1:
            print(f"Cannot have < 1 column! Setting to 1.")
            self.num_cols = 1

        self.spot_height = self.height / self.num_cols

        self.maze = self.init_maze()

    def init_maze(self):
        maze = []
        for i in range(self.num_rows):
            maze.append([])
            for j in range(self.num_cols):
                pos = Vec2(i * self.spot_width, j * self.spot_height) + self.pos
                color = colors.dark_green if (i % 2 == 0 and (j + 1) % 2 == 0) or ((i + 1) % 2 == 0 and j % 2 == 0) else colors.alabaster
                maze[i].append(Spot(pos, self.spot_width, self.spot_height, color, border_width=0))

        return maze

    def get_spot(self, row, col):
        return self.maze[row][col]

    def draw(self, screen):
        for row in self.maze:
            for spot in row:
                spot.draw(screen)


class MazeEngine(Engine):
    APP_NAME = "Maze"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.maze = None
        self.player_pos = None
        self.player_radius = None
        self.player_color = None

        self.last_hat_value = None
        self.hat_input = [0, 0]

        pf = 1
        super().__init__(width, height, pf)

    def process_key_inputs(self, ev: pygame.event.Event):
        if ev.key == pygame.K_SPACE:
            print(f"Pressed space.")

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

    def process_mouse_inputs(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Mouse down events
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

    def on_start(self):
        spots_per_row = 8
        spots_per_col = 8
        spot_size = Vec2(50, 50)
        w = spot_size.x * spots_per_col
        h = spot_size.y * spots_per_row
        self.maze = Maze(Vec2(50, 50), w, h, spots_per_row, spots_per_col)

        self.player_pos = Vec2(0, 0)
        self.player_radius = min(spot_size.x, spot_size.y) * 0.75 * 0.5
        self.player_color = colors.vivid_cerulean

    def on_update(self, et):

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
                if event.button == 6:
                    sys.exit()

            if event.type == pygame.JOYHATMOTION:
                print(event)
                x, y = event.value
                if event.value != (0, 0):
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

        self.screen.fill(colors.BLACK)
        self.maze.draw(self.screen)

        player_spot = self.maze.get_spot(*self.player_pos.get())
        pygame.draw.circle(self.screen, self.player_color, player_spot.get_center().get(), self.player_radius)

        pygame.display.update()


if __name__ == "__main__":
    MazeEngine(500, 500)
