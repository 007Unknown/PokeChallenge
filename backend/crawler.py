import os
import shutil
import requests
import json
import mysql.connector
from settings.database import DB


def pokemon_get(index, api="https://pokeapi.glitch.me/v1/pokemon/", folder="pokemons"):
    """
    Crawler that gets the pokémon data. First it checks if the file is local, otherwise it gets it from the API.
    :param index: pokémon index
    :param api: api selected to crawl
    :param folder: folder output
    :return:
    """

    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, str(folder), str(index) + ".json")

    if not os.path.exists(file_path):
        r = requests.get(url=str(api) + str(index))
        if not r.status_code == 200:
            raise Exception(f"Status code {r.status_code} for {index}")

        with open(file_path, "w") as f:
            if type(r.json()) == dict:
                json.dump(r.json(), f, indent=4)
            else:
                json.dump(r.json()[0], f, indent=4)

        return r.status_code


def pokemon_get_all(api="https://pokeapi.glitch.me/v1/pokemon/", folder="pokemons", first_index=1):
    """
    Crawler that gets all the pokémon data. It depends on poke_get
    :param first_index: first pokémon index
    :param api: api selected to crawl
    :param folder: folder output
    :return:
    """

    index = first_index
    while True:
        pokemon_get(index, api, folder)
        index += 1


def load_file(num, folder="pokemons"):
    """
    Loads a json file and returns it
    :param num: number of the pokémon
    :param folder: folder name
    :return: returns the json file
    """

    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, str(folder), str(num) + ".json")

    try:
        with open(file_path, "r") as f:
            file = json.load(f)
    except FileNotFoundError:
        raise Exception('The file does not exist.')

    return file


def download_image(number=1, folder='images'):
    """
    Downloads an image from the parsed jsons
    :param number: number provided to download from
    :param folder: folder to search in
    :return: returns False if both the directory was made and the file exists, otherwise it gets both
    """

    sprite = load_file(number)['sprite']
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, str(folder), str(number) + ".png")

    if not os.path.exists(str(folder)):
        os.mkdir(str(folder))

    if not os.path.exists(file_path):
        r = requests.get(sprite, stream=True)
        if r.status_code == 200:
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return r.status_code

    return False


def download_images(first_index=1):
    """
    Downloads all images starting from a first index, using download_image function
    :param first_index: first number
    :return: None
    """
    index = first_index
    while True:
        download_image(index)
        index += 1


def feet_to_meter(value):
    """
    Converts feet to meter
    :param value: value to convert
    :return: returns the converted value
    """
    return round(value * 0.3048, 2)


def lb_to_kg(value):
    """
    Converts lb to kg
    :param value: value to convert
    :return: returns the converted value
    """
    return round(value * 0.4535924, 2)


def height_parsing(height):
    """
    Parses the height given
    :param height: height to parse
    :return: returns the parsed height
    """

    if "'" in height:
        height = height.replace("'", ".")
    if "\\" in height:
        height = height.replace("\\", "")
    if '"' in height:
        height = height.replace('"', '')
    if "/" in height:
        height = height.split("/", 1)[0].strip()
    if ".`" in height:
        height = height.replace('.`', '')

    return feet_to_meter(float(height))


def weight_parsing(weight):
    """
    Parses the weight given
    :param weight: weight to parse
    :return: returns the parsed weight
    """

    weight = weight.replace(' ', '')
    if "lbs." in weight:
        weight = weight.replace('lbs.', '')
    if "lbs" in weight:
        weight = weight.replace('lbs', '')
    if "/" in weight:
        weight = weight.split('/', 1)[0]

    return lb_to_kg(float(weight))


def pokemon_parsing(folders, num):
    """
    Parses a pokémon from multiple folders and returns the info
    :param folders: folders to search in
    :param num: pokémon number to find
    :return: returns a tuple with the pokémon parsed
    """

    x = load_file(str(num), str(folders[0]))
    y = load_file(str(num), str(folders[1]))

    num = x['number']
    name = x['name'].replace('♀', '-f').replace('♂', '-m')
    gen = x['gen']
    spec = x['species']
    description = x['description']
    sprite = x['sprite']
    base_xp = y['base_experience']
    hp = y['stats'][0]['base_stat']
    atk = y['stats'][1]['base_stat']
    defense = y['stats'][2]['base_stat']
    special_atk = y['stats'][3]['base_stat']
    special_def = y['stats'][4]['base_stat']
    speed = y['stats'][5]['base_stat']

    gender_rate = {
        "male": x['gender'][0] if len(x['gender']) > 1 else None,
        "female": x['gender'][1] if len(x['gender']) > 1 else None
    }

    abilities = {
        "normal": [ability for ability in x['abilities']['normal']],
        "hidden": [hidden for hidden in x['abilities']['hidden']]
    }

    types = {pokemon_type for pokemon_type in x['types']}

    return (num, name, gen, spec, height_parsing(x['height']), weight_parsing(x['weight']), description, base_xp,
            sprite, hp, atk, defense, special_atk, special_def, speed, gender_rate, abilities, types)


def pokemon_insert(info):
    """
    Inserts a pokémon with parsed information and inserts a row in the table
    :param info: pokémon number to be inserted
    :return: returns the row ID
    """
    cursor = DB.cursor()
    poke = ("INSERT INTO pokemon (ID, name, gen, species, height, weight, description, base_experience, sprite,"
            "hp, attack, defense, special_attack, special_defense, speed, male, female) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8],
            info[9], info[10], info[11], info[12], info[13], info[14], info[15]['male'], info[15]['female'])

    try:
        cursor.execute(poke, data)
        DB.commit()
    except mysql.connector.IntegrityError as e:
        raise Exception(f'Error {e}')

    cursor.close()
    return cursor.lastrowid


