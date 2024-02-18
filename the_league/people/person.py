from enum import Enum, auto


class Person:

    class Stat(Enum):
        SPEED = auto(),
        STRENGTH = auto(),
        OFFENSE = auto(),
        DEFENSE = auto()

    gender_name_ratio_map = {
        "M": 1.0,
        "F": 0.0,
        "T": 0.5
    }
    age_range = (16, 100)

    stat_range = (30, 100)
    speed_range = (10, 100)
    strength_range = (10, 100)
    offense_range = (10, 100)
    defense_range = (10, 100)
    sense_range = (0, 20)

    def __init__(self, name, gender, age, speed, strength, offense, defense, sense):
        self.name = name
        self.gender = gender
        self.age = age
        self.speed = round(speed, 2)
        self.strength = round(strength, 2)
        self.offense = round(offense, 2)
        self.defense = round(defense, 2)
        self.sense = round(sense, 2)
        self.overall = None
        self.calc_overall()

    def __str__(self):
        return f"{self.name} {self.age} {self.gender} | {self.overall}"

    def calc_overall(self):
        stat_avg = (self.speed + self.strength + self.offense + self.defense) / 4
        self.overall = round(stat_avg + self.sense, 2)

    def play(self):
        pass

    def win(self):
        pass

    def lose(self):
        pass

    @staticmethod
    def get_opposite_stat(stat):
        if stat == Person.Stat.SPEED:
            return Person.Stat.STRENGTH
        elif stat == Person.Stat.STRENGTH:
            return Person.Stat.SPEED
        elif stat == Person.Stat.OFFENSE:
            return Person.Stat.DEFENSE
        elif stat == Person.Stat.DEFENSE:
            return Person.Stat.OFFENSE

    def serialize(self):
        person = {
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "speed": self.speed,
            "strength": self.strength,
            "offense": self.offense,
            "defense": self.defense,
            "sense": self.sense,
            "overall": self.overall
        }
        return person

    def deserialize(self, person):
        self.name = person.get("name", "--- ---")
        self.gender = person.get("gender", "M")
        self.age = person.get("age", self.age_range[0])
        self.speed = person.get("speed", self.speed_range[0])
        self.strength = person.get("strength", self.strength_range[0])
        self.offense = person.get("offense", self.offense_range[0])
        self.defense = person.get("defense", self.defense_range[0])
        self.overall = person.get("overall", self.calc_overall())
