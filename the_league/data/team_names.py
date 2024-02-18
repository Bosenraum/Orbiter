import easygui as eg
import json
import random
import copy

first_names = [
    "Cyber", "Galaxy", "Phantom", "Nova", "Electric", "Infinity", "Thunder",
    "Shadow", "Chaos", "Iron", "Venomous", "Crimson", "Elysian", "Mystic",
    "Solar", "Rift", "Thundering", "Astral", "Neon", "Phoenix", "Omega",
    "Dark", "Blaze", "Valkyrie", "Quantum", "Velocity", "Seraphic", "Eclipse",
    "Crystal", "Arcane", "Spectral", "Stormbringer", "Ember", "Radiant",
    "Enigma", "Nebula", "Thunderbolt", "Shadowblade", "Titan", "Aether"
]

last_names = [
    "Vipers", "Titans", "Strikers", "Sentinels", "Storm", "Reapers", "Hawks",
    "Assassins", "Conquerors", "Wolves", "Serpents", "Raiders", "Guardians",
    "Enforcers", "Flares", "Breakers", "Legends", "Warriors", "Knights",
    "Rising", "Hunters", "Dominion", "Brigade", "Vanguard", "Surge", "Vortex",
    "Strikers", "Elite", "Catalysts", "Aces", "Solaris", "Nebulae",
    "Thunderstrike", "Shadowstorm", "Sentinel", "Inferno", "Blazeheart",
    "Tempest", "Venomfang", "Radiance"
]


def save_names(fn):
    global first_names, last_names
    names = {
        "first_names": first_names,
        "last_names": last_names
    }
    with open(fn, "w") as f:
        json.dump(names, f)


def load_names(fn):
    with open(fn, "r") as f:
        names = json.load(f)
    return names


def generate_team_names(num_names):
    fname = "C:/Users/austi_000/Documents/Python/Orbiter/the_league/data/team_names.json"
    name_data = load_names(fname)

    first = copy.deepcopy(name_data["first_names"])
    last = copy.deepcopy(name_data["last_names"])

    team_names = []
    while len(team_names) < num_names:
        first_name = random.choice(first)
        last_name = random.choice(last)
        name = f"{first_name} {last_name}"
        if name not in team_names:
            team_names.append(name)
        else:
            continue

        first.remove(first_name)
        last.remove(last_name)

        if len(first) == 0 or len(last) == 0:
            first = copy.deepcopy(name_data["first_names"])
            last = copy.deepcopy(name_data["last_names"])

    return team_names


if __name__ == "__main__":
    # filename = eg.filesavebox("Save names to file.", "Save Names", ".json")
    # save_names(filename)

    teams = generate_team_names(50)
    for team in teams:
        print(team)
