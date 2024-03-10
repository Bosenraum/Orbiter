import pygame

import engine.colors as colors

from hexes.states.game_state import GameState


class MenuState(GameState):

    def __init__(self, menu_text):
        self.menu_text = menu_text
        super().__init__()

    def enter(self):
        pass

    def exit(self):
        pass

    def sim(self, game_input):
        pass

    def draw(self, surface):
        font = pygame.freetype.SysFont(["consolas", "courier"], 48, bold=True)
        img, img_rect = font.render(f"{self.menu_text}", colors.BLACK, colors.Blue.ocean)
        surface.blit(img, (400, 400))

