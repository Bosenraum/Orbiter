import json


class ControllerException(Exception):

    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class ButtonException(ControllerException):

    def __init__(self, btn_name):
        super().__init__(f"Button {btn_name} could not be found in the button map.")


class AxisException(ControllerException):

    def __init__(self, ax_name):
        super().__init__(f"Axis {ax_name} could not be found in the axis map.")


class HatException(ControllerException):

    def __init__(self, hat_name):
        super().__init__(f"Hat {hat_name} could not be found in the hat map.")


class Controller:
    BUTTON_DEFAULT = 0
    AXIS_DEFAULT = 0.0
    HAT_DEFAULT = 0

    # Input map
    BUTTON_MAP = {
        "A"     : None,
        "B"     : None,
        "X"     : None,
        "Y"     : None,
        "START" : None,
        "SELECT": None,
        "RB"    : None,
        "LB"    : None,
        "RSTICK": None,
        "LSTICK": None,
        "HOME"  : None
    }

    AXIS_MAP = {
        "RX": None,
        "RY": None,
        "LX": None,
        "LY": None,
        "RT": None,
        "LT": None
    }

    def __init__(self, joystick, **kwargs):
        # The pygame joystick we are wrapping
        self.joy = joystick
        self.button_map = None
        self.button_states = None
        self.axis_map = None
        self.axis_states = None
        self.hat_map = None
        self.hat_states = None
        self.axis_defaults = self.get_axis_default_vals()

        self.deadzone = kwargs.get("deadzone", 0.0)
        engine_path = "C:/Users/austi_000/Documents/Python/Orbiter"
        self.controller_map_file = kwargs.get("controller_map_file", f"{engine_path}/engine/config_data/xbox_one_map.json")
        self.load_config(self.controller_map_file)

        # TODO: Add rumble

    def set_joystick(self, joystick):
        self.joy = joystick

    def load_config(self, filepath):
        with open(filepath, "r") as in_file:
            config = json.load(in_file)

            self.update_config(config)

    def save_config(self, filepath):
        with open(filepath, "w+") as out_file:
            config = {**self.button_map, **self.axis_map, **self.hat_map}
            json.dump(config, filepath)

    def update_config(self, new_config):
        self.button_map = new_config.get("button_map", self.button_map)
        self.button_states = {btn: Controller.BUTTON_DEFAULT for btn in self.button_map}
        self.axis_map = new_config.get("axis_map", self.axis_map)
        self.axis_states = {ax: Controller.AXIS_DEFAULT for ax in self.axis_map}
        self.hat_map = new_config.get("hat_map", self.hat_map)
        self.hat_states = {hat: Controller.HAT_DEFAULT for hat in self.hat_map}

        self.update()

    # Update internal states based on event data
    def process_event(self, event):
        pass

    def get_button(self, btn_name):
        if btn_name in self.button_map:
            if self.button_map[btn_name] is not None:
                return self.button_states[self.button_map[btn_name]]
            else:
                return Controller.BUTTON_DEFAULT
        else:
            print(f"Button name: {btn_name}")
            print(f"Button map: {self.button_map}")
            raise ButtonException(btn_name)

    def get_axis(self, ax_name, get_default=False):
        if ax_name in self.axis_map:
            if self.axis_map[ax_name] is not None:
                if get_default:
                    return self.axis_defaults[self.axis_map[ax_name]]
                return self.axis_states[self.axis_map[ax_name]]
            else:
                return Controller.AXIS_DEFAULT
        else:
            print(f"Axis name: {ax_name}")
            print(f"Axis map: {self.axis_map}")
            raise AxisException(ax_name)

    def get_hat(self, hat_name):
        if hat_name in self.hat_map:
            if self.hat_states[hat_name] is not None:
                return self.hat_states[self.hat_map[hat_name]]
            else:
                return Controller.HAT_DEFAULT
        else:
            print(f"Hat name: {hat_name}")
            print(f"Hat map: {self.hat_map}")
            raise HatException(hat_name)

    # Capture current states of everything in our maps
    def update(self):
        self.button_states = self.get_button_vals()
        self.axis_states = self.get_axis_vals()
        self.hat_states = self.get_hat_vals()

    def get_axis_vals(self):
        ax_map = {}
        for ax in range(self.joy.get_numaxes()):
            ax_map[ax] = self.joy.get_axis(ax)

        return ax_map

    def get_axis_default_vals(self):
        return self.get_axis_vals()

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
