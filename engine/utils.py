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
