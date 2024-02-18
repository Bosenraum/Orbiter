import pygame
from engine.engine import *
import math

import copy


class Mat4x4:

    def __init__(self):
        self.m = [[0 for _ in range(4)],
                  [0 for _ in range(4)],
                  [0 for _ in range(4)],
                  [0 for _ in range(4)]]

    def __mul__(self, other):
        matrix = Mat4x4()
        for c in range(len(self.m)):
            for r in range(len(self.m[c])):
                for k in range(4):
                    matrix.m[r][c] += self.m[r][k] * other.m[k][c]
        return matrix


class Matrix:

    def __init__(self, nrows, ncols, preset=0.0, id=False):
        self.m=[]
        for r in nrows:
            self.m.append([preset for _ in range(ncols)])


class Triangle:

    def __init__(self, points: list, color=WHITE, mesh_color=BLUE):
        self.p = points
        self.color = color
        self.mesh_color = mesh_color

    def draw(self, scr, wireframe=False):
        points = [(p.x, p.y) for p in self.p]
        pygame.draw.polygon(scr, self.color, points, width=0)
        if wireframe:
            pygame.draw.lines(scr, self.mesh_color, True, points)

    def __getitem__(self, item):
        return self.p[item]

    def copy(self):
        p = self.p.copy()
        return Triangle(p, self.color, self.mesh_color)

    def normalize(self):
        if self.p[0].w != 0:
            self.p[0] /= self.p[0].w
            self.p[1] /= self.p[1].w
            self.p[2] /= self.p[2].w

    def offset(self, x, y, z):
        for p in self.p:
            p.x += x
            p.y += y
            p.z += z

    def offset_z(self, offset):
        for p in self.p:
            p.z += offset

    def offset_y(self, offset):
        for p in self.p:
            p.y += offset

    def offset_x(self, offset):
        for p in self.p:
            p.x += offset

    def scale(self, width, height, offset_vector=Vec3(0, 0, 0)):
        for p in self.p:
            p.x += offset_vector.x
            p.y += offset_vector.y

            p.x *= offset_vector.x * 0.5 * width
            p.y *= offset_vector.y * 0.5 * height


class Mesh:

    def __init__(self):
        self.tris = []

    def load_from_obj_file(self, filename):
        verts = []
        with open(filename, "r") as obj_file:
            for line in obj_file.readlines():
                parts = line.split(" ")
                if parts[0] == 'v':
                    verts.append(Vec3(float(parts[1]), float(parts[2]), float(parts[3])))
                elif parts[0] == 'f':
                    f = [int(parts[1]), int(parts[2]), int(parts[3])]
                    self.tris.append(Triangle([verts[f[0] - 1], verts[f[1] - 1], verts[f[2] - 1]]))

        return True


