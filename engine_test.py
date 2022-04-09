from engine import *


class DriverEngine(Engine):
    APP_NAME = "DriveEngine"

    def __init__(self, width, height, pf):
        super().__init__(width, height, pf)

    # called once before the loop begins
    def on_start(self):
        pass

    # called once per loop iteration
    def on_update(self, elapsed_time):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(BLACK)


if __name__ == "__main__":
    driver = DriverEngine(720, 480, 2)
    driver.start()
