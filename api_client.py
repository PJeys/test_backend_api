#!flask/bin/python
from flask import Flask, jsonify, request
from anomalies import search_anomalies, create_connection
from registration_dynamics import select_all_registrations_by_month
from login_hourly_stats import login_hourly_stats

app = Flask(__name__)


database = r"data.db"
API_KEY = "fXMWznr92ceoaS5yp8PjcA"

@app.route('/api/users/anomalies')
def anoms():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == API_KEY:
        conn = create_connection(database)
        return jsonify(search_anomalies(conn))
    elif auth == None:
        return jsonify("status code 401")
    else:
        return jsonify("status code 403")


@app.route('/api/registration/bymonth/')
@app.route('/api/registration/bymonth/<int:datemonth>', methods=['GET'])
def month(datemonth=None):
    headers = request.headers
    auth = headers.get("X-Api-Key")
    conn = create_connection(database)
    if auth == API_KEY:
        if not datemonth:
            try:
                return jsonify(select_all_registrations_by_month(conn))
            except Exception as e:
                return 'status code 404'
        else:
            try:
                return jsonify(select_all_registrations_by_month(conn, datemonth))
            except Exception as e:
                return 'status code 404'
            return jsonify(select_all_registrations_by_month(conn, datemonth))
    elif auth == None:
        return jsonify("status code 401")
    else:
        return jsonify("status code 403")


@app.route('/api/sessions/byhour')
def logins():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == API_KEY:
        conn = create_connection(database)
        bar = request.args.to_dict()
        if bar:
            return jsonify(login_hourly_stats(conn,bar))
        else:
            return jsonify(login_hourly_stats(conn))
    elif auth == None:
        return jsonify("status code 401")
    else:
        return jsonify("status code 403")


if __name__ == '__main__':
    app.run(debug=True)
