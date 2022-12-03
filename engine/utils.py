import math
from engine.vector import Vec2


# Calculate the distance between two points
def calc_distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx**2 + dy**2)


def clamp(minimum, value, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def deg_to_rad(angle_deg):
    return angle_deg * math.pi / 180


def rad_to_deg(angle_rad):
    return angle_rad * 180 / math.pi


# Calculate the angle (in radians) between a point and the x-axis of another point
def calc_theta(pos1, pos2):
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y

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

    return math.atan(dx/dy) + theta_adder


def cartesian_to_polar(vec, ref_vec):
    return Vec2(vec.mag(ref_vec), vec.ancle(ref_vec))


def polar_to_cartesian(vec, ref_vec):
    return Vec2(ref_vec.x + (vec.r * math.cos(vec.theta)), ref_vec.y + (vec.r * math.sin(vec.theta)))


# Calculate position from radial coordinates and a reference point
def calc_pos(r, theta, ref_pos):
    x = ref_pos[0] + (r * math.cos(theta))
    y = ref_pos[1] + (r * math.sin(theta))
    return [x, y]


def in_ball(point: Vec2, ball_pos: Vec2, radius) -> bool:
    return calc_distance(point.get(), ball_pos.get()) <= radius


def line_line_intersect(p0, p1, q0, q1):
    x0 = p0.get()
    x1 = p1.get()
    y0 = q0.get()
    y1 = q1.get()

    d = (x1[0] - x0[0]) * (y1[1] - y0[1]) + (x1[1] - x0[1]) * (y0[0] - y1[0])
    if d == 0:
        return None
    t = ((y0[0] - x0[0]) * (y1[1] - y0[1]) + (y0[1] - x0[1]) * (y0[0] - y1[0])) / d
    u = ((y0[0] - x0[0]) * (x1[1] - x0[1]) + (y0[1] - x0[1]) * (x0[0] - x1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return round(x1[0] * t + x0[0] * (1 - t)), round(x1[1] * t + x0[1] * (1 - t))
    return None
