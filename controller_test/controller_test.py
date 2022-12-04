import sys

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

        self.axis_index = 0
        self.axis_list = list(self.axis_map.keys())
        self.axis_defaults = {}
        self.axis_map_start = False
        self.axis_map_done = False
        self.ax_input = {}

        self.axis_deadzone = 0.1
        self.axis_friction = 0.001
        self.gravity = 0.0

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

    def get_axis_vals(self):
        ax_map = {}
        for ax in range(self.joy.get_numaxes()):
            ax_map[ax] = self.joy.get_axis(ax)

        return ax_map

    def on_update(self, elapsed_time):

        self.ax_input = self.get_axis_vals()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.JOYBUTTONUP:
                print(event)

            if event.type == pygame.JOYBUTTONDOWN:
                print(event)

                if not self.button_map_done:
                    self.button_map[self.button_list[self.button_index]] = event.button
                    self.button_index += 1
                    if self.button_index >= len(self.button_list):
                        self.button_map_done = True

                    # Skip other button inputs
                    continue

                if event.button == self.button_map["A"]:
                    self.square_color = colors.GREEN
                    self.axis_map_start = True
                    self.axis_defaults = self.ax_input
                    print(f"Defaults set to {self.ax_input}")
                    self.square_motion.y = -0.30
                elif event.button == 1:
                    self.square_color = colors.RED
                    if self.gravity == 0.0:
                        self.gravity = 0.0981
                    else:
                        self.gravity = 0.0
                elif event.button == 2:
                    self.square_color = colors.BLUE
                elif event.button == 3:
                    self.square_color = colors.YELLOW
                else:
                    self.square_color_index = (self.square_color_index + 1) % len(self.square_colors)
                    self.square_color = self.square_colors[self.square_color_index]

            if event.type == pygame.JOYAXISMOTION:
                if not self.button_map_done or not self.axis_map_done:
                    # Don't accept axis inputs until button mapping is done
                    continue

                print(event)

                if event.axis == self.axis_map["LX"]:
                    self.square_motion.x = event.value
                elif event.axis == self.axis_map["LY"]:
                    self.square_motion.y = event.value

            if event.type == pygame.JOYHATMOTION:
                print(event)

        # Update the axis values for mapped axes
        ax_map = self.get_axis_vals()

        self.map_axes()

        self.screen.fill(colors.BLACK)
        self.print_debug()

        self.square_motion -= Vec2(self.axis_friction, self.axis_friction)

        if abs(self.square_motion.x) <= self.axis_deadzone:
            self.square_motion.x = 0.0
        if abs(self.square_motion.y) <= self.axis_deadzone:
            self.square_motion.y = self.gravity

        # Update position based on movement
        self.square_pos = self.square_pos + (self.square_motion * 10)
        self.square.update(self.square_pos.x, self.square_pos.y, 50, 50)
        pygame.draw.rect(self.screen, self.square_color, self.square)

        pygame.display.update()

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
            self.debug_font.render_to(self.screen, (20, int(self.height * 0.5) + (20 * i)), f"{button}: {self.button_map[button]}", colors.alabaster)

        i = 0
        for axis in self.axis_map:
            ax_num = self.axis_map[axis]
            if ax_num in self.ax_input:
                ax_val = self.ax_input[ax_num]
                axis_str = f"{axis}: {ax_num} : {format(ax_val, '5.4f')}"
            else:
                axis_str = f"{axis}: None : None"
            self.debug_font.render_to(self.screen, (120, int(self.height * 0.5) + (20 * i)), axis_str, colors.alabaster)
            i += 1

        i = 0
        for ax, val in self.ax_input.items():
            ax_str = f"{ax}: {format(val, '5.4f')}"
            self.debug_font.render_to(self.screen, (260, int(self.height * 0.5) + (20 * i)), ax_str, colors.alabaster)
            if ax in self.axis_defaults:
                self.debug_font.render_to(self.screen, (380, int(self.height * 0.5) + (20 * i)), f"Def {ax}: {round(self.axis_defaults[ax], 4)}", colors.GREEN)
            i += 1

        # self.debug_font.render_to(self.screen, (20, int(self.height * 0.5)), str(self.button_map), colors.WHITE)
        # self.debug_font.render_to(self.screen, (20, int(self.height * 0.5) + 20), str(self.axis_map), colors.alabaster)


if __name__ == "__main__":
    ControllerTest(500, 500)