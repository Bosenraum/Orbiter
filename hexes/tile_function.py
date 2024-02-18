

class TileFunction:

    __TILE_FUNCTIONS = 0

    def __init__(self):
        TileFunction.__TILE_FUNCTIONS += 1
        self.id = TileFunction.__TILE_FUNCTIONS

    def activate(self):
        print(f"Tile {self.id} Activated")
