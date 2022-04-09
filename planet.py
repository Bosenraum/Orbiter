import pygame
import random

from vector import *
from colors import *

G = 1e-6


class Planet:

    def __init__(self, name: str, radius, position: Vec2, **kwargs):

        velocity = kwargs.get("velocity", Vec2(0, 0))
        acceleration = kwargs.get("acceleration", None)
        thickness = kwargs.get("thickness", 5)
        mass = kwargs.get("mass", 1e6)
        color = kwargs.get("color", WHITE)
        fill = kwargs.get("fill", False)
        num_rings = kwargs.get("num_rings", 0)
        core = kwargs.get("core", BLACK)

        self.name = name
        self.radius = abs(radius)
        self.position = position
        self.velocity = velocity if velocity else NULL_VECTOR
        self.acceleration = acceleration if acceleration else NULL_VECTOR
        self.thickness = 0 if fill else thickness
        self.mass = mass
        self.color = color
        self.num_rings = num_rings
        self.core = core

    # Draw the planet to the given screen
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.get(), self.radius, self.thickness)
        # pygame.draw.circle(screen, self.color, (self.position.x + (2 * self.radius), self.position.y), self.radius, self.thickness)
        radius = self.radius
        i = 1

        r = self.color[0]
        g = self.color[1]
        b = self.color[2]

        num_rings = self.num_rings
        j = 1.1

        for i in range(num_rings):
            pygame.draw.circle(screen, color_span(self.core, self.color, i, num_rings), self.position.get(), self.radius/(j**i), math.ceil(int(
                    self.radius/num_rings)) ** 3)

        # for i in range(num_rings):
        #     radius = radius // 2
        #     # r = ((r * random.randint(2, 3)) + 10) % 255
        #     # g = ((b + random.randint(10, 20)) * 6) % 255
        #     # b = (g + r) * random.randint(8, 16) % 255
        #     r = (r + (i-1 * 10)) % 255
        #     g = (g + (i-1 * 20)) % 255
        #     b = (b + (1-1 * 30)) % 255
        #     pygame.draw.circle(screen, (r, g, b), self.position.get(), self.radius/(j**i), 1)

    def accel(self, accel_vec):
        self.acceleration.x += accel_vec.x
        self.acceleration.y += accel_vec.y

    def update(self, dt):
        self.position.x = self.acceleration.x * 0.5 * dt ** 2 + self.velocity.x * dt + self.position.x
        self.velocity.x = self.acceleration.x * dt + self.velocity.x

        self.position.y = self.acceleration.y * 0.5 * dt ** 2 * self.velocity.y * dt + self.position.y
        self.velocity.y = self.acceleration.y * dt * self.velocity.y

