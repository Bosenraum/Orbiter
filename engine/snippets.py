
import math

# Some ideas from blog.bruce-hill.com/6-useful-snippets

GOLDEN_RATIO = (math.sqrt(5) + 1) / 2


def mix(low, high, amount):
    return (1 - amount) * low + amount * high


def get_gr_sample(i):
    return (i * GOLDEN_RATIO) % 1


def move_towards(value, target, speed):
    if abs(value - target < speed):
        return target
    direction = (target - value) / abs(target - value)
    return value + direction * speed


def new_pos(prev_pos, pos, dt, accel):
    vel = pos - prev_pos / dt
    new_vel = vel + dt * accel
    new_pos = pos + dt * new_vel
    return new_pos
    # return pos * 2 - prev_pos + accel * dt * dt


if __name__ == "__main__":
    # value = move_towards(value, target, 20)
    pass