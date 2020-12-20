import requests
import db_connector, pymysql
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

id = config.get('back_end_testing', 'id_to_insert')
username = config.get('back_end_testing', 'username_to_insert')

url = config.get('back_end_testing', 'rest_api_base_url') + id
json_payload = {'user_name': username}


def run_post_add_user_request(url, payload, id, is_new_user=True):
    response = requests.post(url, json=json_payload)

    # create Json object from all the response (type is dict)
    json_main_object = json.loads(response.text)

    if (json_main_object["Status"] == "ok"):
        return True
    else:
        print("POST request with ID " + id + " and username " + username + " failed")
        if is_new_user:
            raise Exception("test failed")
        else:
            return False


def run_get_request(url, id):
    response = requests.get(url)

    # create Json object from all the response (type is dict)
    json_main_object = json.loads(response.text)

    if (json_main_object["user_name"] == username):
        return True
    else:
        print("GET request with ID " + id + " did not return the name " + username)
        raise Exception("test failed")


def check_user_added_to_db(username, id):
    conn = db_connector.get_db_connection()
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_name FROM users where user_id=%s", id)
    records = cursor.fetchall()
    conn.close()

    if records:
        if records[0]["user_name"] == username:
            return True
        else:
            print("User Name " + username + " was not found in DB for id: " + id)
            raise Exception("test failed")
    else:
        print("no records found for id: " + id)
        raise Exception("test failed")


def main():
    if (run_post_add_user_request(url, json_payload, id)):
        print("Successful - POST request with ID " + id + " and username " + username + " successful")

    if (run_get_request(url, id)):
        print("Successful - GET request with ID " + id + " returned username " + username)

    if (check_user_added_to_db(username, id)):
        print("Successful - username " + username + " inserted to DB - !!! yeppee")


if __name__ == '__main__':
    main()
