import random
import typing

from tile_representation import TileRepresentation
from tile_function import TileFunction


class TileIDService:

    id_length = 4
    ids = {}
    seq_id = 0

    def __init__(self):
        pass

    @staticmethod
    def generate_id():
        # Generate a unique id
        guid = None
        while not guid or guid in TileIDService.ids:
            guid = "".join([str(random.randint(0, 9)) for _ in range(TileIDService.id_length)])
            print(f"Generated GUID: {guid}")

        return guid

    @staticmethod
    def inc_id():
        output_id = f"{TileIDService.seq_id:04d}"
        TileIDService.seq_id += 1
        return output_id


class TileSides:
    TR = 0
    R = 1
    BR = 2
    BL = 3
    L = 4
    TL = 5


# TODO: Make a tile factory
class Tile:

    MAX_NEIGHBORS = 6
    reverse_index_map = {
        TileSides.TR: TileSides.BL,
        TileSides.R: TileSides.L,
        TileSides.BR: TileSides.TL,
        TileSides.BL: TileSides.TR,
        TileSides.L: TileSides.R,
        TileSides.TL: TileSides.BR
    }

    def __init__(self, representation: TileRepresentation = None, function: TileFunction = None):
        self.id = TileIDService.inc_id()
        self.representation = representation if representation else TileRepresentation((0, 0), color=(0xFF, 0, 0))
        self.function = function if function else TileFunction()

        self.representation.id = self.id

        # Define a convention, list starts with top right side and moves around clockwise
        self.neighbors = [None for _ in range(self.MAX_NEIGHBORS)]

    def __repr__(self):
        return str(self.id)

    @staticmethod
    def reverse_index(index):
        # given a hex index, return the connecting index
        return Tile.reverse_index_map[index]

    def add_neighbor(self, neighbor, index):
        if neighbor and not self.neighbors[index]:
            self.neighbors[index] = neighbor
        else:
            print(f"Error adding neighbor {neighbor}")

    def remove_neighbor(self, neighbor):
        self.neighbors.pop(neighbor.id)

    def get_first_open_neighbor_index(self):
        for i, n in enumerate(self.neighbors):
            if not n:
                return i

    @property
    def open_sides(self):
        return self.neighbors.count(None)

    @property
    def position(self):
        return self.representation.position

    def get_center(self):
        return self.representation.get_center()

    def activate(self):
        self.function.activate()

    def get_elevation(self):
        return self.function.elevation

    def set_band(self, band):
        self.function.band = band
        self.representation.color = band.color

    def intersect(self, position) -> bool:
        return self.representation.intersect(position)

    def set_representation(self, rep: TileRepresentation):
        self.representation = rep

    def draw(self, screen):
        self.representation.draw(screen)
