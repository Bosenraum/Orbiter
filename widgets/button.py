import pygame
import pygame.gfxdraw
import pygame.draw

from engine.colors import *
from engine.vector import Vec2

import json
from widgets.interfaces.ISerializable import ISerializable
from widgets.interfaces.IDrawable import IClickable


class Button(ISerializable, IClickable):

    def __init__(self, text="", xpos=0, ypos=0, width=1, height=1, callback=None, shape="rect", color=WHITE, **kwargs):
        self.text = text
        self.x = xpos
        self.y = ypos
        self._pos = Vec2(self.x, self.y)
        self.height = height
        self.width = width
        self.shape = shape
        self.callback = callback
        self.color = color
        self.border_width = kwargs.get("border_width", 1)
        super().__init__()

    def serialize(self):
        # Return a pickle serializable version of the object
        attributes = {
            "text": self.text,
            "x": self.x,
            "y": self.y,
            "shape": self.shape,
            "height": self.height,
            "width": self.width,
            "callback": self.callback,
            "color": str(self.color),
            "border_width": self.border_width
        }
        root = {
            "type": "button",
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
        self.text = attrs.get("text", "DeserErr")
        self.x = attrs.get("x", 0)
        self.y = attrs.get("y", 0)
        self.shape = attrs.get("shape", "rect")
        self.height = attrs.get("height", 1)
        self.width = attrs.get("width", 1)
        self.callback = attrs.get("callback", None)
        color_str = attrs.get("color", str(WHITE))
        self.color = str_to_color(color_str)
        self.border_width = attrs.get("border_width")

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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.rect.Rect(self.x, self.y, self.width, self.height))
        # pygame.gfxdraw.filled_polygon(screen,
        #                               (
        #                                   (self.x, self.y),
        #                                   (self.x + self.width, self.y),
        #                                   (self.x + self.width, self.y + self.height),
        #                                   (self.x, self.y + self.height)
        #                               ),
        #                               self.color)
        pygame.draw.rect(screen, GREEN, pygame.rect.Rect(self.x, self.y, self.width, self.height), self.border_width)

        font = pygame.freetype.SysFont(["consolas", "courier"], 12, bold=True)
        txt = font.render(self.text, 1, BLACK)
        txt_x = (self.x + self.width * 0.5) - (txt[1].width * 0.5)
        txt_y = (self.y + self.height * 0.5) - (txt[1].height * 0.5)
        font.render_to(screen, (txt_x, txt_y), self.text, BLACK)

    def check_intersect(self, pos: Vec2):
        return self._pos == pos or pygame.rect.Rect(self.x, self.y, self.width, self.height).collidepoint(pos.x, pos.y)

    def unclick(self):
        if self.is_clicked:
            self.callback()
        super().unclick()

