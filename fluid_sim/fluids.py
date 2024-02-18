import random

import pygame
from pygame.event import Event
from pygame.rect import Rect
import pygame.mouse as mouse

import sys
import math
from dataclasses import dataclass

from engine.engine import Engine
from engine.vector import Vec2
import engine.colors as colors
import engine.snippets as snips
import engine.utils as utils

from widgets.shapes import shape_widget_factory as swf

N = 50
ITERATIONS = 1


def IX(x, y):
    x = utils.clamp(0, x, N - 1)
    y = utils.clamp(0, y, N - 1)
    return x + y * N


def diffuse(b, x, x0, diffusion_amount, dt):
    a = dt * diffusion_amount * (N - 2) * (N - 2)
    lin_solve(b, x, x0, a, 1 + 6 * a)


def project(vel_x, vel_y, p, div):
    for j in range(N - 1):
        for i in range(N - 1):
            neighbor_vel = vel_x[IX(i + 1, j)] - vel_x[IX(i - 1, j)] + vel_y[IX(i, j + 1)] - vel_y[IX(i, j - 1)]
            div[IX(i, j)] = -0.5 * neighbor_vel / N
            p[IX(i, j)] = 0

    set_bounds(0, div)
    set_bounds(0, p)
    lin_solve(0, p, div, 1, 6)

    for j in range(N - 1):
        for i in range(N - 1):
            vel_x[IX(i, j)] -= 0.5 * (p[IX(i + 1, j)] - p[IX(i - 1, j)]) * N
            vel_y[IX(i, j)] -= 0.5 * (p[IX(i, j + 1)] - p[IX(i, j - 1)]) * N

    set_bounds(1, vel_x)
    set_bounds(2, vel_y)


def advect(b, d, d0, vel_x, vel_y, dt):
    dtx = dt * (N - 2)
    dty = dt * (N - 2)

    nfloat = N - 2

    for j in range(N - 1):
        for i in range(N - 1):
            tmp1 = dtx * vel_x[IX(i, j)]
            tmp2 = dty * vel_y[IX(i, j)]
            x = i - tmp1
            y = j - tmp2

            if x < 0.5: x = 0.5
            if x > nfloat + 0.5: x = nfloat + 0.5
            i0 = math.floor(x)
            i1 = i0 + 1
            if y < 0.5: y = 0.5
            if y > nfloat + 0.5: y = nfloat + 0.5
            j0 = math.floor(y)
            j1 = j0 + 1

            s1 = x - i0
            s0 = 1 - s1
            t1 = y - j0
            t0 = 1 - t1

            i0i = i0
            i1i = i1
            j0i = j0
            j1i = j1

            d[IX(i, j)] = s0 * (t0 * d0[IX(i0i, j0i)] + t1 * d0[IX(i0i, j1i)]) + \
                          s1 * (t0 * d0[IX(i1i, j0i)] + t1 * d0[IX(i1i, j1i)])

    set_bounds(b, d)


def lin_solve(b, x, x0, a, c):
    c_recip = 1 / c
    for k in range(ITERATIONS):
        for j in range(N - 1):
            for i in range(N - 1):
                neighbor_sum = x[IX(i + 1, j)] + x[IX(i - 1, j)] + x[IX(i, j + 1)] + x[IX(i, j - 1)]
                x[IX(i, j)] = (x0[IX(i, j)] + a * neighbor_sum) * c_recip

        set_bounds(b, x)


def set_bounds(b, x):
    mi = -1 if b == 2 else 1
    mj = -1 if b == 1 else 1

    for i in range(N):

        x[IX(i, 0)] = x[IX(i, 1)] * mi
        x[IX(i, N - 1)] = x[IX(i, N - 2)] * mi

    for j in range(N):
        x[IX(0, j)] = x[IX(1, j)] * mj
        x[IX(N - 1, j)] = x[IX(N - 2, j)] * mj

    x[IX(0, 0)] = 0.5 * (x[IX(1, 0)] + x[IX(0, 1)])
    x[IX(0, N - 1)] = 0.5 * (x[IX(1, N-1)] + x[IX(0, N-2)])
    x[IX(N - 1, 0)] = 0.5 * (x[IX(N - 2, 0)] + x[IX(N - 1, 1)])
    x[IX(N - 1, N - 1)] = 0.5 * (x[IX(N - 2, N - 1)] + x[IX(N - 1, N - 2)])


