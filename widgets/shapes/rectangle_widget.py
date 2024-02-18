from widgets.shapes.shape_widget import *


class RectangleWidget(ShapeWidget):

    def __init__(self, pos, *args, **kwargs):
        self.color = kwargs.get("color", colors.WHITE)
        self._width = kwargs.get("width", 1)
        self._height = kwargs.get("height", 1)
        self._pos = pos

        self.rect = self.calc_rect()

        super().__init__(self._pos)


    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w
        self.rect = self.calc_rect()

    @property
    def height(self):
        return self._width

    @height.setter
    def height(self, h):
        self._height = h
        self.rect = self.calc_rect()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.rect = self.calc_rect()

    def calc_rect(self):
        return pygame.rect.Rect(self._pos.x, self._pos.y, self._width, self._height)

    def draw(self, screen):

        if USE_GFX:
            r = self.rect
            points = [r.topleft, r.topright, r.bottomright, r.bottomleft]
            pygame.gfxdraw.filled_polygon(screen, points, self.color)
        else:
            pygame.draw.rect(screen, self.rect, self.color)
