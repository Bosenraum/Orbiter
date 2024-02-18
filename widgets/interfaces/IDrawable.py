

class IDrawable:

    def draw(self, screen):
        pass


class IClickable(IDrawable):

    def __init__(self):
        self.is_clicked = False

    def draw(self, screen):
        pass

    def check_intersect(self, pos):
        pass

    def click(self):
        self.is_clicked = True

    def unclick(self):
        self.is_clicked = False