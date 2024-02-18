
from tile import Tile
from tile_representation import TileRepresentation
from tile_function import TileFunction


class HexGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.tiles = [[] for _ in range(width)]
        for col in self.tiles:
            [col.append(None) for _ in range(height)]
        self.initialize_tiles()

    def initialize_tiles(self):
        for row in range(self.width):
            for col in range(self.height):
                representation = TileRepresentation((row, col))  # Placeholder, will be updated after creation
                functionality = TileFunction()  # Placeholder, will be updated after creation
                tile = Tile(representation, functionality)
                representation.tile = tile
                functionality.tile = tile
                self.tiles[row][col] = tile
                # tile.activate()

    def get_tile(self, row, col):
        return self.tiles[row][col]

    def get_neighbors(self, row, col):
        tile = self.get_tile(row, col)
        pass
        # return tile.neighbors

    def wrap_coordinates(self, row, col):
        # Implement wrapping logic here
        pass

    def iterate_tiles(self):
        for row in range(self.width):
            for col in range(self.height):
                yield self.tiles[row][col]

    def draw(self, screen):
        for tile in self.iterate_tiles():
            tile.draw(screen)
