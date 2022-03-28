from flask import Flask, request
from flask_cors import CORS
from settings.database import DB
import json
import mysql.connector.errors as err

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'


@app.route('/pokemon/', methods=['GET'])
def pokemon():
    """
    Pokémon endpoint
    :return: returns the json information with a query depending on the args
    """

    args = request.args.to_dict()
    data = []
    conditions = []

    query = 'SELECT * FROM pokemon WHERE'
    for arg in args:
        conditions.append(f"{arg}=%s")
        data.append(args.get(arg))

    filters = " AND ".join(conditions)

    if not args:
        query = 'SELECT * FROM pokemon'
    query = " ".join([query, filters])
    cursor = DB.cursor(dictionary=True)
    cursor.execute(query, tuple(data))
    return json.dumps(cursor.fetchall())


@app.route('/pokemon/abilities/', methods=['GET'])
def abilities():
    """
    Pokémon Abilities endpoint
    :return: returns the json information with a query depending on the args
    """

    args = request.args.to_dict()
    print(args)
    data = []
    conditions = []

    for arg in args:
        conditions.append(f"{arg}=%s")
        data.append(args.get(arg))

    filters = " AND ".join(conditions)

    query = """
    SELECT rap.pokemonID, p.name, JSON_ARRAYAGG(JSON_OBJECT('name', a.ability, 'ability_type', a.abilityType))
    FROM relAbilitiesPokemon AS rap
    INNER JOIN pokemon AS p ON rap.pokemonID = p.ID
    INNER JOIN abilities AS a ON rap.abilityID = a.ID
    """

    if args:
        query = " ".join([query, "WHERE", filters, "GROUP by rap.pokemonID"])
    else:
        query = " ".join([query, filters, "GROUP by rap.pokemonID"])

    cursor = DB.cursor()
    try:
        cursor.execute(query, tuple(data))
    except err.ProgrammingError:
        return 'Key does not exist'
    except err.IntegrityError:
        return 'Ambiguous key'

    to_return = []
    for pId, pName, pAbilities in cursor.fetchall():
        to_return.append({"id": pId,
                          "name": pName,
                          "types": json.loads(pAbilities)})

    return {"data": to_return}


@app.route('/pokemon/types/', methods=['GET'])
def types():
    """
    Pokémon types endpoint
    :return: returns the json information with a query depending on the args
    """

    args = request.args.to_dict()
    data = []
    conditions = []

    for arg in args:
        conditions.append(f"{arg}=%s")
        data.append(args.get(arg))

    filters = " AND ".join(conditions)

    query = """
    SELECT rtp.pokemonID, p.name, JSON_ARRAYAGG(JSON_OBJECT('type', t.`type`))
    FROM relTypesPokemon AS rtp
    INNER JOIN pokemon AS p ON rtp.pokemonID = p.ID
    INNER JOIN types AS t ON rtp.typeID = t.ID
    """

    if args:
        query = " ".join([query, "WHERE", filters, "GROUP by rtp.pokemonID"])
    else:
        query = " ".join([query, filters, "GROUP by rtp.pokemonID"])

    cursor = DB.cursor()
    try:
        cursor.execute(query, tuple(data))
    except err.ProgrammingError:
        return 'Key does not exist'
    except err.IntegrityError:
        return 'Ambiguous key'

    to_return = []
    for pId, pName, pTypes in cursor.fetchall():
        to_return.append({"id": pId,
                          "name": pName,
                          "types": json.loads(pTypes)})

    return {"data": to_return}


if __name__ == '__main__':
    app.run()
