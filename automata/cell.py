from engine.colors import *
from engine.pixel import *
from engine.vector import Vec2


class Cell(Pixel):

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)
        self.next_color = self.on_color
        self.next_state = self.state
        self.alive = True

    def add_color(self, color):
        self.next_color = colors.blend(self.next_color, color)

    def update_color(self):
        self.on_color = self.next_color

    def kill(self):
        self.off_color = self.on_color
        self.alive = False
        self.state = 0

    def set(self):
        if self.alive:
            self.state = 1

    def reset(self):
        self.alive = True
        self.state = 0

    def update(self, on_neighbors):
        self.next_color = colors.get_random_color()
        if self.state:
            if on_neighbors == 2 or on_neighbors == 3:
                self.next_state = 1
            else:
                self.next_state = 0
        else:
            if on_neighbors == 3:
                self.next_state = 1

    def next(self):
        self.state = self.next_state
        self.on_color = self.next_color

    def get_center(self):
        return Vec2(self.x + (self.sf * 0.5), self.y + (self.sf * 0.5))