class FluidCube:

    def __init__(self, dt, diffusion, viscosity):
        self.size = N
        self.dt = dt
        self.diffusion = diffusion
        self.viscosity = viscosity

        self.density = [0 for _ in range(N * N)]
        self.s = [0 for _ in range(N * N)]

        self.Vx = [0 for _ in range(N * N)]
        self.Vy = [0 for _ in range(N * N)]
        self.Vx0 = [0 for _ in range(N * N)]
        self.Vy0 = [0 for _ in range(N * N)]

    def add_density(self, x, y, amount):
        index = IX(x, y)
        self.density[index] += amount

    def add_velocity(self, x, y, amount_x, amount_y):
        index = IX(int(x), int(y))
        self.Vx[index] += amount_x
        self.Vy[index] += amount_y

    def step(self, dt):
        diffuse(1, self.Vx0, self.Vx, self.viscosity, dt)
        diffuse(2, self.Vy0, self.Vy, self.viscosity, dt)

        project(self.Vx0, self.Vy0, self.Vx, self.Vy)

        advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0, dt)
        advect(2, self.Vy, self.Vx0, self.Vx0, self.Vy0, dt)

        project(self.Vx, self.Vy, self.Vx0, self.Vy0)

        diffuse(0, self.s, self.density, self.diffusion, dt)
        advect(0, self.density, self.s, self.Vx, self.Vy, dt)

    def render_density(self, screen, spot_width, spot_height):
        for i in range(N - 1):
            for j in range(N - 1):
                d = utils.clamp(0, self.density[IX(i, j)], 255)
                color = colors.get_gray(d)
                r = pygame.rect.Rect(i * spot_width, j * spot_height, spot_width - 1, spot_height - 1)
                pygame.draw.rect(screen, color, r, width=3)


class FluidEngine(Engine):
    APP_NAME = "Fluids"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)
        self.pf = kwargs.get("pf", 1)

        # ## Common variables ## #
        self.bg_color = None
        self.m1 = None
        self.m2 = None
        self.m3 = None

        self.widget_factory = None
        self.mouse_pos = None
        self.prev_mous_pos = None

        # ## Fluid variables ## #
        self.fluid: FluidCube = FluidCube(1 / self.FPS, 0, 0)

        super().__init__(width, height, self.pf)

    def on_start(self):
        self.widget_factory = swf.ShapeFactory()
        self.mouse_pos = Vec2(mouse.get_pos())
        self.prev_mous_pos = self.mouse_pos

        self.bg_color = colors.get_gray(25)
        color = colors.Blue.electric_blue
        start_pos = Vec2((self.width / 2) - 50, (self.height / 2) - 50)

        self.fluid = FluidCube(0.1, 0.001, 0)

    def process_keydown_inputs(self, ev: Event):

        if ev.key == pygame.K_SPACE:
            print(f"Space at {self.mouse_pos}")

    def run_sim(self):
        self.mouse_held()
        self.fluid.step(0.01)

    def mouse_held(self):
        spot_width = self.width / N
        spot_height = self.height / N
        x = int(self.mouse_pos.x / spot_width)
        y = int(self.mouse_pos.y / spot_height)
        if self.m1:
            self.fluid.add_density(x, y, 50)
        if self.m3:
            amount = self.mouse_pos - self.prev_mous_pos
            self.fluid.add_velocity(x, y, int(amount.x), int(amount.y))

    def draw_sim(self):
        spot_width = self.width / N
        spot_height = self.height / N
        self.fluid.render_density(self.screen, spot_width, spot_height)

    def on_update(self, elapsed_time):

        self.m1, self.m2, self.m3 = pygame.mouse.get_pressed(3)
        self.mouse_pos = Vec2(mouse.get_pos())

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_keydown_inputs(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

        self.screen.fill(self.bg_color)

        self.run_sim()
        self.draw_sim()

        self.prev_mous_pos = self.mouse_pos

        pygame.display.update()


if __name__ == "__main__":
    FluidEngine(800, 800, pf=1)
