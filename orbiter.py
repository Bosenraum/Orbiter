import sys
import math
import random

import pygame
import pygame.gfxdraw
import pygame.freetype
# from pygame.locals import *

from colors import *
from tracer import *
from planet import *
from utils import *
from dial import Dial


def redraw(scr):
    # ########################
    # ##### DRAW SECTION #####
    # ########################
    scr.fill(bg_color)

    nrects = 40
    for i in range(nrects):
        width = SCREEN_WIDTH / nrects
        r = pygame.Rect(i * width, 0, width, SCREEN_HEIGHT)
        color = color_span(blend(silver, outer_space), blend(pink, outer_space), i, nrects)
        cr = int(abs(math.sin(et * math.pi / 6) * color[0] * 1 / 6)) + color[0] * 3 / 4
        cg = int(abs(math.sin(et * math.pi / 4) * color[1] * 2 / 12)) + color[1] * 3 / 4
        cb = int(abs(math.sin(et * math.pi / 2) * color[2] * 2 / 12)) + color[2] * 3 / 4
        ca = int(abs(math.sin(et * math.pi / 8) * 100)) + 150
        color = color_clamp((cr, cg, cb, ca))
        # pygame.draw.rect(scr, color, r)
        pygame.gfxdraw.box(scr, r, color)

    # Draw targets
    # pygame.draw.circle(scr, target_color, target_pos.get(), target_radius, 10)
    # pygame.draw.circle(scr, bullseye_color, bullseye_pos.get(), bullseye_radius, 10)

    # Draw moon trace
    # line_trace.trace(scr)
    # moon_trace.trace(scr)
    # planet_trace.trace(scr)

    # planet.draw(scr)
    # moon.draw(scr)
    # scr.blit(clover, (moon.position - Vec2(8, 8)).get())

    dial.draw(scr)

    # GUI text
    gui_font.render_to(scr, (scr.get_width() / 3, scr.get_height() - 80), f"SCORE: {format(player_score, '07.2f')}", WHITE)

    if print_time:
        gui_font.render_to(scr, (100, scr.get_height() - 100), f"Time Elapsed: {format(et, '5.2f')}", WHITE)

    # Debug text
    pygame.draw.rect(scr, (0x30, 0x30, 0x30), (0, 0, 300, 180), border_bottom_right_radius=20)
    debug_font.render_to(scr, (20, 20), f"FPS={format(nframes / et, '6.2f').rjust(6)}, "
                                           f"theta={format(theta, '.2').rjust(6)} "
                                           f"({round(math.degrees(theta), 2)})", WHITE)
    debug_font.render_to(scr, (20, 40), f"moon_x={format(moon.position.x, '0.5').rjust(6)}, "
                                           f"moon_y={format(moon.position.y, '0.5').rjust(6)}", WHITE)
    debug_font.render_to(scr, (20, 60), f"wobble_speed={round(moon_wobble_speed, 2)}, "
                                           f"wobble_offset={round(moon_wobble_offset, 2)}", WHITE)
    debug_font.render_to(scr, (20, 80), f"planet_x={format(float(planet.position.x), '0.5').rjust(6)}, "
                                           f"planet_y={format(float(planet.position.y), '0.5').rjust(6)}", WHITE)
    debug_font.render_to(scr, (20, 100), f"mouse_held         in_ball", WHITE)

    pygame.gfxdraw.filled_circle(scr, 60, 140, 20, GREEN if mouse_held else RED, )
    pygame.gfxdraw.filled_circle(scr, 180, 140, 20, GREEN if cursor_in_ball1 or cursor_in_ball2 else RED)

    # pygame.draw.circle(scr, pygame.Color(((abs(math.sin(theta)) * 128) % 255, 128, (abs(math.cos(theta)) * 64) % 255)),
    #                    moon_position,
    #                    moon_radius,
    #                    moon_crust_width)

    # pygame.display.update()


# Screen info
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FPS = 60
dt = 1 / FPS
et = 0
print_time = False

# Setup the main screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_window = pygame.display.set_mode((SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80))
bg_color = deep_purple

# Set up font
pygame.freetype.init()
debug_font = pygame.freetype.SysFont(["consolas", "Helvetica", "courier"], 12, bold=True)
gui_font = pygame.freetype.SysFont(["Helvetica", "Futura"], 60, bold=True)

