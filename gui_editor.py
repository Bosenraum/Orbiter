import pygame.key

from engine.engine import *

from widgets.drawable import Drawable
from widgets.serializable import Serializable
from widgets.dial import Dial
from widgets.button import Button

import json
import pickle


def test():
    print("Button clicked!")


class GuiEditor(Engine):
    def __init__(self, width, height, pf):

        self.APP_NAME = "GUI Editor"
        self.clickable_items = []
        self.mouse_held = False

        super().__init__(width, height, pf)

    def on_start(self):
        pass

    def on_update(self, elapsed_time):

        mouse_buttons = pygame.mouse.get_pressed(3)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = Vec2(mouse_x, mouse_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    dial = Dial(mouse_x, mouse_y, 50, color=get_random_color())
                    dial.value = random.randint(dial.min, dial.max)
                    self.clickable_items.append(dial)
                if event.key == pygame.K_f:
                    dial = Dial(mouse_x, mouse_y, 100, color=get_random_color())
                    dial.value = 30
                    self.clickable_items.append(dial)
                if event.key == pygame.K_x:
                    if len(self.clickable_items) > 0:
                        self.clickable_items.pop(-1)

                if event.key == pygame.K_b:
                    button = Button("Click Me!", mouse_x, mouse_y, 150, 50, test)
                    self.clickable_items.append(button)

                if event.key == pygame.K_s:
                    # Serialize all items and save to a file
                    ser_out = []
                    for item in self.clickable_items:
                        if not isinstance(item, Serializable):
                            continue
                        ser_out.append(item.serialize())

                    with open("widgets.obj", "wb") as f:
                        # json.dump(ser_out, f, indent=4)
                        pickle.dump(ser_out, f)

                if event.key == pygame.K_l:
                    # Load items from widget file
                    with open("widgets.obj", "rb") as f:
                        # items = json.load(f)
                        items = pickle.load(f)

                    for item in items:
                        # TODO: Create WidgetBuilder/WidgetFactory to create widgets
                        # Invoke the WidgetBuilder to create the proper widget (for now, just an if check)
                        widget = None
                        if item["type"].lower() == "dial":
                            widget = Dial()
                            widget.deserialize(item["attributes"])
                            self.clickable_items.append(widget)
                        elif item["type"].lower() == "button":
                            widget = Button()
                            widget.deserialize(item["attributes"])
                            self.clickable_items.append(widget)
                        else:
                            print(f"UNKNOWN WIDGET TYPE {item['type']}")

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_held = True
                # On-click mouse behavior
                if mouse_buttons[0]:
                    pass
                elif mouse_buttons[2]:
                    pass
                elif mouse_buttons[1]:
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_held = False
            if event.type == pygame.MOUSEWHEEL:
                # print(f"Mousewheel event: {event.x}, {event.y}")
                top = self.clickable_items[-1]
                if isinstance(top, Dial):
                    top.inc(event.y * 2)
                elif isinstance(top, Button):
                    w = top.border_width
                    w += event.y * 2
                    if w <= 1:
                        w = 1
                    top.border_width = w

        key_states = pygame.key.get_pressed()

        # Process items for mouse events
        for item in self.clickable_items[::-1]:
            if mouse_buttons[0] and (item.check_intersect(mouse_pos) or item.is_clicked):
                if key_states[pygame.K_LSHIFT]:
                    item.pos = mouse_pos
                else:
                    item.click()
                break
            else:
                item.unclick()

        self.screen.fill(BLACK)
        # Draw stuff

        for item in self.clickable_items:
            item.draw(self.screen)

        pygame.display.update()


if __name__ == "__main__":

    editor = GuiEditor(1080, 720, 1)
