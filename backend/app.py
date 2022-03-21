from flask import Flask, request
from settings.database import DB
import json


app = Flask(__name__)


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

    query = "SELECT * FROM pokemon WHERE"
    for arg in args:
        conditions.append(f"{arg}=%s")
        data.append(args.get(arg))

    filters = " AND ".join(conditions)

    query = " ".join([query, filters])
    cursor = DB.cursor()
    cursor.execute(query, tuple(data))
    return json.dumps(cursor.fetchall()[0])


if __name__ == '__main__':
    app.run()
