

class Sequencer:

    def __init__(self, seq=None):
        if not seq:
            self.seq = []
        self.seq = seq

        self.seq_status = None
        self.seq_counter = None
        self.done = False
        self.reset()

    def reset(self):
        self.seq_status = [False for _ in self.seq]
        self.seq_counter = 0

    def check_done(self):
        return all(self.seq_status)

    def check_input(self, seq_in):
        if not self.seq:
            return False

        if self.done:
            self.done = False
            self.reset()

        if seq_in == self.seq[self.seq_counter]:
            self.seq_status[self.seq_counter] = True
            self.seq_counter += 1

            if self.check_done():
                self.done = True
        else:
            self.reset()

        return self.done


