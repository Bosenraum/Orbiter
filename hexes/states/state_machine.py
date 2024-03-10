

class StateMachine:

    def __init__(self, game_surface, game_input):
        self.current_state = None
        self.next_state = None
        self.prev_state = None

        self.game_input = game_input
        self.surface = game_surface

    def set_state(self, state):
        self.current_state = state

    def set_next_state(self, state):
        self.next_state = state

    def step(self):

        if self.current_state:
            self.current_state.sim(self.game_input)
            self.current_state.draw(self.surface)

        self.prev_state = self.current_state
        self.current_state = self.next_state