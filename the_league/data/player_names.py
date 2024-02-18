import copy
import json
import random
import easygui


def generate_names(num_names, male_ratio):
    first_names = []
    for _ in range(num_names):
        if random.random() < male_ratio:
            first_names.append(get_random_male_name())
        else:
            first_names.append(get_random_female_name())
    return first_names


SUFFIXES = ["I", "II", "III", "Jr.", "Sr."]


def generate_name(male_ratio, suffix=None):

    if random.random() < male_ratio:
        first_name = get_random_male_name()
    else:
        first_name = get_random_female_name()

    last_name = get_random_last_name()

    if suffix is None:
        if random.random() < 0.01:
            suffix = random.choice(SUFFIXES)
        else:
            suffix = ""

    name = f"{first_name} {last_name} {suffix}"
    return name


def get_random_male_name():
    # Add your list of male first names here
    male_first_names = ["John", "Michael", "Robert", "William", "David", "James", "Joseph", "Daniel", "Christopher",
                        "Matthew", "Andrew", "Steven", "Kevin", "Thomas", "Brian", "Jason", "Jeffrey", "Timothy",
                        "Richard", "Ryan", "Mark", "Anthony", "Charles", "Jeremy", "Scott", "Stephen", "Jonathan",
                        "Eric", "Justin", "Patrick", "Benjamin", "Adam", "Tyler", "Nathan", "Brandon", "Aaron",
                        "Paul", "Kenneth", "Edward", "George", "Nicholas", "Dylan", "Zachary", "Gregory", "Samuel",
                        "Joshua", "Jesse", "Jacob", "Travis", "Kyle", "Trevor", "Cody", "Shawn", "Peter", "Cameron",
                        "Ethan", "Lucas", "Evan", "Ian", "Alex"]

    return random.choice(male_first_names)


def get_random_female_name():
    # Add your list of female first names here
    female_first_names = ["Mary", "Jennifer", "Linda", "Patricia", "Susan", "Jessica", "Sarah", "Karen", "Nancy",
                          "Lisa", "Betty", "Margaret", "Emily", "Helen", "Sandra", "Donna", "Ashley", "Kimberly",
                          "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Laura", "Rebecca", "Sharon", "Cynthia",
                          "Kathleen", "Amy", "Angela", "Michelle", "Nicole", "Catherine", "Christine", "Samantha",
                          "Janet", "Rachel", "Diane", "Elizabeth", "Virginia", "Kelly", "Julie", "Anna", "Maria",
                          "Heather", "Martha", "Patricia", "Frances", "Ruth", "Joyce", "Ann", "Marie", "Alice",
                          "Dorothy", "Christina", "Evelyn", "Victoria", "Shirley"]

    return random.choice(female_first_names)


def get_last_names():
    # Add your list of last names here
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                  "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez",
                  "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez",
                  "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson",
                  "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans",
                  "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell"]

    return last_names


def get_random_last_name():
    return random.choice(get_last_names())


player_names = []


def generate_player_names(num_names):
    global player_names
    fname = "C:/Users/austi_000/Documents/Python/Orbiter/the_league/data/player_names.json"
    name_data = load_names(fname)

    first = copy.deepcopy((name_data["first_names"]))
    last = copy.deepcopy(name_data["last_names"])

    player_names = []
    while len(player_names) < num_names:
        first_name = random.choice(first)
        last_name = random.choice(last)
        name = f"{first_name} {last_name}"
        if name not in player_names:
            player_names.append(name)
        else:
            name_count = player_names.count(name)
            name += f" {(name_count + 1) * 'I'}"
            player_names.append(name)

    return player_names





def load_names(fn):
    with open(fn, "r") as f:
        names = json.load(f)
    return names


def save_player_names(filename):
    # Set the desired number of names and male ratio
    num_names = 150
    male_ratio = 0.6

    # Generate the lists
    first_names = generate_names(num_names, male_ratio)
    last_names = get_last_names()

    # Combine the lists into a dictionary
    names_dict = {
        "first_names": first_names,
        "last_names": last_names
    }

    # Save the dictionary as a JSON file
    with open(filename, "w") as file:
        json.dump(names_dict, file)


if __name__ == "__main__":
    # fname = easygui.filesavebox("Save Names", "Save names of players", ".json")
    # save_player_names(fname)

    players = generate_player_names(10)
    for player in players:
        print(player)
