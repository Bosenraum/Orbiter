# tile_representation.py
import pygame
import math

import engine.colors as colors


class TileRepresentation:

    abs_offset = -100

    f = math.sqrt(3) / 2
    phi = 3 * math.sqrt(3) / 2

    def __init__(self, position, side_length=25, color=None, outline_color=colors.BLACK):
        self.position = position
        self.side_length = side_length  # Size of the hexagon
        self.apothem = self.side_length * self.f
        self.color = color if color else colors.get_random_color((40, 200), (40, 200), (40, 200))  # Fill color of the hexagon
        self.outline_color = outline_color  # Outline color of the hexagon
        self.do_once = True

    def draw(self, screen):
        row, col = self.position
        x_shift = self.apothem * 2 if row % 2 == 0 else 0
        x_offset = col * self.side_length * 2 * math.sqrt(3) + x_shift
        y_offset = row * self.side_length * 3


        # Calculate the vertices of the hexagon
        vertices = []
        rotation_angle = 30
        for i in range(6):
            angle_deg = 60 * i + rotation_angle
            angle_rad = math.radians(angle_deg)
            x = x_offset + self.side_length * 2 * math.cos(angle_rad) + self.abs_offset
            y = y_offset + self.side_length * 2 * math.sin(angle_rad) + self.abs_offset
            vertices.append((x, y))

        # Draw the hexagon
        pygame.draw.polygon(screen, self.color, vertices)
        pygame.draw.polygon(screen, self.outline_color, vertices, 3)


def