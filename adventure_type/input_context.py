import pygame


class InputContext:

    def __init__(self, context_name):
        self.name = context_name

    def process(self, input_value):
        return None


class TypingContext(InputContext):

    def __init__(self):
        super().__init__("Typing Context")
        self.type_buffer = []

    def process(self, input_event):

        if input_event.key == pygame.K_BACKSPACE:
            if len(self.type_buffer) > 0:
                self.type_buffer.pop(-1)
        else:
            self.type_buffer.append(input_event.unicode)

        buffer_val = self.concatenate()

        return buffer_val

    def concatenate(self):
        return "".join(self.type_buffer)

    def clear(self):
        self.type_buffer = []