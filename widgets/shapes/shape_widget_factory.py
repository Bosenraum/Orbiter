
from widgets.shapes.shape_widget import *
from widgets.shapes.cirlce_widget import CircleWidget
from widgets.shapes.rectangle_widget import RectangleWidget


class ShapeFactory:

    def __init__(self, *args, **kwargs):
        pass

    def create(self, shape, *args, **kwargs) -> ShapeWidget:
        radius = kwargs.get("radius", 1)

        if shape == "circle":
            return CircleWidget(Vec2(0, 0), radius=radius)
        elif shape in ["rect", "rectangle"]:
            return RectangleWidget(Vec2(0, 0), width=1, height=1)
        else:
            return ShapeWidget(Vec2(0, 0))
