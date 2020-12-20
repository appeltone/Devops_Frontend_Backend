from flask import Flask
import db_connector

app = Flask(__name__)


@app.route('/users/get_user_data/<int:id>')
def users(id):
    result = get_user_name_from_db(id)
    return result


def get_user_name_from_db(id):
    conn = db_connector.get_db_connection()
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_name FROM users where user_id=%s", id)
    records = cursor.fetchall()
    conn.close()
    if not records:
        return html("<H2 id='error'>" + "User ID " + str(id) + " not found in DB</H2>")
    else:
        return html("<H2 id='user'>" + records[0]["user_name"] + "</H2>")


def html(content):  # Build my own header for the return html <head></head> <body><body/>
    return '<html><head><H2><b>Appel\'s server reply:</b></H2></head><body>' + content + '</body></html>'


if __name__ == '__main__':
    app.run(port=5001, debug=True)
