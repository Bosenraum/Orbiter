

class Timer:

    def __init__(self, timer_time):
        self._time = None
        self.running = False
        self.time = timer_time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, new_time):
        try:
            if new_time > 0.0:
                self._time = new_time
                self.running = True
            else:
                self._time = 0.0
                self.running = False
        except TypeError:
            print(f"Cannot set time to {new_time} (repr={repr(new_time)}")

    def tick(self, tick_time):
        if self.running:
            self.time -= tick_time

        return self.running

    def set(self, new_time):
        self.time = new_time

    def get(self):
        return self.time

    def is_running(self):
        return self.running


class TickTimer:

    def __init__(self, num_ticks):
        self._ticks = None
        self.running = False
        self.ticks = num_ticks

    @property
    def ticks(self):
        return self._ticks

    @ticks.setter
    def ticks(self, num_ticks):
        if isinstance(num_ticks, int):
            if num_ticks > 0:
                self._ticks = num_ticks
                self.running = True
            else:
                self._ticks = 0
                self.running = False
        else:
            print(f"Not setting ticks to {num_ticks} (repr={num_ticks})")

    def tick(self):
        if self.running:
            self.ticks -= 1
        return self.running

    def get(self):
        return self.ticks

    def set(self, num_ticks):
        self.ticks = num_ticks

    def is_running(self):
        return self.running