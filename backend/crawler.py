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


if __name__ == '__main__':

    load_file(1)  # example
