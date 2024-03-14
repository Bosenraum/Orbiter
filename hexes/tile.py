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

    def __init__(self, row, col, representation: TileRepresentation = None, function: TileFunction = None):
        self.row = row
        self.col = col
        self.id = TileIDService.inc_id()

        default_rep = TileRepresentation((0, 0), color=(0xFF, 0, 0))
        self.representation = [representation if representation else default_rep]

        default_func = TileFunction()
        self.function = [function if function else default_func]

        # Define a convention, list starts with top right side and moves around clockwise
        # self.neighbors = [None for _ in range(self.MAX_NEIGHBORS)]
        self.neighbors: {Tile} = set()

    def __repr__(self):
        return str(self.id)

    def add_neighbor(self, neighbor):
        if not isinstance(neighbor, self.__class__):
            return False

        self.neighbors.add(neighbor)
        # if self not in neighbor.neighbors:
        #     neighbor.add_neighbor(self)

        return True

    def get_neighbors(self):
        if self.neighbors:
            return list(self.neighbors)
        else:
            return []

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)

    @property
    def position(self):
        return self.representation[0].position

    def get_center(self):
        return self.representation[0].position

    def activate(self):
        self.function[0].activate()

    def get_elevation(self):
        return self.function[0].elevation

    def set_band(self, band):
        self.function.band = band
        self.representation.color = band.color

    def intersect(self, position) -> bool:
        return self.representation[0].intersect(position)

    def add_representation(self, rep: TileRepresentation):
        if rep:
            self.representation.insert(0, rep)

    def remove_representation(self):
        if len(self.representation) > 1:
            self.representation.pop(0)

    def draw(self, screen, offset=(0, 0)):
        self.representation[0].draw(screen, offset)
