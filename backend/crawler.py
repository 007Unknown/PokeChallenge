import os
import requests
import json


def pokeget():
    """
    Crawler that gets the pokemon data
        - checks first if the file is local, otherwise it gets it from the API
    :return:
    """

    i = 1
    while True:
        dirpath = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(dirpath, "pokemons", str(i)+".json")
        if not os.path.exists(filepath):

            r = requests.get(url="https://pokeapi.glitch.me/v1/pokemon/"+str(i))

            if not r.status_code == 200:
                return f"Status code {r.status_code} for {i}"

            with open(filepath, "w") as f:
                json.dump(r.json()[0], f, indent=4)

        i += 1


if __name__ == '__main__':
    pokeget()
