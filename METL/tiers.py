import abc
import typing


class Representation(abc.ABC):

    def __init__(self, x, y, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color

    def get_rect(self):
        # Returns the upper-left x,y coord plus width and height of representation
        pass

    def draw(self, screen):
        pass


class Renderer:

    def __init__(self, screen):
        self.screen = screen

    def draw_rep(self, rep: Representation):
        rep.draw(self.screen)

    def draw_reps(self, reps: [Representation]):
        for rep in reps:
            self.draw_rep(rep)


class TaskRenderer:

    def __init__(self, screen):
        self.screen = screen

    def draw_task(self, task):
        task.task_rep.draw(self.screen)

    def draw_tasks(self, tasks):
        for task in tasks:
            self.draw_task(task)


class Task:

    def __init__(self, name, parent, task_rep: Representation):
        self.name = name
        self.parent = parent
        self.task_rep = task_rep


class TierRenderer:

    def __init__(self, screen):
        self.screen = screen

    def draw_tier(self, tier):
        tier.tier_rep.draw(self.screen)

    def draw_tiers(self, tiers):
        for tier in tiers:
            self.draw_tier(tier)


class Tier:

    def __init__(self, parent_tier, tier_rep: Representation):
        self.parent_tier = parent_tier
        self.tasks = set()  # Set of tasks
        self.tier_rep = tier_rep

    def add_task(self, task):
        self.tasks.add(task)

    def get_tasks(self):
        return list(self.tasks)


