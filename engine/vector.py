import math


# A simple class to hold the x and y component of a vector
class Vec2:

    def __init__(self, x, y=None):
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
        return Vec2(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2(self.x - vec.x, self.y - vec.y)

    def __mul__(self, vec):
        x = 0
        y = 0
        if isinstance(vec, self.__class__):
            x = self.x * vec.x
            y = self.y * vec.y
        elif isinstance(vec, (int, float)):
            x = self.x * vec
            y = self.y * vec
        else:
            raise ValueError(f"Cannot multiply Vec2 by {type(vec)}")
        return Vec2(x, y)

    def __truediv__(self, other):
        # print(f"Division!")
        try:
            if isinstance(other, Vec2):
                return Vec2(self.x / other.x, self.y / other.y)
            elif isinstance(other, (int, float)):
                return Vec2(self.x / other, self.y / other)
        except ZeroDivisionError:
            print(f"Cannot divide by zero: ({other.x}, {other.y})")

    # def __rdiv__(self, other):
    #     try:
    #         return Vec2(other.x / self.x, other.y / self.y)
    #     except ZeroDivisionError:
    #         print(f"Cannot divide by zero: ({self.x}, {self.y})")

    def __radd__(self, vec):
        return Vec2(self.x + vec.x, self.y + vec.y)

    def __rsub__(self, vec):
        return Vec2(vec.x - self.x, vec.y - self.y)

    def __getitem__(self, item):
        return self._item_list[item]

    def __rmul__(self, other):
        if isinstance(other, Vec2):
            pass
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)

    def get(self):
        return self._x, self._y

    def distance(self, vec):
        return math.sqrt((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2)

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle(self, vec):
        dx = self.x - vec.x
        dy = self.y - vec.y

        if dx == 0:
            if dy > 0:
                return math.pi * 3 / 2
            elif dy < 0:
                return math.pi
            else:
                return 0

        if dy == 0:
            if dx >= 0:
                return 0
            else:
                return math.pi

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


class Vec3:

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self._x = x
        self._y = y
        self._z = z
        self._w = w
        self._item_list = [self._x, self._y, self._z, self._w]

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __len__(self):
        return 3

    def __getitem__(self, item):
        return self._item_list[item]

    def __setitem__(self, key, value):
        self._item_list[key] = value
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            self.w = value

    def __iter__(self):
        return self._item_list

    def __reversed__(self):
        return self._item_list.reverse()

    def __add__(self, v):
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
        else:
            raise TypeError(f"Vector multiplier must be numeric. {type(scalar)}")

    def __truediv__(self, scalar):
        if scalar == 0.0:
            raise ZeroDivisionError("Cannot divide Vec3 by 0.")

        if isinstance(scalar, (int, float)):
            return Vec3(self.x / scalar, self.y / scalar, self.z / scalar, self.w)
        else:
            raise TypeError(f"Vector divisor must be numeric. {type(scalar)}")

    def sync(self):
        self._item_list = [self._x, self._y, self._z, self._w]

    def mag(self):
        return math.sqrt(self.dot(self))

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        x = self.y * v.z - self.z * v.y
        y = self.z * v.x - self.x * v.z
        z = self.x * v.y - self.y * v.x
        return Vec3(x, y, z)

    def normalize(self):
        mag = self.mag()
        if mag == 0:
            return NULL_VECTOR_3D
        return Vec3(self.x / mag, self.y / mag, self.z / mag)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, other):
        self._z = other
        self.sync()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, other):
        self._y = other
        self.sync()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, other):
        self._x = other
        self.sync()

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, other):
        self._w = other
        self.sync()


NULL_VECTOR_2D = Vec2(0, 0)
UNIT_VECTOR_2D = Vec2(1, 1)

NULL_VECTOR_3D = Vec3(0, 0, 0)
UNIT_VECTOR_3D = Vec3(1, 1, 1)
UNIT_VEC3_X = Vec3(1, 0, 0)
UNIT_VEC3_Y = Vec3(0, 1, 0)
UNIT_VEC3_Z = Vec3(0, 0, 1)
