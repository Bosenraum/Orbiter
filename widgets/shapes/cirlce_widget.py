
from widgets.shapes.shape_widget import *


class CircleWidget(ShapeWidget):

    def __init__(self, pos, *args, **kwargs):
        self.radius = kwargs.get("radius", 1)
        self.color = kwargs.get("color", colors.WHITE)
        super().__init__(pos)

    def draw(self, screen):
        draw_module.circle(screen, self.color, self.pos.x, self.pos.y, self.radius)