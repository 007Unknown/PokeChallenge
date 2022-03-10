import requests
import json
import time


def pokeget():

    url = "https://pokeapi.glitch.me/v1/pokemon/"

    for x in range(1, 820):
        r = requests.get(url=url+str(x))

        if not r.status_code == 200:
            break

        with open(f'pokemons\\{str(x)}.json', 'w') as f:
            json.dump(r.json()[0], f, indent=4)

        time.sleep(0.5)


if __name__ == '__main__':
    pokeget()
