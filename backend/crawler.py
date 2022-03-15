import os
import requests
import json
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv


def pokemon_get(index, api="https://pokeapi.glitch.me/v1/pokemon/", folder="pokemons"):
    """
    Crawler that gets the pokemon data. First it checks if the file is local, otherwise it gets it from the API.
    :param index: pokemon index
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


def pokemon_get_all(api="https://pokeapi.glitch.me/v1/pokemon/", folder="pokemons", first_index=1):
    """
    Crawler that gets all the pokemon data. It depends on poke_get
    :param first_index: first pokemon index
    :param api: api selected to crawl
    :param folder: folder output
    :return:
    """

    i = first_index
    while True:
        pokemon_get(i, api, folder)
        i += 1


def db_connect():
    """
    Connects to the database with the .env file info
    :return: db connection
    """

    try:

        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv("BE_HOST"),
            port=3306,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_SCHEMA")
        )

    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception('User or password is wrong')

        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            raise Exception('Database does not exist')

        else:
            raise Exception(e)

    return connection


def load_file(num, folder="pokemon"):
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
    except Exception as e:
        raise e

    return file


def pokemon_parsing(folders, num):
    """
    Parses a pokemon from multiple folders and returns the info
    :param folders: folders to search in
    :param num: pokemon number to find
    :return:
    """

    try:
        x = load_file(str(num), str(folders[0]))
        y = load_file(str(num), str(folders[1]))
    except Exception as e:
        raise e

    num = x['number']
    name = x['name'].replace('♀', '-f').replace('♂', '-m')
    gen = x['gen']
    spec = x['species']
    height = round(float(x['height'].replace("'", ".").replace('\"', '')) * 0.3048, 2)  # feet to cm
    weight = round(float(x['weight'].replace(' lbs.', '')) * 0.4535924, 2)  # lbs to kg
    description = x['description']
    sprite = x['sprite']
    base_xp = y['base_experience']
    hp = y['stats'][0]['base_stat']
    atk = y['stats'][1]['base_stat']
    defense = y['stats'][2]['base_stat']
    specialatk = y['stats'][3]['base_stat']
    specialdef = y['stats'][4]['base_stat']
    speed = y['stats'][5]['base_stat']

    male = None
    female = None
    if len(x['gender']) > 1:
        male = x['gender'][0]
        female = x['gender'][1]
    normal = x['abilities']['normal'][0]
    hidden = None
    if x['abilities'] and len(x['abilities']) == 2:
        hidden = x['abilities']['hidden'][0]
    type1 = x['types'][0]
    type2 = None
    if x['types'] and len(x['types']) == 2:
        type2 = x['types'][1]

    return (num, name, gen, spec, height, weight, description, sprite, base_xp, hp, atk, defense, specialatk,
            specialdef, speed, male, female, normal, hidden, type1, type2)


def pokemon_insert(num, info):
    """
    Inserts a pokemon row in the table
    :param num: pokemon number to be inserted
    :return: returns the row ID
    """
    cn = db_connect()
    cursor = cn.cursor()

    # placeholder
    poke = ("INSERT INTO pokemon (ID, name, gen, species, height, weight, description, base_experience, sprite,"
                   "hp, attack, defense, special_attack, special_defense, speed, male, female) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = (num, name, gen, spec, height, weight, description, base_xp, sprite,
              hp, atk, defense, specialatk, specialdef, spd, male, female)
    cursor.execute(poke, data)
    cn.commit()

    cursor.close()
    cn.close()
    print(f'Done with {num}.')

    return cursor.lastrowid


def ability_insert(normal, hidden):
    """

    :param normal:
    :param hidden:
    :return: returns the row ID
    """
    # placeholder
    cn = db_connect()  # placeholder
    cursor = cn.cursor()  # placeholder

    cursor.execute("INSERT INTO abilities (normal, hidden) VALUES (%s, %s, %s)", (normal, hidden))
    cn.commit()
    return cursor.lastrowid


def type_insert(type1, type2):
    """

    :param type1: represents the first type
    :param type2: represents the second type
    :return: returns the row ID
    """

    # placeholder
    cn = db_connect()  # placeholder
    cursor = cn.cursor()  # placeholder

    cursor.execute("INSERT INTO types (type1, type2) VALUES (%s, %s, %s)", (type1, type2))
    cn.commit()
    return cursor.lastrowid


def relation_type_pokemon(pokemon_id, type_id):
    """

    :param pokemon_id: represents the pokemon ID
    :param type_id: represents the type ID
    :return:
    """

    # placeholder
    cn = db_connect()  # placeholder
    cursor = cn.cursor()  # placeholder

    cursor.execute("INSERT INTO relTypesPokemon (pokemonID, typeID) VALUES (%s, %s)", (pokemon_id, type_id))
    cn.commit()


def relation_ability_pokemon(pokemon_id, ability_id):
    """

    :param pokemon_id: represents the pokemon ID
    :param ability_id: represents ability ID
    :return:
    """

    # placeholder
    cn = db_connect()  # placeholder
    cursor = cn.cursor()  # placeholder

    cursor.execute("INSERT INTO relAbilitiesPokemon (pokemonID, abilityID) VALUES (%s, %s)", (pokemon_id, ability_id))
    cn.commit()


if __name__ == '__main__':

    load_file(1)  # example
    print(pokemon_parsing(("pokemons", "pokemons2"), 1))  # example
