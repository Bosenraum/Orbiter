import pygame

from engine.vector import Vec2, UNIT_VECTOR_2D
import engine.colors as colors


class Ray:

    def __init__(self, p: Vec2, q: Vec2, **kwargs):
        self.origin = p
        self.q = q
        if q != p:
            self.direction = self.origin - self.q
        else:
            self.direction = UNIT_VECTOR_2D

        self.color = kwargs.get("color", colors.WHITE)
        self.dot_color = kwargs.get("dot_color", self.color)

    def get_point(self, t):
        return self.origin + self.direction * t

    def move(self, pos):
        self.origin = pos
        self.q = self.origin + pos

    def change_direction(self, new_dir):
        self.direction = self.origin - new_dir
        self.q = new_dir

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.origin.get(), self.q.get())
        # Draw circles at the points
        pygame.draw.circle(screen, self.color, self.origin.get(), 4)
        pygame.draw.circle(screen, self.color, self.q.get(), 4)

    def colliderect(self, target: pygame.rect.Rect):
        target_pos = Vec2(target.x, target.y)
        target_size = Vec2(target.x + target.w, target.y + target.h)
        t_near = (target_pos - self.origin) / self.direction
        t_far = (target_pos + target_size - self.origin) / self.direction
        result = {
            "collides": False,
            "contact_point": None,
            "far_contact_point": None,
            "contact_normal": None,
            "t_hit_near": None
        }

        if t_near.x > t_far.x:
            t_near.x, t_far.x = t_far.x, t_near.x

        if t_near.y > t_far.y:
            t_near.y, t_far.y = t_far.y, t_near.y

        if t_near.x > t_far.y or t_near.y > t_far.x:
            return result

        t_hit_near = max(t_near.x, t_near.y)
        t_hit_far = min(t_far.x, t_far.y)

        if t_hit_far < 0:
            return result

        self.get_point(t_hit_near)
        self.get_point(t_hit_far)

        result["contact_point"] = self.origin + t_hit_near * self.direction
        result["far_contact_point"] = self.origin + t_hit_far * self.direction

        if t_near.x > t_near.y:
            if self.direction.x < 0:
                contact_normal = Vec2(1, 0)
            else:
                contact_normal = Vec2(-1, 0)
        elif t_near.x < t_near.y:
            if self.direction.y < 0:
                contact_normal = Vec2(0, 1)
            else:
                contact_normal = Vec2(0, -1)

        result["contact_normal"] = contact_normal
        result["collides"] = True

        return result
