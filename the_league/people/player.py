import random

from the_league.people.person import Person
from the_league.data.stats import PlayerStats
from the_league.data.player_names import generate_name


class Player(Person):

    age_range = (16, 45)

    def __init__(self, name, gender, age, speed, strength, offense, defense, sense):
        super().__init__(name, gender, age, speed, strength, offense, defense, sense)
        self.position = ""

        self.stats = PlayerStats()

    def __str__(self):
        return f"{self.position} {self.name} {self.age} {self.gender} | {self.overall}"

    def assign_position(self, position):
        self.position = position

    def play(self, stat=None):
        value = self.sense
        if stat == Person.Stat.SPEED:
            value += self.speed
        elif stat == Person.Stat.STRENGTH:
            value += self.strength
        elif stat == Person.Stat.OFFENSE:
            value += self.offense
        elif stat == Person.Stat.DEFENSE:
            value += self.defense

        return value

    def win(self):
        self.stats.wins += 1

    def lose(self):
        self.stats.losses += 1

    def serialize(self):
        person = super().serialize()
        person["position"] = self.position
        person["stats"] = self.stats.serialize()
        return person

    def deserialize(self, person):
        super().deserialize(person)
        self.position = person.get("position", "X")

        stats = person.get("stats", None)
        self.stats = PlayerStats()
        if stats:
            self.stats.deserialize(stats)


def create_random_player(**kwargs):
    gender = kwargs.get("gender", "M")
    default_name = generate_name(Person.gender_name_ratio_map[gender])
    name = kwargs.get("name", default_name)
    stat_max = Player.stat_range[-1]
    stat_norm = random.random() * 50 + Player.stat_range[0]
    sigma = 15

    sense_norm = stat_norm / (Person.stat_range[-1] / Person.sense_range[-1])
    sense_sigma = 5/3
    # r = random.normalvariate(stat_norm, sigma)
    # print(f"Random value ({r}) from norm ({stat_norm}) and sigma ({sigma})")

    age = kwargs.get("age", random.randrange(*Player.age_range))
    speed = kwargs.get("speed", random.normalvariate(stat_norm, sigma))
    strength = kwargs.get("strength", random.normalvariate(stat_norm, sigma))
    offense = kwargs.get("offense", random.normalvariate(stat_norm, sigma))
    defense = kwargs.get("defense", random.normalvariate(stat_norm, sigma))
    sense = kwargs.get("sense", random.normalvariate(sense_norm, sense_sigma))

    player = Player(name, gender, age, speed, strength, offense, defense, sense)
    return player

