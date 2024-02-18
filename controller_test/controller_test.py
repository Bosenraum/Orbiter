import sys
import json
from enum import Enum, auto

import pygame

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2
from engine.controller import Controller
from engine.sequencer import Sequencer


# def save_input_map(in_map, filename="./controller_test/xbox_one_map.json"):
#     with open(filename, "w+") as map_file:
#         print(f"Saving input map to {filename}")
#         json.dump(in_map, map_file, indent=4)
#
#
# def load_input_map(filename="./controller_test/xbox_one_map.json"):
#     with open(filename, "r") as map_file:
#         in_map = json.load(map_file)
#     return in_map


class ControllerTest(Engine):

    def __init__(self, width, height):
        self.joy = None

        self.square = None
        self.square_pos = None
        self.square_color_index = None
        self.square_motion = None
        self.square_color = None
        self.square_colors = None

        self.axis_deadzone = 0.1
        self.axis_friction = 0.001
        self.gravity = 0.0

        self.controller = None
        self.rumble_enable = False

        self.debug_enabled = True
        self.debug_toggle_seq = None
        self.debug_sequencer = None

        super().__init__(width, height, 1)

    def on_start(self):
        self.square = pygame.Rect(50, 50, 50, 50)
        self.square_pos = Vec2(50, 50)
        self.square_color_index = 0
        self.square_color = colors.WHITE
        self.square_colors = [colors.alabaster, colors.razzmatazz, colors.grape]

        self.square_motion = Vec2(0, 0)

        [print(j.get_name()) for j in self.joysticks]
        self.joy = self.joysticks[0]
        self.joy.init()
        self.controller = Controller(self.joy, deadzone=self.axis_deadzone)
        # self.controller.load_config("./controller_test/controller_map.json")
        self.debug_toggle_seq = ["START", "SELECT", "HOME", "HOME"]
        self.debug_sequencer = Sequencer([self.controller.button_map[n] for n in self.debug_toggle_seq])

    # Take action on inputs once
    def process_controller_events(self, event):
        if event.type == pygame.JOYBUTTONUP:
            print(event)

            if event.button == self.controller.button_map["A"]:
                self.square_color = colors.dark_green
            elif event.button == self.controller.button_map["B"]:
                self.square_color = colors.razzmatazz
            elif event.button == self.controller.button_map["X"]:
                self.square_color = colors.vivid_cerulean
            elif event.button == self.controller.button_map["Y"]:
                self.square_color = colors.beer

        if event.type == pygame.JOYBUTTONDOWN:
            print(event)

            if self.debug_sequencer.check_input(event.button):
                self.debug_enabled = not self.debug_enabled

            # if event.button == self.controller.button_map[self.debug_toggle_seq[self.debug_seq_counter]]:
            #     self.debug_seq_status[self.debug_seq_counter] = True
            #     if False not in self.debug_seq_status:
            #         # Toggle debug
            #         self.debug_enabled = not self.debug_enabled
            #         self.debug_seq_counter = 0
            #         self.debug_seq_status = [False for _ in self.debug_toggle_seq]
            #     else:
            #         self.debug_seq_counter += 1
            # else:
            #     # Sequence failed, start over
            #     self.debug_seq_counter = 0
            #     self.debug_seq_status = [False for _ in self.debug_toggle_seq]

            if event.button == self.controller.button_map["A"]:
                self.square_color = colors.GREEN
            elif event.button == self.controller.button_map["B"]:
                self.square_color = colors.RED
                if self.gravity == 0.0:
                    self.gravity = 0.0981
                else:
                    self.gravity = 0.0
            elif event.button == self.controller.button_map["X"]:
                self.square_color = colors.BLUE
                self.rumble_enable = True
            elif event.button ==  self.controller.button_map["Y"]:
                self.square_color = colors.YELLOW
                self.rumble_enable = False
            else:
                self.square_color_index = (self.square_color_index + 1) % len(self.square_colors)
                self.square_color = colors.get_random_color((20, 230), (20, 230), (20, 230))

        if event.type == pygame.JOYHATMOTION:
            print(event)
            if self.controller.get_hat("LEFT"):
                self.square_pos = Vec2(50, 50)
                self.square_motion = Vec2(0, 0)
                self.square_color = colors.alabaster

        if event.type == pygame.JOYBALLMOTION:
            print(event)

    # Take action on each button every frame
    def process_controller_inputs(self):

        # 'A' pressed or not
        if self.controller.get_button("A"): pass

        # 'B' pressed or not
        if self.controller.get_button("B"): pass

        # 'X' pressed or not
        if self.controller.get_button("X"):
            self.rumble_enable = True

        # 'Y' pressed or not
        if self.controller.get_button("Y"):
            self.square_color = colors.YELLOW
            self.rumble_enable = False

        # TODO: Enumerate other buttons being pressed/not pressed
        if self.controller.get_button("START") and self.controller.get_button("SELECT"):
            sys.exit()

        self.square_motion.x = self.controller.get_axis("LX")
        self.square_motion.y = self.controller.get_axis("LY")

        # TODO: Handle other axis values

    def on_update(self, elapsed_time):

        self.controller.update()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type not in [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION]:
                print(event)
            self.process_controller_events(event)

        self.process_controller_inputs()

        # self.map_axes()
        if self.rumble_enable:
            self.joy.rumble((1 + self.controller.get_axis('LT')) * 0.5, (1 + self.controller.get_axis('RT')) * 0.5, 0)
        else:
            self.joy.stop_rumble()

        self.screen.fill(colors.BLACK)

        self.square_motion -= Vec2(self.axis_friction, self.axis_friction)

        if abs(self.square_motion.x) <= self.axis_deadzone:
            self.square_motion.x = 0.0
        if abs(self.square_motion.y) <= self.axis_deadzone:
            self.square_motion.y = self.gravity

        # Update position based on movement
        self.square_pos = self.square_pos + (self.square_motion * 10)
        self.square.update(self.square_pos.x, self.square_pos.y, 50, 50)
        pygame.draw.rect(self.screen, self.square_color, self.square)

        self.draw_controller()

        if self.debug_enabled:
            self.print_debug()

        pygame.display.update()

    def draw_controller(self):
        # Draw axis reps

        con_rect = pygame.rect.Rect(0.25 * self.width, 0.1 * self.height, self.width * 0.5, self.height * 0.3)
        con_w_unit = con_rect.width * 0.1
        con_h_unit = con_rect.height * 0.1
        pygame.draw.rect(self.screen, colors.alabaster, con_rect, width=1)

        grid_on = False
        grid_color = colors.dark_green
        if grid_on:
            # draw grid:
            for i in range(1, 10):
                # Draw vertical lines
                v = con_rect.x + i * con_w_unit
                pygame.draw.line(self.screen, grid_color, (v, con_rect.y), (v, con_rect.y + con_rect.height))

                # Draw horizontal lines
                h = con_rect.y + i * con_h_unit
                pygame.draw.line(self.screen, grid_color, (con_rect.x, h), (con_rect.x + con_rect.width, h))

        stick_radius = min(con_w_unit, con_h_unit)

        # Left stick
        left_stick_pos = Vec2(con_rect.x + con_w_unit * 1, con_rect.y + 5 * con_h_unit)
        left_point = left_stick_pos + Vec2(stick_radius * self.controller.get_axis('LX'), stick_radius * self.controller.get_axis('LY'))

        pygame.draw.circle(self.screen, colors.WHITE, left_stick_pos.get(), 3)
        pygame.draw.circle(self.screen, colors.WHITE, left_stick_pos.get(), stick_radius, width=1)
        pygame.draw.line(self.screen, colors.WHITE, left_stick_pos.get(), left_point.get(), width=1)
        pygame.draw.circle(self.screen, colors.empty_beer, left_point.get(), 5)

        # Right stick
        right_stick_pos = Vec2(con_rect.x + con_w_unit * 6, con_rect.y + con_h_unit * 8)
        right_point = right_stick_pos + Vec2(stick_radius * self.controller.get_axis('RX'), stick_radius * self.controller.get_axis('RY'))

        pygame.draw.circle(self.screen, colors.WHITE, right_stick_pos.get(), 3)
        pygame.draw.circle(self.screen, colors.WHITE, right_stick_pos.get(), stick_radius, width=1)
        pygame.draw.line(self.screen, colors.WHITE, right_stick_pos.get(), right_point.get(), width=1)
        pygame.draw.circle(self.screen, colors.beer, right_point.get(), 5)

        # Draw A, B, X, Y buttons
        button_radius = con_w_unit * 0.5
        button_pos = Vec2(con_rect.x + con_w_unit * 8, con_rect.y + con_h_unit * 5)
        pygame.draw.circle(self.screen, colors.GREEN, (button_pos + Vec2(0, button_radius * 2)).get(),
                           radius=button_radius, width=0 if self.controller.get_button("A") else 1)
        pygame.draw.circle(self.screen, colors.RED, (button_pos + Vec2(button_radius * 2, 0)).get(),
                           radius=button_radius, width=0 if self.controller.get_button("B") else 1)
        pygame.draw.circle(self.screen, colors.YELLOW, (button_pos - Vec2(0, button_radius * 2)).get(),
                           radius=button_radius, width=0 if self.controller.get_button("Y") else 1)
        pygame.draw.circle(self.screen, colors.BLUE, (button_pos - Vec2(button_radius * 2, 0)).get(),
                           radius=button_radius, width=0 if self.controller.get_button("X") else 1)

        # Draw START, SELECT, HOME buttons
        start_radius = button_radius * 0.5
        center_button_pos = Vec2(con_rect.x + con_w_unit * 5, con_rect.y + con_h_unit * 5)
        pygame.draw.circle(self.screen, colors.get_gray(150), (center_button_pos + Vec2(button_radius, 0)).get(),
                           radius=start_radius, width=0 if self.controller.get_button("START") else 1)
        pygame.draw.circle(self.screen, colors.get_gray(150), (center_button_pos - Vec2(button_radius, 0)).get(),
                           radius=start_radius, width=0 if self.controller.get_button("SELECT") else 1)
        pygame.draw.circle(self.screen, colors.get_gray(150), (center_button_pos - Vec2(0, button_radius * 2)).get(),
                           radius=button_radius, width=0 if self.controller.get_button("HOME") else 1)

        # Draw Bumper buttons
        left_bumper_pos = Vec2(con_rect.x + con_w_unit, con_rect.y + con_h_unit)
        pygame.draw.rect(self.screen, colors.silver, pygame.rect.Rect(left_bumper_pos.x, left_bumper_pos.y, con_w_unit, con_h_unit),
                         width=0 if self.controller.get_button("LB") else 1)
        right_bumper_pos = Vec2(con_rect.x + con_w_unit * 8, con_rect.y + con_h_unit)
        pygame.draw.rect(self.screen, colors.silver, pygame.rect.Rect(right_bumper_pos.x, right_bumper_pos.y, con_w_unit, con_h_unit),
                         width=0 if self.controller.get_button("RB") else 1)

        # Draw Triggers
        lt_val = ((1 + self.controller.get_axis("LT")) / 2.0)
        lt_rect = pygame.rect.Rect(left_bumper_pos.x, con_rect.y, con_w_unit * lt_val, con_h_unit)
        pygame.draw.rect(self.screen, colors.vivid_cerulean, (lt_rect.x, lt_rect.y, con_w_unit, lt_rect.height), width=1)
        if lt_val > 0.01:
            pygame.draw.rect(self.screen, colors.vivid_cerulean, lt_rect, width=0)

        rt_val = ((1 + self.controller.get_axis("RT")) / 2.0)
        rt_rect = pygame.rect.Rect(right_bumper_pos.x, con_rect.y, con_w_unit * rt_val, con_h_unit)
        pygame.draw.rect(self.screen, colors.vivid_cerulean, (rt_rect.x, rt_rect.y, con_w_unit, rt_rect.height), width=1)
        if rt_val > 0.01:
            pygame.draw.rect(self.screen, colors.vivid_cerulean, rt_rect, width=0)

        # Draw D-Pad (9 options)
        def draw_hat(row, col, condition):
            hat_start_pos = Vec2(con_rect.x + con_w_unit * 2, con_rect.y + con_h_unit * 6)
            hat_rect = pygame.rect.Rect(hat_start_pos.x + col * con_w_unit, hat_start_pos.y + row * con_h_unit, con_w_unit, con_h_unit)
            pygame.draw.rect(self.screen, colors.get_gray(150), hat_rect, width=0 if condition else 1)

        draw_hat(0, 0, self.controller.get_hat("LEFT") and self.controller.get_hat("UP"))
        draw_hat(0, 1, self.controller.get_hat("UP"))
        draw_hat(0, 2, self.controller.get_hat("UP") and self.controller.get_hat("RIGHT"))

        draw_hat(1, 0, self.controller.get_hat("LEFT"))
        draw_hat(1, 1, not self.controller.get_hat("LEFT") and not self.controller.get_hat("RIGHT") and not self.controller.get_hat("UP") and not self.controller.get_hat("DOWN"))
        draw_hat(1, 2, self.controller.get_hat("RIGHT"))

        draw_hat(2, 0, self.controller.get_hat("LEFT") and self.controller.get_hat("DOWN"))
        draw_hat(2, 1, self.controller.get_hat("DOWN"))
        draw_hat(2, 2, self.controller.get_hat("DOWN") and self.controller.get_hat("RIGHT"))

    def print_debug(self):

        button_x_pos = 20
        axis_x_pos = 200
        hat_val_x_pos = 600

        for i, button in enumerate(self.controller.button_map):
            color = colors.GREEN if self.controller.get_button(button) else colors.alabaster
            self.debug_font.render_to(self.screen, (button_x_pos, int(self.height * 0.5) + (20 * i)), f"{button}: {self.controller.button_map[button]} :"
                                                                                                      f" {self.controller.get_button(button)}", color)

        for i, axis in enumerate(self.controller.axis_map):
            ax_val = self.controller.get_axis(axis)
            color = colors.pink if abs(ax_val) > 0.5 else colors.alabaster
            axis_str = f"{axis}: {self.controller.axis_map[axis]} : {format(ax_val, '5.4f')}"
            self.debug_font.render_to(self.screen, (axis_x_pos, int(self.height * 0.5) + (20 * i)), axis_str, color)

        for i, hat in enumerate(self.controller.hat_map):
            color = colors.byzantine if self.controller.get_hat(hat) else colors.alabaster
            self.debug_font.render_to(self.screen, (hat_val_x_pos, int(self.height * 0.5) + (20 * i)), f"{hat}: {self.controller.get_hat(hat)}", color)

        x, y = 40, self.height - 40
        radius = 10
        x_inc = 30
        for status in self.debug_sequencer.seq_status:
            width = 0 if status else 1
            pygame.draw.circle(self.screen, colors.GREEN, (x, y), radius, width)
            x += x_inc


if __name__ == "__main__":
    ControllerTest(800, 800)
