

# hexgraph.py
import random
from tile import *
from tile_representation import *
from tile_function import *


class HexGraph:
    def __init__(self, num_tiles):
        self.tile_positions = set()
        self.seed_tile = None
        self.generate_graph(num_tiles)

    # Generates a neighbor tile at the given index or in convention order
    def generate_neighbor(self, tile, index=None, color=None):
        if not index:
            # If no index was given, find the first open neighbor starting clockwise from the top right.
            index = tile.get_first_open_neighbor_index()

        if tile.neighbors[index]:
            # filled neighbor slot, did not generate a tile
            return

        np = self.generate_neighbors_positions(tile)

        new_tile = None

        while not new_tile or new_tile.position in self.tile_positions:
            tile_rep = ScaleTileRep(np[index], color=color)
            tile_func = TileFunction()
            new_tile = Tile(tile_rep, tile_func)
            tile.add_neighbor(new_tile, index)
            new_tile.add_neighbor(tile, Tile.reverse_index(index))
            self.tile_positions.add(new_tile.position)

        return new_tile

    def generate_graph(self, num_tiles):
        seed_tile_rep = ScaleTileRep((0, 0), color=colors.Blue.electric_blue)  # Create a seed tile at position (0, 0)
        seed_tile_func = TileFunction()
        seed_tile = Tile(seed_tile_rep, seed_tile_func)
        self.seed_tile = seed_tile

        neighbor_pos = self.generate_neighbors_positions(self.seed_tile)

        self.tile_positions.add(self.seed_tile.position)  # Add the seed tile to the graph
        num_generated_tiles = 1

        tile_stack = [self.seed_tile]

        while num_generated_tiles < num_tiles:
            active_tile = tile_stack[0]
            # Choose a random tile from the existing tiles
            if active_tile.open_sides > 0:
                new_tile = self.generate_neighbor(active_tile, color=colors.get_gray(int(256 * num_generated_tiles/num_tiles)))
                tile_stack.append(new_tile)
                num_generated_tiles += 1
            else:
                tile_stack.pop(0)

        return seed_tile

    def generate_neighbors_positions(self, tile):
        row, col = tile.representation.position
        # Define the relative positions of the neighboring tiles
        neighbors_offsets = [
            (0, 1),    # Top-right
            (1, 0),     # Right
            (0, -1),     # Bottom-right
            (-1, -1),    # Bottom-left
            (-1, 0),    # Left
            (-1, 0),  # Top-left
        ]
        # Generate positions of neighbors relative to the current tile
        neighbors_positions = [(row + dr, col + dc) for dr, dc in neighbors_offsets]
        # print(neighbors_positions)
        return neighbors_positions

    def iterate_graph(self):
        tile_stack = [self.seed_tile]
        visited_tiles = set()

        while tile_stack:
            tile = tile_stack.pop(0)
            visited_tiles.add(tile)
            for t in tile.neighbors:
                if t and t not in visited_tiles:
                    tile_stack.append(t)
            yield tile

    def draw(self, screen):

        for tile in self.iterate_graph():
            tile.draw(screen)
        self.seed_tile.draw(screen)

