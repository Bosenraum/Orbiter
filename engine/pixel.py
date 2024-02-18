import pygame
import engine.colors as colors


class Pixel:

    def __init__(self, x, y, **kwargs):

        self.x = x
        self.y = y
        self.sf = kwargs.get("scale_factor", 1)

        # pygame Rect objects use x, y, width, height, so specify our pixel coordinates and the pixel width/height
        self.rect = pygame.Rect(self.x * self.sf, self.y * self.sf, self.sf, self.sf)
        self.state = kwargs.get("init_state", 0)
        self.on_color = kwargs.get("on_color", colors.WHITE)
        self.off_color = kwargs.get("off_color", colors.BLACK)

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
        pygame.draw.rect(screen, self.on_color if self.state else self.off_color, self.rect)


def generate_pixels(T, width, height, pf, **kwargs):
    init_state = kwargs.get("init_state", 0)
    on_color = kwargs.get("on_color", colors.WHITE)
    off_color = kwargs.get("off_color", colors.BLACK)

    pixels = []
    for w in range(width):
        pixels.append([])
        for h in range(height):
            pixels[w].append(T(w, h, off_color=off_color, on_color=on_color, scale_factor=pf, init_state=init_state))
    return pixels
