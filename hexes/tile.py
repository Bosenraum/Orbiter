

class Tile:
    def __init__(self, representation, function):
        self.representation = representation
        self.function = function
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def activate(self):
        self.function.activate()

    def draw(self, screen):
        self.representation.draw(screen)
