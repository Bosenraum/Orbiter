import math


# A simple class to hold the x and y component of a vector
class Vec2:

    def __init__(self, x, y):
        if y is None:
            y = x[1]
            x = x[0]

        self._x = x
        self._y = y
        self._r = x
        self._theta = y
        self._item_list = [self._x, self._y]

    def __str__(self):
        return f"({self._x}, {self._y})"

    def __add__(self, vec):
        self.x += vec.x
        self.y += vec.y
        return self

    def __sub__(self, vec):
        self.x -= vec.x
        self.y -= vec.y
        return self

    def __mul__(self, vec):
        if isinstance(vec, self.__class__):
            self.x *= vec.x
            self.y *= vec.y
        elif isinstance(vec, (int, float)):
            self.x *= vec
            self.y *= vec
        else:
            raise ValueError(f"Cannot multiply Vec2 by {type(vec)}")
        return self

    def __radd__(self, vec):
        return Vec2(self.x + vec.x, self.y + vec.y)

    def __rsub__(self, vec):
        return Vec2(vec.x - self.x, vec.y - self.y)

    def __getitem__(self, item):
        return self._item_list[item]

    def get(self):
        return self._x, self._y

    def distance(self, vec):
        return math.sqrt((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2)

    def mag(self, vec):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle(self, vec):
        dx = self.x - vec.x
        dy = self.y - vec.y

        # Offset theta based on quadrant
        # Quadrant 1
        if dx > 0 and dy > 0:
            theta_adder = 0

        # Quadrant 2 or 3
        elif dx < 0:
            theta_adder = math.pi

        # Quadrant 4
        else:
            theta_adder = 2 * math.pi

        return math.atan(dx / dy) + theta_adder

    def dot(self, vec):
        return self.x * vec.x + self.y + vec.y

    def cross(self, vec):
        print(f"Don't cross me!")

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._r = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._theta = y

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._x = r
        self._r = r

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, theta):
        self._y = theta
        self._theta = theta


NULL_VECTOR = Vec2(0, 0)
UNIT_VECTOR = Vec2(1, 1)