class ThreeDEngine(Engine):
    APP_NAME = "ThreeDEngine"

    def __init__(self, width, height, pf):
        self.meshCube = Mesh()
        self.matProj = Mat4x4()

        self.camera = NULL_VECTOR_3D
        self.look_dir = UNIT_VEC3_Z

        self.yaw = 0.0

        self.theta = 0

        super().__init__(width, height, pf)     # Starts the engine

    @staticmethod
    def multiply_vector_matrix(v, m):
        o = Vec3()
        o.x = v.x * m.m[0][0] + v.y * m.m[1][0] + v.z * m.m[2][0] + v.w * m.m[3][0]
        o.y = v.x * m.m[0][1] + v.y * m.m[1][1] + v.z * m.m[2][1] + v.w * m.m[3][1]
        o.z = v.x * m.m[0][2] + v.y * m.m[1][2] + v.z * m.m[2][2] + v.w * m.m[3][2]
        o.w = v.x * m.m[0][3] + v.y * m.m[1][3] + v.z * m.m[2][3] + v.w * m.m[3][3]

        return o

    def make_identity_matrix(self):
        id_mat = Mat4x4()
        id_mat.m[0][0] = 1.0
        id_mat.m[1][1] = 1.0
        id_mat.m[2][2] = 1.0
        id_mat.m[3][3] = 1.0
        return id_mat

    def make_rot_x_matrix(self, angle_rad):
        matrix = Mat4x4()
        matrix.m[0][0] = 1
        matrix.m[1][1] = math.cos(angle_rad)
        matrix.m[1][2] = math.sin(angle_rad)
        matrix.m[2][1] = -math.sin(angle_rad)
        matrix.m[2][2] = math.cos(angle_rad)
        matrix.m[3][3] = 1
        return matrix

    def make_rot_y_matrix(self, angle_rad):
        matrix = Mat4x4()
        matrix.m[0][0] = math.cos(angle_rad)
        matrix.m[1][1] = 1.0
        matrix.m[0][2] = math.sin(angle_rad)
        matrix.m[2][0] = -math.sin(angle_rad)
        matrix.m[2][2] = math.cos(angle_rad)
        matrix.m[3][3] = 1
        return matrix

    def make_rot_z_matrix(self, angle_rad):
        matrix = Mat4x4()
        matrix.m[0][0] = math.cos(angle_rad)
        matrix.m[0][1] = math.sin(angle_rad)
        matrix.m[1][1] = math.cos(angle_rad)
        matrix.m[1][0] = -math.sin(angle_rad)
        matrix.m[2][2] = 1
        matrix.m[3][3] = 1
        return matrix

    def make_translation(self, x, y, z):
        matrix = self.make_identity_matrix()
        matrix.m[3][0] = x
        matrix.m[3][1] = y
        matrix.m[3][2] = z
        return matrix

    def multiply_tri_matrix(self, tri, matrix):
        return Triangle([
            self.multiply_vector_matrix(tri[0], matrix),
            self.multiply_vector_matrix(tri[1], matrix),
            self.multiply_vector_matrix(tri[2], matrix)
        ], color=tri.color, mesh_color=tri.mesh_color)

    def make_projection_matrix(self, fov, aspect_ratio, z_near, z_far):
        q = z_far / (z_far - z_near)
        fov_rad = 1.0 / math.tan(fov * 0.5 / 180.0 * math.pi)

        mat_proj = Mat4x4()
        mat_proj.m[0][0] = aspect_ratio * fov_rad
        mat_proj.m[1][1] = fov_rad
        mat_proj.m[2][2] = q
        mat_proj.m[3][2] = -z_near * q
        mat_proj.m[2][3] = 1
        return mat_proj

    def matrix_point_at(self, pos: Vec3, target: Vec3, up: Vec3):
        new_forward = (target - pos).normalize()

        a = new_forward * up.dot(new_forward)
        new_up = (up - a).normalize()

        new_right = new_up.cross(new_forward)

        matrix = Mat4x4()
        matrix.m[0][0] = new_right.x; matrix.m[0][1] = new_right.y; matrix.m[0][2] = new_right.z; matrix.m[0][3] = 0
        matrix.m[1][0] = new_up.x; matrix.m[1][1] = new_up.y; matrix.m[1][2] = new_up.z; matrix.m[1][3] = 0
        matrix.m[2][0] = new_forward.x; matrix.m[2][1] = new_forward.y; matrix.m[2][2] = new_forward.z; matrix.m[2][3] = 0
        matrix.m[3][0] = pos.x; matrix.m[3][1] = pos.y; matrix.m[3][2] = pos.z; matrix.m[3][3] = 1
        return matrix

    def quick_inverse_matrix(self, m):
        matrix = Mat4x4()

        matrix.m[0][0] = m.m[0][0]
        matrix.m[0][1] = m.m[1][0]
        matrix.m[0][2] = m.m[2][0]
        matrix.m[0][3] = 0.0

        matrix.m[1][0] = m.m[0][1]
        matrix.m[1][1] = m.m[1][1]
        matrix.m[1][2] = m.m[2][1]
        matrix.m[1][3] = 0.0

        matrix.m[2][0] = m.m[0][2]
        matrix.m[2][1] = m.m[1][2]
        matrix.m[2][2] = m.m[2][2]
        matrix.m[2][3] = 0.0

        matrix.m[3][0] = -(m.m[3][0] * matrix.m[0][0] + m.m[3][1] * matrix.m[1][0] + m.m[3][2] * matrix.m[2][0])
        matrix.m[3][1] = -(m.m[3][0] * matrix.m[0][1] + m.m[3][1] * matrix.m[1][1] + m.m[3][2] * matrix.m[2][1])
        matrix.m[3][2] = -(m.m[3][0] * matrix.m[0][2] + m.m[3][1] * matrix.m[1][2] + m.m[3][2] * matrix.m[2][2])
        matrix.m[3][3] = 1.0

        return matrix

    def vector_intersect_plane(self, plane_p: Vec3, plane_n: Vec3, line_start: Vec3, line_end: Vec3):
        plane_n = plane_n.normalize()
        plane_d = -1 * plane_n.dot(plane_p)
        ad = line_start.dot(plane_n)
        bd = line_end.dot(plane_n)
        t = (-plane_d - ad) / (bd - ad)
        line_start_to_end = line_end - line_start
        line_to_intersect = line_start_to_end * t
        return line_start + line_to_intersect

    def triangle_clip_against_plane(self, plane_p: Vec3, plane_n: Vec3, tri: Triangle):
        plane_n = plane_n.normalize()

        dist = lambda p: plane_n.x * p.x + plane_n.y * p.y + plane_n.z * p.z - plane_n.dot(plane_p)

        in_points = []
        in_point_count = 0
        out_points = []
        out_point_count = 0

        d0 = dist(tri.p[0])
        d1 = dist(tri.p[1])
        d2 = dist(tri.p[2])

        if d0 >= 0:
            in_point_count += 1
            in_points.append(tri.p[0])
        else:
            out_point_count += 1
            out_points.append(tri.p[0])

        if d1 >= 0:
            in_point_count += 1
            in_points.append(tri.p[1])
        else:
            out_point_count += 1
            out_points.append(tri.p[1])

        if d2 >= 0:
            in_point_count += 1
            in_points.append(tri.p[2])
        else:
            out_point_count += 1
            out_points.append(tri.p[2])

        if in_point_count == 0:
            return ()
        if in_point_count == 3:
            return tri,
        if in_point_count == 1 and out_point_count == 2:
            out_tri = tri.copy()
            # out_tri.color = vivid_cerulean
            # out_tri.mesh_color = razzmatazz
            out_tri.p[0] = in_points[0]

            out_tri.p[1] = self.vector_intersect_plane(plane_p, plane_n, in_points[0], out_points[0])
            out_tri.p[2] = self.vector_intersect_plane(plane_p, plane_n, in_points[0], out_points[1])

            return out_tri,

        if in_point_count == 2 and out_point_count == 1:
            out_tri1 = tri.copy()
            out_tri2 = tri.copy()

            # out_tri1.color = pink
            # out_tri2.color = empty_beer
            # out_tri1.mesh_color = byzantine
            # out_tri2.mesh_color = dark_green

            out_tri1.p[0] = in_points[0]
            out_tri1.p[1] = in_points[1]
            out_tri1.p[2] = self.vector_intersect_plane(plane_p, plane_n, in_points[0], out_points[0])

            out_tri2.p[0] = in_points[1]
            out_tri2.p[1] = out_tri2.p[2]
            out_tri2.p[2] = self.vector_intersect_plane(plane_p, plane_n, in_points[1], out_points[0])

            return out_tri1, out_tri2

    # called once before the loop begins
    def on_start(self):
        # self.meshCube.tris = [
        #     # SOUTH
        #     Triangle([Vec3(0.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 0.0)]),
        #     Triangle([Vec3(0.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 0.0, 0.0)]),
        #
        #     # EAST
        #     Triangle([Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0)]),
        #     Triangle([Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 0.0, 1.0)]),
        #
        #     # NORTH
        #     Triangle([Vec3(1.0, 0.0, 1.0), Vec3(1.0, 1.0, 1.0), Vec3(0.0, 1.0, 1.0)]),
        #     Triangle([Vec3(1.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 0.0, 1.0)]),
        #
        #     # WEST
        #     Triangle([Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 1.0, 0.0)]),
        #     Triangle([Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 0.0), Vec3(0.0, 0.0, 0.0)]),
        #
        #     # TOP
        #     Triangle([Vec3(0.0, 1.0, 0.0), Vec3(0.0, 1.0, 1.0), Vec3(1.0, 1.0, 1.0)]),
        #     Triangle([Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 1.0, 0.0)]),
        #
        #     # BOTTOM
        #     Triangle([Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0)]),
        #     Triangle([Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0), Vec3(1.0, 0.0, 0.0)]),
        # ]

        # self.meshCube.load_from_obj_file("obj_files/VideoShip.obj")
        # self.meshCube.load_from_obj_file("obj_files/axis.obj")
        # self.meshCube.load_from_obj_file("obj_files/teapot.obj")
        # self.meshCube.load_from_obj_file("obj_files/mountains.obj")
        self.meshCube.load_from_obj_file("obj_files/VideoShip.obj")

        self.static_angle = [0 for _ in range(3)]
        self.sa_index = 0

        # Projection Matrix
        fov = 90.0
        aspect_ratio = self.height/self.width
        z_near = 0.1
        z_far = 100.0
        self.matProj = self.make_projection_matrix(fov, aspect_ratio, z_near, z_far)

        pygame.key.set_repeat(50, 50)

    # called once per loop iteration
    def on_update(self, elapsed_time):

        # ### USER INPUT ### #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            keys = pygame.key.get_pressed()
            shift = False
            if keys[pygame.K_LSHIFT]:
                shift = True

            if event.type == pygame.KEYDOWN:
                v_forward = self.look_dir * 2 * 60 * self.tick
                if event.key == pygame.K_w:
                    if shift:
                        self.camera.y -= 8 * 60 * self.tick
                    else:
                        self.camera += v_forward
                if event.key == pygame.K_s:
                    if shift:
                        self.camera.y += 8 * 60 * self.tick
                    else:
                        self.camera -= v_forward

                # if event.key == pygame.K_w:
                #     self.camera += v_forward
                # if event.key == pygame.K_s:
                #     self.camera -= v_forward
                if event.key == pygame.K_a:
                    self.yaw += 8 * self.tick
                if event.key == pygame.K_d:
                    self.yaw -= 8 * self.tick

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    self.static_angle[self.sa_index] += 15 * math.pi / 180
                elif mouse_buttons[2]:
                    self.static_angle[self.sa_index] -= 15 * math.pi / 180
                elif mouse_buttons[1]:
                    self.sa_index = (self.sa_index + 1) % 3

        self.theta = 2.0 * elapsed_time

        mat_rot_z = self.make_rot_z_matrix(self.static_angle[2])
        mat_rot_y = self.make_rot_y_matrix(self.static_angle[1])
        mat_rot_x = self.make_rot_x_matrix(self.static_angle[0])
        # mat_rot_z = self.make_rot_z_matrix(self.theta * 0.9)
        # mat_rot_x = self.make_rot_x_matrix(self.theta * 0.5)
        # mat_rot_y = self.make_rot_y_matrix(self.theta * 0.1)

        mat_trans = self.make_translation(0.0, 0.0, 40.0)

        # mat_world = self.make_identity_matrix()
        mat_world = mat_rot_z * mat_rot_y * mat_rot_x
        mat_world = mat_world * mat_trans

        v_up = UNIT_VEC3_Y
        # v_target = self.camera + self.look_dir
        v_target = UNIT_VEC3_Z
        mat_camera_rot = self.make_rot_y_matrix(self.yaw)
        self.look_dir = self.multiply_vector_matrix(v_target, mat_camera_rot)
        v_target = self.camera + self.look_dir

        mat_camera = self.matrix_point_at(self.camera, v_target, v_up)
        mat_view = self.quick_inverse_matrix(mat_camera)

        self.screen.fill(blend(alabaster, blue_violet))
        # Draw stuff

        tris_to_raster = []

        # draw triangles
        for tri in self.meshCube.tris:
            # ### ROTATION ### #
            # tri_rot = self.multiply_tri_matrix(tri, mat_rot_z)
            # tri_rot = self.multiply_tri_matrix(tri_rot, mat_rot_y)
            # tri_rot = self.multiply_tri_matrix(tri_rot, mat_rot_x)
            #
            # ### Z TRANSLATION ### #
            # tri_translated = tri_rot
            # z_offset = 8.0
            # tri_translated.offset_z(z_offset)

            # tri_transformed = Triangle([
            #     self.multiply_vector_matrix(origin, mat_world) for origin in tri.origin
            # ])
            # tri_transformed = tri_translated
            tri_transformed = self.multiply_tri_matrix(tri, mat_world)

            # ### NORMALS ### #
            line1 = tri_transformed.p[1] - tri_transformed.p[0]
            line2 = tri_transformed[2] - tri_transformed[0]
            normal = line1.cross(line2).normalize()

            camera_ray = tri_transformed.p[0] - self.camera

            if normal.dot(camera_ray) < 0:

                # ### ILLUMINATION ### #
                light_direction = Vec3(1.0, -1.0, -1.0).normalize()
                dp = light_direction.dot(normal)
                color = color_clamp((220 * dp + 35, 220 * dp + 35, 220 * dp + 35))

                # Convert World space ---> View space
                tri_viewed = self.multiply_tri_matrix(tri_transformed, mat_view)
                tri_viewed.color = color

                clipped = self.triangle_clip_against_plane(UNIT_VEC3_Z * 0.1, UNIT_VEC3_Z, tri_viewed)

                for n in clipped:
                    # ### PROJECTION ### #
                    tri_projected = self.multiply_tri_matrix(n, self.matProj)

                    # ### SCALING ### #
                    tri_projected.normalize()
                    tri_projected.scale(self.width, self.height, offset_vector=Vec3(1, 1, 0))

                    tris_to_raster.append(tri_projected)

        tris_to_raster.sort(key=lambda t: (t.origin[0].z + t.origin[1].z + t.origin[2].z) / 3.0, reverse=True)
        for tri in tris_to_raster:
            # ### DRAW ### #
            clipped = []
            tri_list = [tri]
            new_tris = 1

            for p in range(4):
                while new_tris > 0:
                    test = tri_list[0]
                    tri_list.remove(tri_list[0])
                    new_tris -= 1

                    if p == 0:
                        clipped = self.triangle_clip_against_plane(NULL_VECTOR_3D, UNIT_VEC3_Y, test)
                    elif p == 1:
                        clipped = self.triangle_clip_against_plane(UNIT_VEC3_Y * (self.height - 1), UNIT_VEC3_Y * -1, test)
                    elif p == 2:
                        clipped = self.triangle_clip_against_plane(NULL_VECTOR_3D, UNIT_VEC3_X, test)
                    elif p == 3:
                        clipped = self.triangle_clip_against_plane(UNIT_VEC3_X * (self.width - 1), UNIT_VEC3_X * -1, test)

                    for c in clipped:
                        tri_list.append(c)

                new_tris = len(tri_list)

            for t in tri_list:
                t.draw(self.screen, wireframe=False)

        pygame.display.update()


if __name__ == "__main__":
    DDD = ThreeDEngine(800, 800, 1)
