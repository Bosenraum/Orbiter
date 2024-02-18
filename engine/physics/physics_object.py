from engine.vector import Vec2, UNIT_VECTOR_2D, NULL_VECTOR_2D


class ITickable:

    def tick(self):
        pass


class PhysicsObjectPool(ITickable):

    def __init__(self, max_objects=None):
        self.max_objects = max_objects
        self.objects = []

    def add(self, obj: ITickable):
        if self.max_objects is None or len(self.objects) < self.max_objects:
            self.objects.append(obj)
            return True
        return False

    def remove(self, obj: ITickable):
        try:
            self.objects.remove(obj)
            return True
        except ValueError:
            return False

    def tick(self):
        for obj in self.objects:
            obj.tick()


class PhysicsObject2D(ITickable):

    def __init__(self, pos: Vec2, vel: Vec2 = 0, accel: Vec2 = 0):
        self.pos = pos
        self.vel = vel
        self.accel = accel

    def tick(self):
        # Every tick, update the physics objects
        self.pos += self.vel
        self.vel += self.accel


