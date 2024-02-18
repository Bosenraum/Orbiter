import pygame

from interfaces.IDrawable import IDrawable


# An individual drawable particle
# Can have a custom shape/color/size/scaling/ect.
class Particle(IDrawable):

    def __init__(self, color, scale_factor, **kwargs):
        self.color = color
        self.scale_factor = scale_factor

    def draw(self, screen):
        pass


class CircleParticle(Particle):

    def __init__(self, color, scale_factor, **kwargs):
        super().__init__(color, scale_factor, **kwargs)

        self.radius = kwargs.get("radius", 1)
        self.physics = kwargs.get("physics")

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos)