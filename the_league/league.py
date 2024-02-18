
from team import *
from people.coach import *
from people.player import *
from game import *


class League:

    def __init__(self, name, age, num_teams, players_per_team, percent_extra_players):
        self.name = name
        self.age = age

        self.num_teams = num_teams
        self.players_per_team = players_per_team
        self.num_players = int(self.num_teams * self.players_per_team * (1 + (percent_extra_players / 100)))

        self.teams = []
        self.players = []
        self.available_players = []

        self.num_playoff_teams = 12
        self.draft_player_limit_per_round = 5

        self.season = 1
        self.round = 1

    def __str__(self):
        return f"{self.name}"

    def play_round(self):
        print(f"\n{self.name} Season {self.season} : Round {self.round}")
        teams_remaining = [t for t in self.teams]
        while len(teams_remaining) > 1:
            team1 = random.choice(teams_remaining)
            teams_remaining.remove(team1)

            team2 = random.choice(teams_remaining)
            teams_remaining.remove(team2)
            game = Game(team1, team2)
            game.play()

        self.teams.sort(key=lambda t: t.stats.wins, reverse=True)

        self.round += 1

    def create_teams(self, team_names):
        # team_names = generate_team_names(self.num_teams)
        self.teams = []
        while team_names:
            team_name = random.choice(team_names)
            team_names.remove(team_name)
            team_age = random.randint(0, self.age)
            coach = create_random_coach()

            team = Team(team_name, team_age, coach)
            self.teams.append(team)

    def create_players(self, player_names):
        # player_names = generate_player_names(self.num_players)
        self.players = []
        while player_names:
            player_name = random.choice(player_names)
            player_names.remove(player_name)

            gender = random.random()
            if gender < 0.01:
                gender = "T"
            elif gender < 0.4:
                gender = "F"
            else:
                gender = "M"

            player = create_random_player(name=player_name, gender=gender)
            self.players.append(player)

    def draft(self):
        self.available_players = [_ for _ in self.players]
        for draft_round in range(self.players_per_team):
            # random.shuffle(self.teams)
            for team in self.teams:
                team_pick = team.draft_player(self.available_players, self.draft_player_limit_per_round)

                self.available_players.remove(team_pick)

    def serialize(self):
        teams = [
            team.serialize() for team in self.teams
        ]
        players = [
            player.serialize() for player in self.players
        ]
        available_players = [
            player.serialize() for player in self.available_players
        ]
        league = {
            "name": self.name,
            "age": self.age,
            "num_teams": self.num_teams,
            "teams": teams,
            "players": players,
            "available_players": available_players,
            "season": self.season,
            "round": self.round
        }
        return league

    def deserialize(self, league):
        self.name = league.get("name", "MLL")
        self.age = league.get("age", 0)
        self.num_teams = league.get("num_teams", 30)
        teams = league.get("teams", [])
        for team in teams:
            t = create_random_team()
            t.deserialize(team)
            self.teams.append(t)

        players = league.get("players", [])
        for player in players:
            p = create_random_player()
            p.deserialize(player)
            self.players.append(p)

        available_players = league.get("available_players", [])
        for player in available_players:
            p = create_random_player()
            p.deserialize(player)
            self.available_players.append(p)

        self.season = league.get("season", 1)
        self.round = league.get("round", 1)


def create_league():
    return League("MLL", 0, 30, 10, 10)