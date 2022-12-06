import sys
import json
from enum import Enum, auto

import pygame

from engine.engine import Engine
import engine.colors as colors
from engine.vector import Vec2


# Input map
BUTTON_MAP = {
    "A": None,
    "B": None,
    "X": None,
    "Y": None,
    "START": None,
    "SELECT": None,
    "RB": None,
    "LB": None,
    "RSTICK": None,
    "LSTICK": None,
    "HOME": None
}

AXIS_MAP = {
    "RX": None,
    "RY": None,
    "LX": None,
    "LY": None,
    "RT": None,
    "LT": None
}


def map_controller():
    global BUTTON_MAP, AXIS_MAP

    for button in BUTTON_MAP:
        print(f"Press the {button} button. ", end="")
        count = 0
        button_value = None

        if not BUTTON_MAP[button]:

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if count == 0:
                        button_value = event.button
                        print(f"Got {button_value}. Confirm: ", end="")
                        count += 1
                    else:
                        if event.button == button_value:
                            print(f"{button_value} +")
                            BUTTON_MAP[button] = button_value
                        else:
                            print(f"Button mismatch! Got:{event.button} Expected:{button_value} -")
                            print(f"")

    print(f"Button Map: {BUTTON_MAP}")


def save_input_map(in_map, filename="./controller_test/controller_map.json"):
    with open(filename, "w+") as map_file:
        print(f"Saving input map to {filename}")
        json.dump(in_map, map_file, indent=4)


def load_input_map(filename="./controller_test/controller_map.json"):
    with open(filename, "r") as map_file:
        in_map = json.load(map_file)
    return in_map


