
import pygame
from tiers import Representation


class CircleTaskRep(Representation):

    def __init__(self, x, y, color, r):
        super().__init__(x, y, color)
        self.r = r

    def get_rect(self):
        return self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r

    def draw(self, screen):
        center = (self.x, self.y)
        pygame.draw.circle(screen, self.color, center, self.r)
