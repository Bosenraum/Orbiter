# tile_representation.py
import pygame
import math

import engine.colors as colors
import engine.utils as utils


class GlobalTileProperties:

    abs_offset = (25, 25)
    side_length = 13
    recalc_needed = False

    f = math.sqrt(3) / 2
    phi = 3 * math.sqrt(3) / 2

    apothem = side_length * f
    debug = False

    def __init__(self):
        pass

    @staticmethod
    def get_properties():
        properties = {
            "offset": GlobalTileProperties.abs_offset,
            "side_length": GlobalTileProperties.side_length,
            "apothem": GlobalTileProperties.apothem,
            "f": GlobalTileProperties.f,
            "phi": GlobalTileProperties.phi
        }
        return properties

    @staticmethod
    def set_abs_offset(position):
        GlobalTileProperties.recalc_needed = not GlobalTileProperties.abs_offset == position
        GlobalTileProperties.abs_offset = position

    @staticmethod
    def move_abs_offset(delta):
        x = GlobalTileProperties.abs_offset[0] + delta[0]
        y = GlobalTileProperties.abs_offset[1] + delta[1]
        GlobalTileProperties.recalc_needed = not GlobalTileProperties.abs_offset == (x, y)
        GlobalTileProperties.abs_offset = (x, y)

    @staticmethod
    def zoom(amount):
        MIN_SIDE_LENGTH = 5
        MAX_SIDE_LENGTH = 500
        new_side_length = GlobalTileProperties.side_length + amount
        new_side_length = utils.clamp(MIN_SIDE_LENGTH, new_side_length, MAX_SIDE_LENGTH)

        GlobalTileProperties.recalc_needed = not GlobalTileProperties.side_length == new_side_length
        GlobalTileProperties.side_length = new_side_length
        GlobalTileProperties.apothem = GlobalTileProperties.side_length * GlobalTileProperties.f


class TileRepresentation:

    freetype_init = None
    id_font = None

    def __init__(self, position, color=None, outline_color=colors.BLACK):
        self.position = position
        self.color = color if color else colors.get_random_color((40, 200), (40, 200), (40, 200))  # Fill color of the hexagon
        self.outline_color = outline_color  # Outline color of the hexagon

        self.vertices = None

        self.recalc()

        if not TileRepresentation.freetype_init:
            pygame.freetype.init()
            TileRepresentation.freetype_init = True
            TileRepresentation.id_font = pygame.freetype.SysFont(["consolas", "courier"], 24, bold=True)

    def recalc(self):
        self.vertices = self.get_vertices()

    # Gets the list of vertices from the tile based on position and attributes
    def get_vertices(self, position=None):
        if position is None:
            position = self.position

        x_offset, y_offset = position

        # Calculate the vertices of the hexagon
        vertices = []
        rotation_angle = 30
        for i in range(6):
            angle_deg = 60 * i + rotation_angle
            angle_rad = math.radians(angle_deg)
            x = x_offset + GlobalTileProperties.side_length * math.cos(angle_rad)
            y = y_offset + GlobalTileProperties.side_length * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices

    def offset_vertices(self, offset):
        offx, offy = offset[0], offset[1]

        offset_vertices = []
        for vertex in self.vertices:
            x = vertex[0] + offx
            y = vertex[1] + offy
            offset_vertices.append((x, y))

        return offset_vertices

    def intersect(self, point):
        dist = utils.calc_distance(point,self.position)
        if dist <= GlobalTileProperties.apothem:
            return True
        return False

    def draw(self, screen, position):
        draw_pos = position
        # self.position = draw_pos
        draw_vertices = self.get_vertices(position)

        # Draw the hexagon
        pygame.draw.polygon(screen, self.color, draw_vertices)
        outline_width = int(GlobalTileProperties.side_length // 25)
        outline_width = utils.clamp(1, outline_width, 10)
        pygame.draw.polygon(screen, self.outline_color, draw_vertices, outline_width)

        if GlobalTileProperties.debug:
            # Draw some debug lines
            pygame.draw.line(screen, colors.WHITE, draw_pos, self.vertices[0], width=2)
            v1 = draw_vertices[0]
            v2 = draw_vertices[-1]
            mx = (v1[0] + v2[0]) / 2
            my = (v1[1] + v2[1]) / 2
            pygame.draw.line(screen, colors.BLACK, draw_pos, (mx, my), width=2)
            # pygame.draw.circle(screen, colors.BLUE, self.get_center(), GlobalTileProperties.side_length, width=2)
            pygame.draw.circle(screen, colors.YELLOW, draw_pos, GlobalTileProperties.apothem, width=2)


class GrassTileRep(TileRepresentation):

    def __init__(self, position, color=colors.Green.grass, outline_color=colors.get_gray(40)):
        super().__init__(position, color, outline_color)

    def draw(self, screen, offset=(0, 0)):
        super().draw(screen, offset)


class WaterTileRep(TileRepresentation):

    def __init__(self, position, color=colors.Blue.ocean, outline_color=colors.get_gray(40)):
        super().__init__(position, color, outline_color)

    def draw(self, screen, offset=(0, 0)):
        super().draw(screen, offset)