# Game clock
game_clock = pygame.time.Clock()

# clover = pygame.image.load("ThreeLeafClover.png")

surf = pygame.Surface((40, 40), pygame.HWSURFACE | pygame.HWACCEL)
surf.fill((120, 50, 50, 0))
pygame.gfxdraw.filled_circle(surf, 20, 20, 20, pink)
cc = pygame.cursors.Cursor((20, 20), surf)

# pygame.mouse.set_cursor(*pygame.cursors.broken_x)
# pygame.mouse.set_cursor(cc)

planet_position = Vec2(SCREEN_WIDTH/2, SCREEN_HEIGHT * (3/8))
planet_velocity = NULL_VECTOR_2D
planet_radius = .1 * min(SCREEN_WIDTH, SCREEN_HEIGHT)
planet_crust_width = 8
planet_mass = 1e6

planet = Planet("Planet 1", planet_radius, planet_position,
                thickness=planet_crust_width,
                mass=planet_mass,
                color=violet_blue,
                core=blue_violet,
                fill=False,
                num_rings=25)

planet_placeholder = NULL_VECTOR_2D

moon_position = Vec2(planet.position.x - (1 * planet.radius), planet.position.y - (1 * planet.radius))
moon_velocity = NULL_VECTOR_2D
# moon_theta = calc_theta(moon_position, planet_position)
moon_angular_velocity = math.pi/180
moon_radius = planet_radius // 5
moon_crust_width = planet_crust_width // 5
moon_mass = 1e3

moon = Planet("Moon 1", moon_radius, moon_position,
              thickness=moon_crust_width,
              mass=moon_mass,
              color=(*white_coffee, 128),
              fill=False)

moon_distance = 2.5 * planet_radius #moon.position.mag(planet.position)
moon_distance_normal = moon_distance
moon_wobble = 0
moon_wobble_speed = 0 #2 * math.pi / 2
moon_wobble_offset = 0

theta = moon.position.angle(planet.position)

moon_trace = Tracer(empty_beer, moon_radius, 3000, TracerType.POINT, end_color=blue_violet)
planet_trace = Tracer(RED, 15, 75, TracerType.POINT)
line_trace = Tracer(RED, 2, 100, TracerType.LINE, end_color=GREEN)

grey = 255
grey_up = True

grey_max = 250
grey_min = 132
grey_inc = 2

ball_radius = 20

target_pos = Vec2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
target_color = WHITE
target_radius = SCREEN_HEIGHT/4
target_active = False
target_speed = Vec2(2, 2)

bullseye_pos = target_pos
bullseye_color = RED
bullseye_radius = target_radius / 3
bullseye_active = False

player_score = 0

ball1_pos = Vec2(200, 200)
ball1_color = BLUE
ball1_radius = ball_radius
ball1_active = False

ball2_pos = Vec2(400, 400)
ball2_color = GREEN
ball2_radius = ball_radius * 1.5
ball2_active = False

planet_active = False
mouse_held = False
nframes = 0

dial = Dial(500, 500, 100, color=GREEN)

