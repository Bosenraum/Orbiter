# Standard library imports
import sys
import math

# Third-party imports
import pygame

# Local imports
from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2, NULL_VECTOR_2D, UNIT_VECTOR_2D
from engine.controller import Controller
from engine.collisions import Ray
from engine.tracer import Tracer, TracerType


class Square:

    def __init__(self, width, height, **kwargs):
        pos = kwargs.get("pos", None)
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        self.color = kwargs.get("color", colors.BLACK)

        self.jump_height = kwargs.get("jump_height", 10)
        self.move_speed = kwargs.get("move_speed", 5)
        self.vel = kwargs.get("vel", NULL_VECTOR_2D)
        self.accel = kwargs.get("accel", NULL_VECTOR_2D)
        self.friction = kwargs.get("friction", NULL_VECTOR_2D)

        if pos and isinstance(pos, Vec2):
            self.pos = pos
        else:
            self.pos = Vec2(x, y)

        self.collisions = {
            "BOTTOM": False,
            "TOP": False,
            "LEFT": False,
            "RIGHT": False
        }

        self.rect = pygame.rect.Rect(x, y, width, height)
        self.is_jumping = False

    def jump(self):
        self.vel.y -= self.jump_height
        self.is_jumping = True

    def move_left(self, vel=1):
        self.vel.x -= vel * self.move_speed

    def move_right(self, vel=1):
        self.vel.x += vel * self.move_speed

    def move(self, vel: Vec2):
        self.vel.x = vel.x * self.move_speed

    def update(self):
        self.vel += self.accel + self.friction

        if self.collisions["BOTTOM"]:
            if not self.is_jumping and self.vel.y > 0:
                self.vel.y = 0

            if self.vel.x > 0:
                self.vel.x -= 0.2
            elif self.vel.x < 0:
                self.vel.x += 0.2

        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        self.pos += self.vel
        self.rect.update(self.pos.x, self.pos.y, self.rect.w, self.rect.h)

    def check_collision(self, other):

        # Check collisions!
        # if self.square.colliderect(self.platform):
        if self.rect.y + self.rect.h > other.y \
                and self.rect.x <= other.x + other.w \
                and self.rect.x + self.rect.w >= other.x \
                and self.vel.y > 0:
            self.collisions["BOTTOM"] = True

            # Bottom collision
            self.rect.y = other.y - self.rect.h
        else:
            self.collisions["BOTTOM"] = False
            self.friction = NULL_VECTOR_2D

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self, border_radius=4)


