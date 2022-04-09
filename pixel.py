import pygame
import colors


class Pixel:

    def __init__(self, x, y, on_color=colors.WHITE, scale_factor=1):
        self.x = x
        self.y = y
        self.sf = scale_factor
        # pygame Rect objects use x, y, width, height, so specify our pixel coordinates and the pixel width/height
        self.rect = pygame.Rect(self.x * self.sf, self.y * self.sf, self.sf, self.sf)
        self.state = 0  # initialize to black
        self.on_color = on_color

    def set(self):
        self.state = 1

    def clear(self):
        self.state = 0

    def toggle(self):
        self.state = not self.state

    def set_color(self, color):
        self.on_color = color

    def draw(self, screen):
        self.rect = pygame.Rect(self.x * self.sf, self.y * self.sf, self.sf, self.sf)
        pygame.draw.rect(screen, self.on_color if self.state else colors.BLACK, self.rect)