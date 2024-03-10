import pygame
from tiers import Representation


class TierRep(Representation):

    def __init__(self, x, y, color, w, h):
        super().__init__(x, y, color)
        self.w = w
        self.h = h

    def get_rect(self):
        return self.x, self.y, self.w, self.h

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())
