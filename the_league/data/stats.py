from typing import Any


class Stats:

    def __init__(self):
        self.score = 0
        self.overall = 0
        self.wins = 0
        self.losses = 0

    def serialize(self):
        stat = {
            "score": self.score,
            "overall": self.overall,
            "wins": self.wins,
            "losses": self.losses
        }
        return stat

    def deserialize(self, stat):
        self.score = stat.get("score", 0)
        self.overall = stat.get("overall", 0)
        self.wins = stat.get("wins", 0)
        self.losses = stat.get("losses", 0)


class PlayerStats(Stats):

    def __init__(self):
        self.time_played = 0.0
        self.saves = 0
        super().__init__()

    def serialize(self):
        stat = super().serialize()
        stat["time_played"] = self.time_played
        stat["saves"] = self.saves
        return stat

    def deserialize(self, stat):
        super().deserialize(stat)
        self.time_played = stat.get("time_played", 0.0)
        self.saves = stat.get("saves", 0)


class CoachStats(Stats):
    def __init__(self):
        super().__init__()


class TeamStats(Stats):

    def __init__(self):
        super().__init__()


