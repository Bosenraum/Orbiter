

class Drawable:

    def draw(self, screen):
        pass


class Clickable(Drawable):

    def __init__(self):
        self.is_clicked = False

    def draw(self, scree):
        pass

    def check_intersect(self, pos):
        pass

    def click(self):
        self.is_clicked = True

    def unclick(self):
        self.is_clicked = False