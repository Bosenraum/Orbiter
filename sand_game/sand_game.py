import pygame
import sys

from engine.engine import Engine
import engine.colors as colors


class SandEngine(Engine):
    APP_NAME = "SAND GAME"

    def __init__(self, width, height, **kwargs):
        self.debug = kwargs.get("debug", False)

        pf = 1
        super().__init__(width, height, pf)

    def process_key_inputs(self, ev: pygame.event.Event):
        if ev.key == pygame.K_SPACE:
            print(f"Pressed space.")

        # Debug toggle
        if ev.key == pygame.K_F1:
            self.debug = not self.debug

    def process_mouse_inputs(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            # Mouse down events
            pass
        if ev.type == pygame.MOUSEBUTTONUP:
            # Mouse up events
            pass

        if ev.type == pygame.MOUSEWHEEL:
            # Mousewheel events
            pass

        if ev.type == pygame.MOUSEMOTION:
            # Mouse motion events
            pass

    def on_start(self):
        pass

    def on_update(self, et):

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                sys.exit()

            # Process inputs
            if event.type == pygame.KEYDOWN:
                self.process_key_inputs(event)

            # Process mouse inputs
            self.process_mouse_inputs(event)

        self.screen.fill(colors.BLACK)

        pygame.display.update()


if __name__ == "__main__":
    SandEngine(500, 500)
