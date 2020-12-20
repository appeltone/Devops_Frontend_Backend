from flask import Flask, request, jsonify
import db_connector, pymysql
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to my PYTHON front-end/back-end Flask REST API project :-)"


@app.route('/users', methods=["GET"])
def get_users_list():
    conn = db_connector.get_db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    print("total rows are: ", len(records))

    result_dict = []
    for row in records:
        result_dict.append(row)

    conn.close()
    return jsonify(result_dict)


@app.route('/users/<int:id>', methods=["GET", "POST", "PUT", "DELETE"])
def users(id):
    conn = db_connector.get_db_connection()
    cursor = conn.cursor()

    # GET method -----------------------------------------------------
    if request.method == "GET":
        cursor.execute("SELECT user_name FROM users where user_id=%s", id)
        records = cursor.fetchall()
        conn.close()
        if not records:
            return jsonify({"Status": "error", "reason": "no such id"}), 500
        else:
            return jsonify({"Status": "ok", "user_name": records[0]["user_name"]}), 200

    # POST method -----------------------------------------------------
    flag = False

    if request.method == "POST":
        while (True):
            try:
                if (flag == False):
                    current_time = get_current_time_date()
                    json_payload = request.get_json()  # get json payload as dict
                    cursor.execute("INSERT INTO users (user_id, user_name, creation_date) VALUES (%d, '%s', '%s')" %
                                   (id, json_payload["user_name"], current_time))
                    conn.commit()
                else:
                    cursor.execute("SELECT user_id FROM users WHERE user_id =(SELECT MAX(user_id) FROM users)")
                    records = cursor.fetchall()
                    current_time = get_current_time_date()
                    json_payload = request.get_json()  # get json payload as dict
                    id_used_if_exist = records[0]['user_id']
                    cursor.execute("INSERT INTO users (user_id, user_name, creation_date) VALUES (%d, '%s', '%s')" %
                                   (records[0]['user_id'] + 1, json_payload["user_name"], current_time))
                    conn.commit()
                    break
            except pymysql.err.IntegrityError as err:
                message = err.args
                print(">> GOT AN ERROR >>>>>", message)  # Write error message to console as well
                flag = True
        conn.close()
        return jsonify({"Status": "ok", "user_added": json_payload["user_name"], "id_used": id_used_if_exist}), 200

    # PUT method -----------------------------------------------------
    if request.method == "PUT":
        current_time = get_current_time_date()
        json_payload = request.get_json()  # get json payload as dict
        cursor.execute("UPDATE users SET user_name='%s', creation_date='%s' WHERE user_id=%s" %
                       (json_payload["user_name"], current_time, id))
        conn.commit()
        conn.close()
        # If cursor.rowcount is 0 it means that no records where updated, ID not found, if 1 so 1 record changed
        if cursor.rowcount == 0:
            return jsonify({"Status": "error", "reason": "no such id"}), 500
        else:
            return jsonify({"Status": "ok", "user_updated": json_payload["user_name"]}), 200

    # DELETE method -------------------------------------------------
    if request.method == "DELETE":
        cursor.execute("DELETE from users where user_id=%s", id)
        conn.commit()
        print("Rows deleted: ", cursor.rowcount)
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({"Status": "error", "reason": "no such id"}), 500
        else:
            return jsonify({"Status": "ok", "user_deleted": id}), 200


def get_current_time_date():
    now = datetime.now()
    return now.strftime("%d/%m/%y %H:%M:%S")


if __name__ == '__main__':
    app.run(debug=True)
