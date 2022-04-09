import math


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