import abc


class GameState(abc.ABC):

    def __init__(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def sim(self, game_input):
        pass

    def draw(self, surface):
        pass
