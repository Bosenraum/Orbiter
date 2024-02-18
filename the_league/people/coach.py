import random

from the_league.people.person import Person
from the_league.data.stats import CoachStats
from the_league.data.player_names import generate_name


class Coach(Person):

    age_range = (35, 100)

    def __init__(self, name, gender, age, speed, strength, offense, defense, sense):
        super().__init__(name, gender, age, speed, strength, offense, defense, sense)

        self.stats = CoachStats()

    def __str__(self):
        return f"Coach {self.name} {self.age} {self.gender} | {self.overall}"

    def play(self):
        pass

    def win(self):
        self.stats.wins += 1

    def lose(self):
        self.stats.losses += 1

    def serialize(self):
        person = super().serialize()
        person["stats"] = self.stats.serialize()
        return person

    def deserialize(self, person):
        super().deserialize(person)
        stats = person.get("stats", None)
        self.stats = CoachStats()
        if stats:
            self.stats.deserialize(stats)


def create_random_coach(**kwargs):
    gender = kwargs.get("gender", "M")
    default_name = generate_name(Person.gender_name_ratio_map[gender])
    name = kwargs.get("name", default_name)
    age = kwargs.get("age", random.randrange(*Coach.age_range))
    speed = kwargs.get("speed", random.randrange(*Person.speed_range))
    strength = kwargs.get("strength", random.randrange(*Person.strength_range))
    offense = kwargs.get("offense", random.randrange(*Person.offense_range))
    defense = kwargs.get("defense", random.randrange(*Person.defense_range))
    sense = kwargs.get("sense", random.randrange(*Person.sense_range))

    coach = Coach(name, gender, age, speed, strength, offense, defense, sense)
    return coach