import random
from the_league.people.person import Person


class Game:

    def __init__(self, team1, team2, num_rounds=9):
        self.team1 = team1
        self.team2 = team2
        self.played = False
        self.score = [0, 0]
        self.num_rounds = num_rounds

    def play(self):
        if self.played:
            return

        team1_players = []
        team2_players = []

        # Each team must select one player per round
        for r in range(self.num_rounds):
            self.play_round()

        while self.score[0] == self.score[1]:
            self.play_round()

        if self.score[0] > self.score[1]:
            self.team1.win()
            self.team2.lose()
            team1_result = "W"
            team2_result = "L"
        else:
            self.team2.win()
            self.team1.lose()
            team1_result = "L"
            team2_result = "W"

        team1_str = f"{self.team1.name.ljust(30)} ({team1_result})"
        team2_str = f"{self.team2.name.rjust(30)} ({team2_result})"
        print(f"{team1_str.ljust(40)} vs {team2_str.rjust(40)} \t({self.score[0]: <03} - {self.score[1] : >03})")

        self.played = True

    def play_round(self):
        p1 = self.team1.play()
        p2 = self.team2.play()

        stat1 = random.choice([Person.Stat.SPEED, Person.Stat.STRENGTH, Person.Stat.OFFENSE, Person.Stat.DEFENSE])
        stat2 = Person.get_opposite_stat(stat1)
        r1 = round(p1.play(stat1))
        r2 = round(p2.play(stat2))

        if r1 > r2:
            self.score[0] += 1
        elif r2 > r1:
            self.score[1] += 1