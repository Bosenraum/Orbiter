import random

import engine.snippets as snips

from tile import Tile
from tile_representation import *
from tile_function import TileFunction

# from perlin_noise import PerlinNoise
import numpy as np
import noise


class Band:

    def __init__(self, name, elevation, color):
        self.name = name
        self.elevation = elevation
        self.color = color


class HexGrid:
    def __init__(self, width, height, clip_plane=None, seed=None):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.clip_plane = clip_plane

        self.selected_tile = None

        self.bands = {
            "ocean": Band("ocean", 33, colors.Blue.ocean),
            "beach": Band("beach", 50, colors.Yellow.goldenrod),
            "grass": Band("grass", 80, colors.Green.grass),
            "hills": Band("hills", 100, colors.Brown.saddle_brown)
        }

        self.tiles = [[] for _ in range(width)]
        for col in self.tiles:
            [col.append(None) for _ in range(height)]

        # self.noise = PerlinNoise(octaves=10, seed=1)
        self.pnoise = self.generate_perlin_noise(self.width, self.height, scale=100, octaves=24, seed=seed)
        self.initialize_tiles()
        # self.gtp = GlobalTileProperties()

    # TODO: Move to engine utils
    def generate_perlin_noise(self, width, height, scale=100, octaves=10, persistance=0.5, lacunarity=2.5, seed=None):
        print(f"Generating Perlin Noise with seed={seed}")
        perlin_values = np.zeros((height, width))

        if seed is None:
            seed = np.random.randint(0, 10000)
            print(seed)

        for y in range(height):
            for x in range(width):
                perlin_values[y][x] = noise.pnoise2(x/scale, y/scale, octaves=octaves,
                                                    persistence=persistance, lacunarity=lacunarity,
                                                    repeaty=2048, repeatx=2048, base=seed)

        # perlin_values = np.interp(perlin_values, (perlin_values.min(), perlin_values.max()), (0, 255))
        # return perlin_values.astype(int)

        # print(f"min={perlin_values.min()}, max={perlin_values.max()}")
        perlin_values = np.interp(perlin_values, (perlin_values.min(), perlin_values.max()), (0, 100))
        return perlin_values

    def get_band(self, value):
        # Want the band with elevation closest to value while being greater than value
        output_band = self.bands["hills"]
        for band in self.bands.values():
            if band.elevation > value:
                return band

        return output_band

    def set_bands(self, bands):
        for band, elevation in bands.items():
            self.bands[band].elevation = elevation

        self.update_tiles()

    def update_tiles(self):
        for tile in self.iterate_tiles():
            tile.set_band(self.get_band(tile.get_elevation()))

    def check_tile_intersect(self, position) -> Tile:
        for tile in self.iterate_tiles():
            if tile.intersect(position):
                return tile

        return None

    def initialize_tiles(self):
        for row in range(self.width):
            for col in range(self.height):
                # representation = TileRepresentation((row, col))  # Placeholder, will be updated after creation
                # r = 200 * (row / self.width) + 55
                # g = 200 * (col / self.height) + 55
                # b = 0
                # c = colors.get_gray(self.noise([row/self.width, col/self.height]) * 215 + 40)
                # representation = TileRepresentation((row, col), color=(r, g, b))

                elevation = self.pnoise[row][col]
                band = self.get_band(elevation)
                c = colors.get_gray(elevation)

                tile_type = -1
                # tile_type = random.choice((0, 1))

                if tile_type == 0:
                    representation = WaterTileRep((row, col))
                elif tile_type == 1:
                    representation = GrassTileRep((row, col))
                else:
                    representation = TileRepresentation((row, col), color=band.color)

                functionality = TileFunction(elevation)  # Placeholder, will be updated after creation
                tile = Tile(representation, functionality)
                representation.tile = tile
                functionality.tile = tile
                self.tiles[row][col] = tile
                # tile.activate()

    def get_tile_rep(self):
        return self.get_tile(0, 0).representation

    def get_tile(self, row, col) -> Tile:
        return self.tiles[row][col]

    def get_offset(self):
        return GlobalTileProperties.abs_offset

    def move(self, position):
        GlobalTileProperties.set_abs_offset(position)

    def zoom(self, amount):
        zoom_amount = amount * 0.1 * GlobalTileProperties.side_length
        GlobalTileProperties.zoom(zoom_amount)

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
            if not self.clip(tile):
                tile.draw(screen)
            # else:
            #     print(f"TILE {tile.id} CLIPPED: {tile.get_center()}")
        GlobalTileProperties.recalc_needed = False

    def clip(self, tile):
        if self.clip_plane is None:
            return False

        tx = tile.get_center()[0]
        ty = tile.get_center()[1]
        side_length = GlobalTileProperties.side_length
        apothem = GlobalTileProperties.apothem

        x_inbounds = 0 - side_length < tx < self.clip_plane[0] + side_length
        y_inbounds = 0 - side_length < ty < self.clip_plane[1] + side_length
        return not (x_inbounds and y_inbounds)
