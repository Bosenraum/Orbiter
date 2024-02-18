import pygame
import pygame.gfxdraw

import math

import engine.colors as colors
from engine.vector import Vec2
from engine.utils import in_ball

import json
from widgets.interfaces.ISerializable import ISerializable
from widgets.interfaces.IDrawable import IClickable


class Dial(ISerializable, IClickable):

    def __init__(self, xpos=0, ypos=0, radius=1, low=0, high=100, color=colors.WHITE):
        self.x = xpos
        self.y = ypos
        self._pos = Vec2(self.x, self.y)
        self.radius = radius
        self.min = low
        self.max = high
        self.color = color
        self._value = self.min

    def serialize(self):
        # Return a json serializable version of the object
        attributes = {
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
            "min": self.min,
            "max": self.max,
            "color": str(self.color),
            "value": self.value
        }
        root = {
            "type": "dial",
            "attributes": attributes
        }
        return root

    def deserialize(self, attrs):
        if isinstance(attrs, str):
            attrs = json.loads(attrs)
        if not isinstance(attrs, dict):
            print(f"Cannot deserialize {type(attrs)}")
            return

        # attrs = root.get("attributes", {})
        self.x = attrs.get("x", 0)
        self.y = attrs.get("y", 0)
        self.radius = attrs.get("radius", 1)
        self.min = attrs.get("min", 0)
        self.max = attrs.get("max", 100)
        color_str = attrs.get("color", str(colors.WHITE))
        self.color = colors.str_to_color(color_str)
        self.value = attrs.get("value", self.min)

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

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, x, y=None):
        if isinstance(x, Vec2):
            y = x.y
            x = x.x
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            pass
        else:
            print(f"Cannot set position to x={x} (type={type(x)}")
            if y:
                print(f"y={y} (type={type(y)}")
            return

        self._pos.x = x
        self._pos.y = y
        self.x = x
        self.y = y

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
            pygame.gfxdraw.pie(screen, self.x, self.y, self.radius-i, -90, int(angle_deg - 90), self.color)

    def check_intersect(self, mouse_pos):
        in_ball(self.pos, mouse_pos, self.radius)
