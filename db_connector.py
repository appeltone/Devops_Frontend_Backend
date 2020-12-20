from configparser import ConfigParser
import pymysql

config = ConfigParser()
config.read('config.ini')


def get_db_connection():
    connection = pymysql.connect(host=config['database']['host'],
                                 port=int(config['database']['port']),
                                 user=config['database']['user'],
                                 password=config['database']['password'],
                                 db=config['database']['db'],
                                 charset=config['database']['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    if connection != '':
        return connection
    else:
        raise ConnectionError


def get_item_from_config_table(item_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    stmt = "select value from config where item_name = %s"
    data = (item_name,)

    cursor.execute(stmt, data)
    records = cursor.fetchall()
    conn.close()

    return records[0]['value']


def close_db_connection():
    connection.close()


connection = get_db_connection()
print(connection)
connection.close()