class ControllerTest(Engine):

    button_map = BUTTON_MAP
    axis_map = AXIS_MAP

    def __init__(self, width, height):
        self.joy = None

        self.square = None
        self.square_pos = None
        self.square_color_index = None
        self.square_motion = None
        self.square_color = None
        self.square_colors = None

        self.button_index = 0
        self.button_list = list(self.button_map.keys())
        self.button_map_done = False
        self.btn_input = {}

        self.axis_index = 0
        self.axis_list = list(self.axis_map.keys())
        self.axis_defaults = {}
        self.axis_map_start = False
        self.axis_map_done = False
        self.ax_input = {}

        self.axis_deadzone = 0.1
        self.axis_friction = 0.001
        self.gravity = 0.0

        self.hat_input = {}

        self.rumble_enable = False

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

    def get_axis_vals(self):
        ax_map = {}
        for ax in range(self.joy.get_numaxes()):
            ax_map[ax] = self.joy.get_axis(ax)

        return ax_map

    def get_button_vals(self):
        btn_map = {}
        for btn in range(self.joy.get_numbuttons()):
            btn_map[btn] = self.joy.get_button(btn)

        return btn_map

    def get_hat_vals(self):
        hat_map = {}
        for hat in range(self.joy.get_numhats()):
            h0, h1 = self.joy.get_hat(hat)
            # HAT X Axis
            if h0 == -1:
                hat_map["LEFT"] = 1
                hat_map["RIGHT"] = 0
            if h0 == 1:
                hat_map["LEFT"] = 0
                hat_map["RIGHT"] = 1
            if h0 == 0:
                hat_map["LEFT"] = 0
                hat_map["RIGHT"] = 0

            # HAT Y Axis
            if h1 == -1:
                hat_map["DOWN"] = 1
                hat_map["UP"] = 0
            if h1 == 1:
                hat_map["DOWN"] = 0
                hat_map["UP"] = 1
            if h1 == 0:
                hat_map["DOWN"] = 0
                hat_map["UP"] = 0

        return hat_map

    def get_button(self, btn_name):
        if btn_name in self.button_map:
            if self.button_map[btn_name] is not None:
                return self.btn_input[self.button_map[btn_name]]
            else:
                return 0
        else:
            print(f"Could not find {btn_name} in button_map. Check names.")
            return 0

    def get_axis(self, ax_name):
        if ax_name in self.axis_map:
            if self.axis_map[ax_name] is not None:
                return self.ax_input[self.axis_map[ax_name]]
            else:
                return 0.0
        else:
            print(f"Could not find {ax_name} in axis_map. Check names.")
            return 0.0

    def get_hat(self, hat_name):
        if hat_name in self.hat_input:
            return self.hat_input[hat_name]
        else:
            print(f"Could not find {hat_name} in hat map. Check names.")
            return 0

    def process_joystick_inputs(self, event):
        if event.type == pygame.JOYBUTTONUP:
            print(event)
            # Secret load mapping input Press Start + LT
            if event.button == 7:
                if self.ax_input[4] > 0.8:
                    in_map = load_input_map()
                    self.button_map = in_map.get("button_map", {})
                    self.axis_map = in_map.get("axis_map", {})
                    self.button_map_done = True
                    self.axis_map_done = True

        if event.type == pygame.JOYBUTTONDOWN:
            print(event)

            if not self.button_map_done:
                self.button_map[self.button_list[self.button_index]] = event.button
                self.button_index += 1
                if self.button_index >= len(self.button_list):
                    self.button_map_done = True

                # Skip other button inputs
                return

            if event.button == self.button_map["A"]:
                self.square_color = colors.GREEN
                if not self.axis_map_done:
                    self.axis_map_start = True
                    self.axis_defaults = self.ax_input
                    print(f"Defaults set to {self.ax_input}")
                self.square_motion.y = -0.30
            elif event.button == self.button_map["B"]:
                self.square_color = colors.RED
                if self.gravity == 0.0:
                    self.gravity = 0.0981
                else:
                    self.gravity = 0.0
            elif event.button == self.button_map["X"]:
                self.square_color = colors.BLUE
                self.rumble_enable = True
            elif event.button == self.button_map["Y"]:
                self.square_color = colors.YELLOW
                self.rumble_enable = False
            else:
                self.square_color_index = (self.square_color_index + 1) % len(self.square_colors)
                # self.square_color = self.square_colors[self.square_color_index]
                self.square_color = colors.get_random_color((20, 230), (20, 230), (20, 230))

        if event.type == pygame.JOYAXISMOTION:
            if not self.button_map_done or not self.axis_map_done:
                # Don't accept axis inputs until button mapping is done
                return

            # print(event)

            if event.axis == self.axis_map["LX"]:
                self.square_motion.x = event.value
            elif event.axis == self.axis_map["LY"]:
                self.square_motion.y = event.value

        if event.type == pygame.JOYHATMOTION:
            print(event)
            if self.hat_input["LEFT"]:
                self.square_pos = Vec2(50, 50)
                self.square_motion = Vec2(0, 0)
                self.square_color = colors.alabaster

        if event.type == pygame.JOYBALLMOTION:
            print(event)

    def on_update(self, elapsed_time):

        self.ax_input = self.get_axis_vals()
        self.btn_input = self.get_button_vals()
        self.hat_input = self.get_hat_vals()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type not in [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION]:
                print(event)
            self.process_joystick_inputs(event)

        self.map_axes()
        if self.rumble_enable:
            self.joy.rumble((1 + self.get_axis('LT')) * 0.5, (1 + self.get_axis('RT')) * 0.5, 0)
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
        left_point = left_stick_pos + Vec2(stick_radius * self.get_axis('LX'), stick_radius * self.get_axis('LY'))

        pygame.draw.circle(self.screen, colors.WHITE, left_stick_pos.get(), 3)
        pygame.draw.circle(self.screen, colors.WHITE, left_stick_pos.get(), stick_radius, width=1)
        pygame.draw.line(self.screen, colors.WHITE, left_stick_pos.get(), left_point.get(), width=1)
        pygame.draw.circle(self.screen, colors.empty_beer, left_point.get(), 5)

        # Right stick
        right_stick_pos = Vec2(con_rect.x + con_w_unit * 6, con_rect.y + con_h_unit * 8)
        right_point = right_stick_pos + Vec2(stick_radius * self.get_axis('RX'), stick_radius * self.get_axis('RY'))

        pygame.draw.circle(self.screen, colors.WHITE, right_stick_pos.get(), 3)
        pygame.draw.circle(self.screen, colors.WHITE, right_stick_pos.get(), stick_radius, width=1)
        pygame.draw.line(self.screen, colors.WHITE, right_stick_pos.get(), right_point.get(), width=1)
        pygame.draw.circle(self.screen, colors.beer, right_point.get(), 5)

        # Draw A, B, X, Y buttons
        button_radius = con_w_unit * 0.5
        button_pos = Vec2(con_rect.x + con_w_unit * 8, con_rect.y + con_h_unit * 5)
        pygame.draw.circle(self.screen, colors.GREEN, (button_pos + Vec2(0, button_radius * 2)).get(),
                           radius=button_radius, width=0 if self.get_button("A") else 1)
        pygame.draw.circle(self.screen, colors.RED, (button_pos + Vec2(button_radius * 2, 0)).get(),
                           radius=button_radius, width=0 if self.get_button("B") else 1)
        pygame.draw.circle(self.screen, colors.YELLOW, (button_pos - Vec2(0, button_radius * 2)).get(),
                           radius=button_radius, width=0 if self.get_button("Y") else 1)
        pygame.draw.circle(self.screen, colors.BLUE, (button_pos - Vec2(button_radius * 2, 0)).get(),
                           radius=button_radius, width=0 if self.get_button("X") else 1)

        # Draw START, SELECT, HOME buttons
        start_radius = button_radius * 0.5
        center_button_pos = Vec2(con_rect.x + con_w_unit * 5, con_rect.y + con_h_unit * 5)
        pygame.draw.circle(self.screen, colors.get_gray(150), (center_button_pos + Vec2(button_radius, 0)).get(),
                           radius=start_radius, width=0 if self.get_button("START") else 1)
        pygame.draw.circle(self.screen, colors.get_gray(150), (center_button_pos - Vec2(button_radius, 0)).get(),
                           radius=start_radius, width=0 if self.get_button("SELECT") else 1)
        pygame.draw.circle(self.screen, colors.get_gray(150), (center_button_pos - Vec2(0, button_radius * 2)).get(),
                           radius=button_radius, width=0 if self.get_button("HOME") else 1)

        # Draw Bumper buttons
        left_bumper_pos = Vec2(con_rect.x + con_w_unit, con_rect.y + con_h_unit)
        pygame.draw.rect(self.screen, colors.silver, pygame.rect.Rect(left_bumper_pos.x, left_bumper_pos.y, con_w_unit, con_h_unit),
                         width=0 if self.get_button("LB") else 1)
        right_bumper_pos = Vec2(con_rect.x + con_w_unit * 8, con_rect.y + con_h_unit)
        pygame.draw.rect(self.screen, colors.silver, pygame.rect.Rect(right_bumper_pos.x, right_bumper_pos.y, con_w_unit, con_h_unit),
                         width=0 if self.get_button("RB") else 1)

        # Draw Triggers
        lt_val = ((1 + self.get_axis("LT")) / 2.0)
        lt_rect = pygame.rect.Rect(left_bumper_pos.x, con_rect.y, con_w_unit * lt_val, con_h_unit)
        pygame.draw.rect(self.screen, colors.vivid_cerulean, (lt_rect.x, lt_rect.y, con_w_unit, lt_rect.height), width=1)
        if lt_val > 0.01:
            pygame.draw.rect(self.screen, colors.vivid_cerulean, lt_rect, width=0)

        rt_val = ((1 + self.get_axis("RT")) / 2.0)
        rt_rect = pygame.rect.Rect(right_bumper_pos.x, con_rect.y, con_w_unit * rt_val, con_h_unit)
        pygame.draw.rect(self.screen, colors.vivid_cerulean, (rt_rect.x, rt_rect.y, con_w_unit, rt_rect.height), width=1)
        if rt_val > 0.01:
            pygame.draw.rect(self.screen, colors.vivid_cerulean, rt_rect, width=0)

        # Draw D-Pad (9 options)
        def draw_hat(row, col, condition):
            hat_start_pos = Vec2(con_rect.x + con_w_unit * 2, con_rect.y + con_h_unit * 6)
            hat_rect = pygame.rect.Rect(hat_start_pos.x + col * con_w_unit, hat_start_pos.y + row * con_h_unit, con_w_unit, con_h_unit)
            pygame.draw.rect(self.screen, colors.get_gray(150), hat_rect, width=0 if condition else 1)

        draw_hat(0, 0, self.get_hat("LEFT") and self.get_hat("UP"))
        draw_hat(0, 1, self.get_hat("UP"))
        draw_hat(0, 2, self.get_hat("UP") and self.get_hat("RIGHT"))

        draw_hat(1, 0, self.get_hat("LEFT"))
        draw_hat(1, 1, not self.get_hat("LEFT") and not self.get_hat("RIGHT") and not self.get_hat("UP") and not self.get_hat("DOWN"))
        draw_hat(1, 2, self.get_hat("RIGHT"))

        draw_hat(2, 0, self.get_hat("LEFT") and self.get_hat("DOWN"))
        draw_hat(2, 1, self.get_hat("DOWN"))
        draw_hat(2, 2, self.get_hat("DOWN") and self.get_hat("RIGHT"))

    def save_input_map(self):
        in_map = {**self.button_map, **self.axis_map}
        save_input_map(in_map)

    def map_axes(self):
        if not self.axis_map_done and self.axis_map_start:
            max_delta = 0.0
            max_axis = None
            # Get the position of all axes
            for ax, ax_val in self.ax_input.items():
                ax_delta = abs(abs(self.axis_defaults[ax]) - abs(ax_val))
                if ax_delta >= max_delta:
                    max_delta = ax_delta
                    max_axis = ax

            if not self.engTimers[0].is_running() and max_delta >= 0.75:
                self.axis_map[self.axis_list[self.axis_index]] = max_axis
                self.axis_index += 1
                self.engTimers[0].set(1.0)
                if self.axis_index >= len(self.axis_list):
                    self.axis_map_done = True
                    self.save_input_map()

    def print_debug(self):
        debug_loc = Vec2(20, self.height - 20)
        debug_str = f"Input mapping complete."
        if not self.button_map_done:
            debug_str = f"Press the {self.button_list[self.button_index]} button."
        elif not self.axis_map_done:
            if not self.axis_map_start:
                debug_str = f"Release all axes and press A"
            else:
                debug_str = f"Use the {self.axis_list[self.axis_index]} axis."
        self.debug_font.render_to(self.screen, debug_loc.get(), debug_str, colors.WHITE)

        for i, button in enumerate(self.button_map):
            color = colors.GREEN if self.get_button(button) else colors.alabaster
            self.debug_font.render_to(self.screen, (20, int(self.height * 0.5) + (20 * i)), f"{button}: {self.button_map[button]}", color)

        i = 0
        for axis in self.axis_map:
            ax_num = self.axis_map[axis]
            if ax_num in self.ax_input:
                ax_val = self.ax_input[ax_num]
                axis_str = f"{axis}: {ax_num} : {format(ax_val, '5.4f')}"
            else:
                axis_str = f"{axis}: None : None"
            self.debug_font.render_to(self.screen, (200, int(self.height * 0.5) + (20 * i)), axis_str, colors.alabaster)
            i += 1

        i = 0
        for ax, val in self.ax_input.items():
            ax_str = f"{ax}: {format(val, '5.4f')}"
            self.debug_font.render_to(self.screen, (400, int(self.height * 0.5) + (20 * i)), ax_str, colors.alabaster)
            if ax in self.axis_defaults:
                self.debug_font.render_to(self.screen, (600, int(self.height * 0.5) + (20 * i)), f"Def {ax}: {round(self.axis_defaults[ax], 4)}", colors.GREEN)
            i += 1

        # self.debug_font.render_to(self.screen, (20, int(self.height * 0.5)), str(self.button_map), colors.WHITE)
        # self.debug_font.render_to(self.screen, (20, int(self.height * 0.5) + 20), str(self.axis_map), colors.alabaster)


if __name__ == "__main__":
    ControllerTest(800, 800)