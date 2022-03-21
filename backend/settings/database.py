import os
from mysql.connector import errorcode
from mysql import connector

try:
    DB = connector.connect(host=os.environ.get("MYSQL_HOST"),
                           port=3306,
                           user=os.environ.get("MYSQL_USER"),
                           password=os.environ.get("MYSQL_PASSWORD"),
                           database=os.environ.get("MYSQL_DATABASE"))
except connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        raise Exception('User or password is wrong')

    if e.errno == errorcode.ER_BAD_DB_ERROR:
        raise Exception('Database does not exist')

    raise Exception(e)