class GamePlatformSquare(Engine):

    def __init__(self, width, height):
        self.dir_start = NULL_VECTOR_2D
        self.dir_end = UNIT_VECTOR_2D
        self.mouse_rays = None
        self.active_ray = None
        self.draw_active_ray = None
        self.mouse_pos = None
        self.mouse_size = None
        self.mouse_color = None
        self.mouse_tracer = None

        self.shift_held = None

        # Declare game variables before super call
        self.square: Square = None
        self.platform = None
        self.p2 = None
        self.platform_pos = NULL_VECTOR_2D
        self.p2_pos = NULL_VECTOR_2D

        self.gravity = Vec2(0, 0.0981)
        self.msg_font = None
        self.font_size = 50
        self.show = False

        self.text_rect: pygame.rect.Rect = None
        self.text_buffer = None
        self.text_pos = Vec2(100, 100)
        self.text_pos_offset = Vec2(0, 0)

        self.controller: Controller = None

        super().__init__(width, height, 1)

    def on_start(self):
        # Initialize game variables
        self.active_ray = Ray(self.dir_start, self.dir_end, color=colors.vivid_cerulean, dot_color=colors.beer)
        self.mouse_rays = []
        self.mouse_pos = Vec2(pygame.mouse.get_pos())
        self.mouse_size = 5

        self.mouse_color = colors.beer
        self.mouse_tracer = Tracer(self.mouse_color, 100, tracer_type=TracerType.CIRCLE, end_color=colors.razzmatazz, width=2)

        self.shift_held = False

        _unit = 50
        self.square = Square(_unit, _unit, pos=Vec2(_unit, _unit), color=colors.silver, accel=self.gravity)

        self.platform_pos = Vec2(0, self.height - _unit)
        self.platform = pygame.rect.Rect(self.platform_pos.x, self.platform_pos.y, self.width, _unit)

        self.p2_pos = Vec2(self.width * 0.6, self.height * 0.6)
        self.p2 = pygame.rect.Rect(self.p2_pos.x, self.p2_pos.y, self.width * 0.5, _unit)

        self.msg_font = pygame.freetype.SysFont(["jetbrainsmono"], self.font_size)

        self.text_buffer = ""
        self.text_rect = pygame.rect.Rect(self.text_pos.x, self.text_pos.y, 0, 0)

        if self.joysticks:
            self.controller = Controller(self.joysticks[0], deadzone=0.01)

    def process_key_inputs(self, event: pygame.event.Event):
        if event.mod & pygame.KMOD_SHIFT:
            self.shift_held = True
        else:
            self.shift_held = False

        if event.type == pygame.KEYDOWN:

            # Handle special keys if needed before adding to text
            if event.key == pygame.K_BACKSPACE:
                self.text_buffer = self.text_buffer[:len(self.text_buffer) - 1]
            else:
                self.text_buffer += event.unicode

            if event.key == pygame.K_SPACE:
                # msg = f"Austin Loves Jasmine More!"
                # print(msg)
                self.show = not self.show
                self.square.jump()

            if event.key == pygame.K_RETURN:
                if self.shift_held:
                    self.text_buffer = ""

            if event.key == pygame.K_a:
                self.square.move_left()
            if event.key == pygame.K_d:
                self.square.move_right()

    def process_mouse_inputs(self, ev: pygame.event.Event):
        self.draw_active_ray = True

        try:
            self.mouse_pos = Vec2(ev.pos[0], ev.pos[1])
        except AttributeError:
            pass

        if ev.type == pygame.MOUSEMOTION:
            if ev.buttons[0]:
                self.text_pos = self.mouse_pos + self.text_pos_offset
                self.active_ray.q = self.mouse_pos

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                self.active_ray.origin = self.mouse_pos
                self.draw_active_ray = False

                if self.text_rect.collidepoint(self.mouse_pos.x, self.mouse_pos.y):
                    self.text_pos_offset = self.text_pos - self.mouse_pos

        if ev.type == pygame.MOUSEBUTTONUP:
            new_ray = Ray(self.active_ray.origin, self.active_ray.q, color=colors.dark_green, dot_color=colors.byzantine)
            self.mouse_rays.append(new_ray)

        if ev.type == pygame.MOUSEWHEEL:
            self.mouse_size += ev.y * (5 if self.shift_held else 1)
            if self.mouse_size <= 1:
                self.mouse_size = 1

    def process_controller_events(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == self.controller.button_map["A"]:
                self.square.jump()

        if event.type == pygame.JOYAXISMOTION:
            pass
            # if event.axis == self.controller.axis_map["LX"]:
            #     lx_value = self.controller.get_axis("LX")
            #     if abs(lx_value) > self.controller.deadzone:
            #         self.square.move(Vec2(lx_value, 0))

    def process_controller_inputs(self):
        # if event.axis == self.controller.axis_map["LX"]:
        lx_value = self.controller.get_axis("LX")
        if abs(lx_value) > self.controller.deadzone:
            self.square.move(Vec2(lx_value, 0))

    def on_update(self, elapsed_time):
        # Simulate game and update game variables
        if self.controller:
            self.controller.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # TEXTINPUT does not receive unicode characters like 'RETURN' - '\r' or 'BACKSPACE' - '\0x08'
            # if event.type == pygame.TEXTINPUT:
            #     self.text_buffer += event.text

            # print(event)

            if event.type in Engine.KEYBOARD_EVENTS:
                self.process_key_inputs(event)
            elif event.type in Engine.MOUSE_EVENTS:
                self.process_mouse_inputs(event)
            elif event.type in Engine.CONTROLLER_EVENTS:
                # Event based controller states
                if self.controller:
                    self.process_controller_events(event)

        # Non-event based controller states
        if self.controller:
            self.process_controller_inputs()

        # Update physics
        self.square.update()

        self.square.check_collision(self.platform)
        self.square.check_collision(self.p2)

        self.screen.fill(colors.BLACK)
        # Draw stuff

        # pygame.draw.rect(self.screen, colors.get_gray(30), self.text_rect)
        if True:
            # msg = f"Austin Loves Jasmine More!"
            msg = self.text_buffer
            i = 0
            for line in msg.split("\r"):
                # Render the text to get dimensions
                line_surface, t_rect = self.msg_font.render(line.encode("UTF-8"), True, colors.GREEN)
                # self.screen.blit(line_surface, self.text_pos.get())
                self.text_rect.update(self.text_pos.x, self.text_pos.y, max(self.text_rect.w, t_rect.w), self.text_rect.y - self.text_rect.h - t_rect.h)
                self.msg_font.render_to(self.screen, (self.text_pos.x, self.text_pos.y + (50 * i)), line, colors.alabaster)
                i += 1

        # pygame.draw.rect(self.screen, colors.silver, self.square, 0, border_radius=4)
        self.square.draw(self.screen)
        pygame.draw.rect(self.screen, colors.GREEN, self.platform, 0)
        pygame.draw.rect(self.screen, colors.BLUE, self.p2, 0)

        draw_radius = self.mouse_size + 0.2 * self.mouse_size * math.sin(self.et * math.pi * 2 * 0.4)
        if draw_radius <= 1:
            draw_radius = 1
        pygame.draw.circle(self.screen, self.mouse_color, self.mouse_pos.get(), draw_radius, 1)
        # self.mouse_tracer.trace(self.screen)
        self.mouse_tracer.append((self.mouse_pos, draw_radius))

        for ray in self.mouse_rays:
            ray.draw(self.screen)

            p2_result = ray.colliderect(self.p2)
            if p2_result["collides"]:
                pygame.draw.circle(self.screen, colors.silver, p2_result["contact_point"].get(), 4)
                pygame.draw.circle(self.screen, colors.silver, p2_result["far_contact_point"].get(), 4)
                # pygame.draw.line(self.screen, colors.silver, p2_result["contact_point"].get(), p2_result["contact_point"] + (p2_result["contact_normal"] * 5).get())

        if self.draw_active_ray:
            self.active_ray.draw(self.screen)


        pygame.display.update()


if __name__ == "__main__":
    # Global variables to hold type hint info
    rect = pygame.rect.Rect(0, 0, 0, 0)
    # Start the game
    w, h = 800, 800
    GamePlatformSquare(w, h)
