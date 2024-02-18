import pygame.gfxdraw
import pygame.draw

from widgets.interfaces import IDrawable
import engine.colors as colors
from engine.vector import Vec2

USE_GFX = True
draw_module = pygame.gfxdraw if USE_GFX else pygame.draw


class ShapeWidget:

    def __init__(self, pos: Vec2, *args, **kwargs):
        self.pos = pos

    def draw(self, screen):
        pass