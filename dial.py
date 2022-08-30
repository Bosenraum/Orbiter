import pygame
import pygame.gfxdraw

import math

from colors import *


class Dial:

    def __init__(self, xpos, ypos, radius, low=0, high=100, color=WHITE):
        self.x = xpos
        self.y = ypos
        self.radius = radius
        self.min = low
        self.max = high
        self.color = color
        self._value = self.min

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v > self.max:
            self._value = self.max
        elif v < self.min:
            self._value = self.min
        else:
            self._value = v

    def inc(self, value):
        self.value += value

    def reset(self):
        self.value = self.min

    def set(self, value):
        self.value = value

    def draw(self, screen):
        # Draw outer circle
        pygame.gfxdraw.circle(screen, self.x, self.y, self.radius, self.color)

        # Get the angle from vertical (in radians)
        angle = 2 * math.pi * self.value / self.max
        angle_deg = 360 * self.value / self.max

        if angle > math.pi:
            x2 = self.x - self.radius * math.sin(angle - math.pi)
            y2 = self.y + self.radius * math.cos(angle - math.pi)
        else:
            x2 = self.x + self.radius * math.sin(angle)
            y2 = self.y - self.radius * math.cos(angle)

        # Draw the dial line at the correct position
        # pygame.gfxdraw.line(screen, self.x, self.y, int(x2), int(y2), BLACK)

        # Draw an arc sweeping out the angle
        for i in range(self.radius):
            pygame.gfxdraw.pie(screen, self.x, self.y, self.radius-i, -90, int(angle_deg - 90), RED)