def pokemon_insert_all(first_index=1):
    """
    Iterative function that inserts all pokémon with a certain first index
    :param first_index: first pokémon index ID
    :return: returns the row ID
    """

    index = first_index
    while True:
        parse = pokemon_parsing(("pokemons", "pokemons2"), index)
        pokemon_insert(parse)
        index += 1


def ability_insert(pokemon_ability, ability_type):
    """
    Inserts a column in the abilities table
    :param pokemon_ability: pokémon ability name
    :param ability_type: pokémon ability type [normal|hidden]
    :return: returns the row ID
    """

    cursor = DB.cursor()
    cursor.execute("INSERT INTO abilities (ability, abilityType) VALUES (%s, %s)",
                   (pokemon_ability, ability_type))
    DB.commit()
    return cursor.lastrowid


def type_insert(pokemon_type):
    """
    Insert a type column in the types table
    :param pokemon_type: represents the type
    :return: returns the row ID
    """

    cursor = DB.cursor()
    cursor.execute("INSERT INTO types (type) VALUES (%s)", (pokemon_type,))
    DB.commit()
    return cursor.lastrowid


def relation_type_pokemon(pokemon_id, type_id):
    """
    Makes a relation between the type(s) and the pokémon
    :param pokemon_id: represents the pokémon ID
    :param type_id: represents the type ID
    :return:
    """

    cursor = DB.cursor()
    cursor.execute("INSERT INTO relTypesPokemon (pokemonID, typeID) VALUES (%s, %s)", (pokemon_id, type_id))
    DB.commit()


def relation_ability_pokemon(pokemon_id, ability_id):
    """
    Makes a relation between the ability(ies) and the pokémon
    :param pokemon_id: represents the pokémon ID
    :param ability_id: represents ability ID
    :return:
    """

    cursor = DB.cursor()

    cursor.execute("INSERT INTO relAbilitiesPokemon (pokemonID, abilityID) VALUES (%s, %s)", (pokemon_id, ability_id))
    DB.commit()


def full_insert(info):
    """
    Inserts a Pokémon with the desired info
    :param info: full information of the pokémon parsed, can use pokemon_parsing for that
    :return: None
    """

    poke_exists = pokemon_exists(info[1])
    if poke_exists[0]:  # if the pokémon exists, returns the row ID
        poke = poke_exists[1]
    else:
        poke = pokemon_insert(info)  # otherwise, it inserts it
    for pokemon_ability in info[16]['normal']:
        ab_exists = ability_exists(pokemon_ability)
        if ab_exists[0]:  # if the ability exists, returns the row ID
            ability_normal = ab_exists[1]
        else:
            ability_normal = ability_insert(pokemon_ability, "Normal")  # otherwise, it inserts it
        relation_ability_pokemon(poke, ability_normal)  # make the relation between the ability and pokémon

    if info[16]['hidden']:  # if there is any hidden ability
        for pokemon_ability in info[16]['hidden']:
            ab_exists = ability_exists(pokemon_ability)
            if ab_exists[0]:  # if the hidden ability exists, returns the row ID
                ability_hidden = ab_exists[1]
            else:
                ability_hidden = ability_insert(pokemon_ability, "Hidden")  # otherwise, it inserts it
            relation_ability_pokemon(poke, ability_hidden)  # make the relation between the ability and pokémon

    for pokemon_type in info[17]:
        tp_exists = type_exists(pokemon_type)
        if tp_exists[0]:  # if the type exists, returns the row ID
            type_name = tp_exists[1]
        else:
            type_name = type_insert(pokemon_type)  # otherwise, it inserts it
        relation_type_pokemon(poke, type_name)  # make the relation between the type and pokémon


def full_insert_all(index=1, end=807):
    """
    Inserts all (with an index and end) pokémon with the desired info
    :param index: first number given
    :param end: last number given
    :return: None
    """

    for numb in range(index, end+1):
        parsing = pokemon_parsing(("pokemons", "pokemons2"), numb)
        full_insert(parsing)


def pokemon_exists(p):
    """
    Checks if the pokémon exists in the pokemon table
    :param p: column to check the type
    :return: returns bool (if it exists) and the row ID
    """

    cursor = DB.cursor()
    cursor.execute("SELECT * FROM pokemon WHERE name=%s LIMIT 1", (p,))  # searches if there's any of the P pokemon
    y = cursor.fetchall()
    return bool(y), y[0][0] if y else None


def type_exists(t):
    """
    Checks if the type exists in the type table
    :param t: column to check the type
    :return: returns bool (if it exists) and the row ID
    """

    cursor = DB.cursor()
    cursor.execute("SELECT * FROM types WHERE type=%s LIMIT 1", (t,))  # searches if there's any of the T type
    y = cursor.fetchall()
    return bool(y), y[0][0] if y else None


def ability_exists(a):
    """
    Checks if the type exists in the ability table
    :param a: column to check the ability
    :return: returns bool (if it exists) and the row ID
    """

    cursor = DB.cursor()
    cursor.execute("SELECT * FROM abilities WHERE ability=%s LIMIT 1", (a,))  # searches if there's any of the A ability
    y = cursor.fetchall()
    return bool(y), y[0][0] if y else None


if __name__ == '__main__':
    download_images(1)  # example
