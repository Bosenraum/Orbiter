

class TileFunction:

    __TILE_FUNCTIONS = 0

    def __init__(self, elevation=0, band=None):
        TileFunction.__TILE_FUNCTIONS += 1
        self.id = TileFunction.__TILE_FUNCTIONS
        self.elevation = elevation
        self.band = band

    def activate(self):
        print(f"Tile {self.id} Activated")


