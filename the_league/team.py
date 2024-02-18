from the_league.people.player import *
from the_league.people.coach import *
from data.stats import TeamStats


class Team:

    positions = [_ for _ in "FLRMUDWGP0"]

    def __init__(self, name, age, coach):
        self.name = name
        self.age = age
        self.coach = coach
        self.players = []
        self.open_positions = [pos for pos in Team.positions]
        self.overall = 0
        self.calc_overall()

        self.stats = TeamStats()

    def __str__(self):
        return f"{self.name} {round(self.overall, 1)} ({self.stats.wins} - {self.stats.losses})"

    def calc_overall(self):
        if len(self.players) == 0:
            self.overall = 0
            return

        sum = 0
        for player in self.players:
            sum += player.overall

        self.overall = sum / len(self.players)

    def num_players(self):
        return len(self.players)

    def add_player(self, player: Player) -> None:
        player = self.assign_position(player)
        self.players.append(player)
        self.calc_overall()

    def assign_position(self, player):
        player.position = random.choice(self.open_positions)
        self.open_positions.remove(player.position)
        return player

    def draft_player(self, players, player_limit):
        pick = None
        for p in random.sample(players, player_limit):
            if pick is None:
                pick = p
            else:
                if p.overall > pick.overall:
                    pick = p

        if pick:
            self.add_player(pick)
        return pick

    def get_roster(self):
        roster = [p for p in self.players]
        roster.append(self.coach)
        return roster

    def play(self):
        return random.choice(self.players)

    def win(self):
        self.stats.wins += 1
        [player.win() for player in self.players]
        self.coach.win()

    def lose(self):
        self.stats.losses += 1
        [player.lose() for player in self.players]
        self.coach.lose()

    def draw(self):
        self.stats.draws += 1
        [player.draw() for player in self.players]
        self.coach.draw()

    def serialize(self):
        players = [
            player.serialize() for player in self.players
        ]
        team = {
            "name": self.name,
            "age": self.age,
            "coach": self.coach.serialize(),
            "players": players,
            "open_positions": self.open_positions,
            "stats": self.stats.serialize()
        }
        return team

    def deserialize(self, team):
        self.name = team.get("name", "***** *****")
        self.age = team.get("age", 0)

        coach = team.get("coach", None)
        c = create_random_coach()
        if coach:
            c.deserialize(coach)

        self.coach = c

        players = team.get("players")
        for player in players:
            p = create_random_player()
            p.deserialize(player)
            self.players.append(p)

        self.open_positions = team.get("open_positions", Team.positions)

        stats = team.get("stats", None)
        self.stats = TeamStats()
        if stats:
            self.stats.deserialize(stats)
        self.calc_overall()


def create_random_team(**kwargs):
    name = kwargs.get("name", "***** *****")
    age = kwargs.get("age", 0)
    coach = create_random_coach()
    coach = kwargs.get("coach", coach)

    return Team(name, age, coach)