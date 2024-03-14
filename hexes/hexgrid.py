import random

import engine.snippets as snips

from tile import Tile
from tile_representation import *
from tile_function import TileFunction

# from perlin_noise import PerlinNoise
import numpy as np
import noise


class HexGrid:
    def __init__(self, position, width, height, clip_plane=None, seed=None):
        self.position = position
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.clip_plane = clip_plane

        self.selected_tile = None

        self.tiles = [[] for _ in range(width)]
        for col in self.tiles:
            [col.append(None) for _ in range(height)]

        # self.noise = PerlinNoise(octaves=10, seed=1)
        self.pnoise = self.generate_perlin_noise(self.width, self.height, scale=100, octaves=24, seed=seed)
        self.initialize_tiles()
        self.update_neighbors()
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

    def check_tile_intersect(self, position) -> Tile:
        for tile in self.iterate_tiles():
            if tile.intersect(position):
                return tile

        return None

    def get_tile_offset(self, row, col):
        x_shift = GlobalTileProperties.apothem if row % 2 == 0 else 0
        x_offset = col * GlobalTileProperties.side_length * math.sqrt(3) + x_shift
        y_offset = row * GlobalTileProperties.side_length * 3 / 2

        x_offset += GlobalTileProperties.abs_offset[0]
        y_offset += GlobalTileProperties.abs_offset[1]

        return x_offset, y_offset

    def initialize_tiles(self):
        GlobalTileProperties.recalc_needed = True
        for row in range(self.width):
            for col in range(self.height):

                x_offset, y_offset = self.get_tile_offset(row, col)

                elevation = self.pnoise[row][col]
                c = colors.get_gray(elevation)

                tile_type = -1
                tile_type = random.choice((0, 1))

                if tile_type == 0:
                    representation = WaterTileRep((x_offset, y_offset))
                elif tile_type == 1:
                    representation = GrassTileRep((x_offset, y_offset))
                else:
                    representation = TileRepresentation((x_offset, y_offset), color=c)

                functionality = TileFunction(elevation)  # Placeholder, will be updated after creation
                tile = Tile(row, col, representation, functionality)
                representation.tile = tile
                functionality.tile = tile
                self.tiles[row][col] = tile

                # tile.activate()

        GlobalTileProperties.recalc_needed = False

    def get_tile_rep(self):
        return self.get_tile(0, 0).representation

    def get_tile(self, row, col) -> Tile:
        if row < len(self.tiles) and col < len(self.tiles[0]):
            return self.tiles[row][col]
        else:
            return None

    def get_offset(self):
        return GlobalTileProperties.abs_offset

    def move(self, position):
        GlobalTileProperties.set_abs_offset(position)

    def zoom(self, amount):
        zoom_amount = amount * 0.1 * GlobalTileProperties.side_length
        GlobalTileProperties.zoom(zoom_amount)

    def update_neighbors(self):
        for tile in self.iterate_tiles():
            self.set_neighbors(tile)

    def even_row_offsets(self, row, col):
        neighbor_offsets = [
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col),
            (row + 1, col + 1)
        ]
        return neighbor_offsets

    def odd_row_offsets(self, row, col):
        neighbor_offsets = [
            (row - 1, col),
            (row - 1, col - 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col),
            (row + 1, col - 1)
        ]
        return neighbor_offsets

    def set_neighbors(self, tile):
        row = tile.row
        col = tile.col

        neighbor_offsets = self.odd_row_offsets(row, col) if row % 2 else self.even_row_offsets(row, col)

        tile = self.get_tile(row, col)
        if not tile:
            return None

        for npos in neighbor_offsets:
            neighbor_tile = self.get_tile(npos[0], npos[1])
            if neighbor_tile:
                tile.add_neighbor(neighbor_tile)

    # def get_neighbors(self, row, col):
    #     tile = self.get_tile(row, col)
    #     return tile.neighbors

    def get_neighbors(self, tile, depth=1):
        all_neighbors = tile.get_neighbors()
        to_visit = {tile}
        visited = set()

        for i in range(depth):
            neighbors = set()
            for t in list(to_visit):
                if t in visited:
                    continue

                [neighbors.add(n) for n in t.get_neighbors()]
                visited.add(t)
            all_neighbors += list(neighbors)
            to_visit = neighbors

        return all_neighbors

    def wrap_coordinates(self, row, col):
        # Implement wrapping logic here
        pass

    def iterate_tiles(self):
        for row in range(self.width):
            for col in range(self.height):
                yield self.tiles[row][col]

    def draw(self, screen):
        for tile in self.iterate_tiles():

            x_offset, y_offset = self.get_tile_offset(tile.row, tile.col)
            if not self.clip(tile):
                tile.draw(screen, (x_offset, y_offset))

        GlobalTileProperties.recalc_needed = False

    def clip(self, tile):
        return False

        if self.clip_plane is None:
            return False

        tx = tile.get_center()[0]
        ty = tile.get_center()[1]
        side_length = GlobalTileProperties.side_length

        x_inbounds = 0 - side_length < tx < self.clip_plane[0] + side_length
        y_inbounds = 0 - side_length < ty < self.clip_plane[1] + side_length
        return not (x_inbounds and y_inbounds)