while True:

    game_clock.tick(FPS)
    et += dt
    nframes += 1

    for event in pygame.event.get():
        # process events
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                moon_wobble_speed += math.pi / 15
                target_speed += Vec2(1, 1)
                dial.inc(5)
                # moon_trace.clear()
            elif event.key == pygame.K_DOWN:
                moon_wobble_speed -= math.pi / 15
                target_speed -= Vec2(1, 1)
                dial.inc(-5)
                # moon_trace.clear()
            elif event.key == pygame.K_RIGHT:
                moon_wobble_offset += math.pi / 4
                target_speed.x += 1
                dial.inc(25)
                # moon_trace.clear()
            elif event.key == pygame.K_LEFT:
                moon_wobble_offset -= math.pi / 4
                target_speed.y += 1
                dial.inc(-25)
                # moon_trace.clear()
            elif event.key == pygame.K_SPACE:
                moon_trace.clear()
                target_speed = Vec2(2, 2)
                dial.reset()
            elif event.key == pygame.K_TAB:
                dial.set(dial.max)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False
        elif event.type == pygame.MOUSEWHEEL:
            # print(f"Mousewheel event: {event.x}, {event.y}")
            dial.inc(event.y * 2)

    # planet.position.x = planet_position.x + 1 * math.cos(math.pi / 12 * et)
    # planet.position.y = planet_position.y + 1.5 * math.sin(math.pi / 7 * et + math.pi / 3)

    mouse_pos = Vec2(*pygame.mouse.get_pos())
    cursor_in_ball1 = in_ball(mouse_pos, ball1_pos, ball1_radius)
    cursor_in_ball2 = in_ball(mouse_pos, ball2_pos, ball2_radius)
    cursor_in_planet = in_ball(mouse_pos, planet.position, planet.radius)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        print_time = True
        # print(f"W pressed")
    else:
        print_time = False

    mouse_buttons_pressed = pygame.mouse.get_pressed(3)
    if mouse_buttons_pressed[0]:
        if cursor_in_ball1 or ball1_active:
            ball1_active = True
            ball1_pos = mouse_pos
        elif cursor_in_ball2 or ball2_active:
            ball2_pos = mouse_pos
            ball2_active = True
        if cursor_in_planet or planet_active:
            if planet_placeholder == NULL_VECTOR_2D:
                planet_placeholder = Vec2(mouse_pos.x - planet.position.x, mouse_pos.y - planet.position.y)
            planet_active = True
            planet.set_position(Vec2(int(mouse_pos.x - planet_placeholder.x), int(mouse_pos.y - planet_placeholder.y)))
            # planet.position = mouse_pos
            # print(mouse_pos.x, ", ", mouse_pos.y, end="")
            # print(f"  -  {planet.position.x}, {planet.position.y}")
    else:
        ball1_active = False
        ball2_active = False
        planet_active = False
        planet_placeholder = NULL_VECTOR_2D

    # Update the simulation
    # new_moon_angular_velocity = (moon_angular_velocity / 2) * math.cos(math.sin(et) * math.pi * 2/3) + (moon_angular_velocity / 2)
    theta += moon_angular_velocity
    theta = theta % (math.pi*2)
    # moon.position = calc_pos(moon_distance, theta, planet.position)
    # moon_wobble = 90 * math.sin(moon_wobble_speed * math.tan(math.sin(et)) * math.cos(round(et, 4)) * 2/math.pi) + 60 * math.cos(
    #         moon_wobble_offset * (2/3) * math.tanh(et) * math.pi / 4) + moon_wobble_offset
    moon_wobble = moon_distance * 0.5 * math.cos(moon_wobble_speed * et)
    moon.position = polar_to_cartesian(Vec2(moon_distance + moon_wobble, theta), planet.position)

    # moon_trace.color = (empty_beer[0] * 1/4 * math.cos(math.pi * 0.25 * et) + empty_beer[0] * 3/4,
    #                     empty_beer[1] * 1/4 * math.cos(math.pi * 0.25 * et) + empty_beer[1] * 3/4,
    #                     empty_beer[2] * 1/4 * math.cos(math.pi * 0.25 * et) + empty_beer[2] * 3/4)
    # moon_trace.end_color = (violet_blue[0] * 1/4 * math.cos(math.pi * .75 * et) + blue_violet[0] * 3/4,
    #                         blue_violet[1] * 1/4 * math.cos(math.pi * .75 * et) + blue_violet[1] * 3/4,
    #                         blue_violet[2] * 1/4 * math.cos(math.pi * .75 * et) + blue_violet[2] * 3/4)
    moon_trace.append(moon.position)

    # Check scoring conditions
    if in_ball(moon.position, bullseye_pos, bullseye_radius):
        player_score += 3 * dt
    elif in_ball(moon.position, target_pos, target_radius):
        player_score += dt

    planet_trace_color = (255, 0, 255)
    planet_trace.append(Vec2(*planet.position.get()), planet_trace_color)

    line_trace.append((planet.position.get(), moon.position.get()))

    target_pos += target_speed
    if ((target_pos.x + target_radius) > SCREEN_WIDTH) or (target_pos.x - target_radius) < 0:
        target_speed.x *= -1

    if ((target_pos.y + target_radius) > SCREEN_HEIGHT) or (target_pos.y - target_radius) < 0:
        target_speed.y *= -1

    # screen.fill(bg_color)
    redraw(game_window)
    pygame.display.update()
